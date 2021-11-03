import json
from io import BytesIO
import zipfile
import boto3

s3 = boto3.resource('s3')

bucket_name = "tkw-priv"
bucket_name_dest = "tkw-itgaiden-bucket"
archive_name_dest = "images_new031121.zip"
archive_public_access = "true"

# An object is a file 
# and any metadata that describes that file
s3_bucket = s3.Bucket(bucket_name)
summaries = s3_bucket.objects
summaries_all = s3_bucket.objects.all()
#s3_bucket.objects.pages()

def count_objects(objects):
    count=0
    for x in objects.all(): 
        count+=1
    return count

def delete_object_if_exists(bucketName, key):
    obj = s3.Object(bucketName,key)
    if obj is None:
        return
    obj.delete()

def main_handler(event, context):
    try:
        print('Lambda starts:')
    	
        bucketNameSource = bucket_name
        bucketNameDest = bucket_name_dest
        archiveNameDest = archive_name_dest
        
        # Safe to delete
        delete_object_if_exists(bucketNameDest, archiveNameDest)
        print('Target zip:', bucketNameDest + '/' + archiveNameDest)

         # Get number of objects from bucket
        num_objects = count_objects(summaries)
        print("Source bucket files count:", num_objects)

        # Create IO file
        zip_buffer = BytesIO()
        
        # Gather the content from the body and parse it (JSON)
        body = (event['body'])
        dataDic = json.loads(body)
        
        for item in dataDic['Images']:
            imgName = item['Name']
            zip_file = s3.ObjectSummary(bucketNameDest, archiveNameDest)
            print("zip_file:", zip_file)
            print("Uploading files to ", archiveNameDest)
            print("***************************************************")
            
            obj = s3.Object(bucket_name, imgName)
            content = obj.get()['Body'].read()
            
            ## Open Zipfile and append each object,key (file)
            with zipfile.ZipFile(zip_buffer, mode="a",compression=zipfile.ZIP_DEFLATED) as zf:
                #Write image name and content within the archive.
                zf.writestr(imgName, content)
                print("------------------------------")
                print("Image added to the zip (ZipInfo)>>:",imgName)
                print("------------------------------")
            
            # Set ACL for the ZIP as public-read
            print ("ZIP FILE FINISHED>>>>>", zip_file)
            zip_file.put(Body=zip_buffer.getvalue(), ACL='public-read')
            
        return "Download your images at: "+"'https://%s.s3.amazonaws.com/%s'" % (bucketNameDest, archiveNameDest)
    
    except Exception as err:
        return "Exception :" + str(err)