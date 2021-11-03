import json
from io import BytesIO
import zipfile
import boto3

s3 = boto3.resource('s3')

bucket_name = "tkw-priv"
bucket_name_dest = "tkw-itgaiden-bucket"
archive_name_dest = "images_new.zip"
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

""" In Java:
AmazonS3Client s3 = new AmazonS3Client(myCredentials);
for ( S3ObjectSummary summary : S3Objects.withPrefix(s3, "my-bucket", "photos/") ) {
    System.out.printf("Object with key '%s'n", summary.getKey());
}
"""

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
        print('Source Bucket:', bucketNameSource)
        print('Target zip:', bucketNameDest + '/' + archiveNameDest)

         # Get number of objects from bucket
        num_objects = count_objects(summaries)
        print("Source bucket files count:", num_objects)

        # Create IO file
        zip_buffer = BytesIO()

        print ("TEST:", summaries)
        print ("<<TEST2>>:", summaries_all)
        print("Entering in the loop")
        
        #summaries = s3_bucket.objects
        # For each object inside the objectsCollectionmanager.
        for obj in summaries.page_size(10).pages():
            print("Inside loop")
            print("s3.Bucket(bucketObjects->:",summaries)
            print("Objects inside summaries>>:", obj)
            print("***************************************************")
            
            ##Destination file creation.
            zip_file = s3.ObjectSummary(bucketNameDest, archiveNameDest)
            print("zip_file:", zip_file)
            print("Upload files to {}...".format(archiveNameDest))
            print("WITH ZIPFILE.ZIPFILE starts")

            ## Open Zipfile and append each object,key (file)
            with zipfile.ZipFile(zip_buffer, mode="a",compression=zipfile.ZIP_DEFLATED) as zf:
                #Iterate within the ObjectSummary.
                for img in obj:
                    #object = bucket.Object('tiles/10/S/DG/2015/12/7/0/B01.jp2')
                    #img_data = object.get().get('Body').read()
                    zf.writestr(img.key, img.get().get('Body').read())
                    print("------------------------------")
                    print("Print Object summary (X)>>:",img)
                    print("Print key (x.key)>>:", img.key)
                    print("Print key (x.get)>>:", img.get)
                    print("Print key (x.get)Body>>:", img.get()['Body'])
                    #print("Print key (x.get)Body.READ>>:", img.get()['Body'].read())
                    print("------------------------------")
            
            # Set ACL for the ZIP as public-read
            print ("ZIP FILE FINISHED>>>>>", zip_file)
            zip_file.put(Body=zip_buffer.getvalue(), ACL='public-read')
            # for obj in page.objects.filter(Prefix='images/'):
            #     print('{0}:{1}'.format(page.name, obj.key))
        return "Download your images at: "+"'https://%s.s3.amazonaws.com/%s'" % (bucketNameDest, archiveNameDest)
    
    except Exception as err:
        return "Exception :" + str(err)