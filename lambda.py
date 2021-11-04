import json
from io import BytesIO
import zipfile
import boto3

s3 = boto3.resource('s3')

bucket_name_src = "tkw-priv"
bucket_name_dst = "tkw-itgaiden-bucket"
zip_name_dst = "images_041121.zip"

# An object is a file 
# and any metadata that describes that file
s3_bucket = s3.Bucket(bucket_name_src)
summaries = s3_bucket.objects

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
        
        # bucketNameSource = bucket_name
        # bucketNameDest = bucket_name_dest
        # archiveNameDest = archive_name_dest

        # Safe to delete
        delete_object_if_exists(bucket_name_dst, zip_name_dst)
        print('Target zip:', bucket_name_dst + '/' + zip_name_dst)

         # Get number of objects from bucket
        num_objects = count_objects(summaries)
        print("Source bucket files count:", num_objects)

        # Create IO file
        zip_buffer = BytesIO()
        
        # Gather the content from the body and parse it (JSON)
        body = (event['body'])
        dataDic = json.loads(body)
        print("BEFORE LOOP")
        
        zip_file = s3.ObjectSummary(bucket_name_dst, zip_name_dst)


        for item in dataDic['Images']:
            imgName = item['Name']
           
            print("zip_file:", zip_file)
            print("Uploading files to ", zip_name_dst)
            print("***************************************************")
            
            obj = s3.Object(bucket_name_src, imgName)
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

            #s3_client = boto3.client('s3')
            #url = s3_client.generate_presigned_url(ClientMethod='get_object', Params={'Bucket': bucket_name_dst, 'Key': zip_file}, ExpiresIn=90)
        #    print ("URL:", url)

        return "Download your images at: "+"'https://%s.s3.amazonaws.com/%s'" % (bucket_name_dst, zip_name_dst)
    
    except Exception as err:
        return "Exception :" + str(err)