import json
from io import BytesIO
import zipfile
import boto3

s3 = boto3.resource('s3')

bucket_name = "tkw-priv"
bucket_name_dest = "tkw-itgaiden-bucket"
archive_name_dest = "images_new.zip"
archive_public_access = "true"

###### NEW ####
s3_bucket = s3.Bucket(bucket_name)
#summaries = s3_bucket.objects.all()
summaries = s3_bucket.objects
########

def count_objects(objects):
    count=0
    for x in objects.all(): 
        count+=1
    return count

""" JAVA!!!
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

        print("Entering in the loop")
        
        #for page in objects.page_size(amount_objects).pages():
        for page in summaries.page_size(20).pages():
            print("INSIDE THE LOOP")
            print("s3.Bucket(bucketName)->:",s3_bucket)
            print("s3.Bucket(bucketObjects->:",summaries)
            print("PAGE>>>>:", page)
            print("***************************************************")
            
            ##Destination file 
            zip_file = s3.ObjectSummary(bucketNameDest, archiveNameDest)
            print("zip_file:", zip_file)
            print("Upload files to {}...".format(archiveNameDest))
            print("WITH ZIPFILE.ZIPFILE starts")

            ## Open Zipfile and append each object,key (file)
            with zipfile.ZipFile(zip_buffer, mode="a",compression=zipfile.ZIP_DEFLATED) as zf:
                for x in page:
                    zf.writestr(x.key, x.get()['Body'].read())
                    print("------------------------------")
                    print("Print key (x.key)>>:", x.key)
                    print("Print Object summary (X)>>:",x)
                    print("------------------------------")
            
            zip_file.put(Body=zip_buffer.getvalue(), ACL='public-read')
            # for obj in page.objects.filter(Prefix='images/'):
            #     print('{0}:{1}'.format(page.name, obj.key))
        return "Download your images at: "+"'https://%s.s3.amazonaws.com/%s'" % (bucketNameDest, archiveNameDest)
    
    except Exception as err:
        return "Exception :" + str(err)