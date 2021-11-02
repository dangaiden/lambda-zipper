import json
from io import BytesIO
import zipfile
import boto3

s3 = boto3.resource('s3')

bucket_name = "tkw-priv"
bucket_name_dest = "tkw-itgaiden-bucket"
archive_name_dest = "images_awesome.zip"
archive_public_access = "true"

###### NEW ####
s3_bucket = s3.Bucket(bucket_name)
#summaries = s3_bucket.objects.all()
summaries = s3_bucket.objects
########

def function_return(success, message, link = None):
    return {
        "statusCode": 200,
        "body": json.dumps({
            "success" : success,
            "message": message,
            "link": link
        })
    }

def all_objects_from_bucket(bucketName):
    bucket = s3.Bucket(bucketName)
    return bucket.objects

def objects_from_bucket_per_page(bucketName, page_size):
    return s3.Bucket(bucketName).objects.page_size(page_size)

def count_objects(objects):
    count=0
    for x in objects.all(): 
        count+=1
    return count

def get_object_summary(bucket, key):
    return s3.ObjectSummary(bucket, key)

""" JAVA!!!
AmazonS3Client s3 = new AmazonS3Client(myCredentials);
for ( S3ObjectSummary summary : S3Objects.withPrefix(s3, "my-bucket", "photos/") ) {
    System.out.printf("Object with key '%s'n", summary.getKey());
}

"""

def data_from_object(bucketName, key):
    obj = s3.Object(bucketName,key)
    return obj.content_type

def link_from_object(bucketName, key):
    return 'https://%s.s3.amazonaws.com/%s' % (bucketName, key)

def delete_object_if_exists(bucketName, key):
    obj = s3.Object(bucketName,key)

    if obj is None:
        return
    
    obj.delete()


""" 

bucket_name = 'tkw-itgaiden-bucket/images/'
bucket_name_dest = "tkw-itgaiden-bucket/download/"
archive_name_dest = "imageschachis.zip"
archive_public_access = "true"
amount_of_files_to_upload = 10 

"""


def main_handler(event, context):
    try:
        print('Started the Lambda function')

        bucketNameSource = bucket_name
        bucketNameDest = bucket_name_dest
        archiveNameDest = archive_name_dest
        archivePublicAccess = archive_public_access

        print('Source Bucket:', bucketNameSource)
        print('Target archive:', bucketNameDest + '/' + archiveNameDest)

        # Get objects from bucket
        objects = all_objects_from_bucket(bucketNameSource)
        num_objects = count_objects(objects)


        print("Source bucket files count:", num_objects)

    	# Safe to delete.
        delete_object_if_exists(bucketNameDest, archiveNameDest)

        # Create IO file
        binary = BytesIO()

        print("Entering in the loop")
        
        #for page in objects.page_size(amount_objects).pages():
        for page in objects.page_size(20).pages():
            print("INSIDE THE LOOP")
            ##Destination file 
            zip_file = get_object_summary(bucketNameDest, archiveNameDest)
            print("Upload files to {}...".format(archiveNameDest))
            with zipfile.ZipFile(binary, mode="a",compression=zipfile.ZIP_DEFLATED) as zf:
                for x in page:
                    zf.writestr(x.key, x.get()['Body'].read())
                    print('Target archive:', bucketNameDest + '/' + archiveNameDest)
                    print("Print key:", x.key)
                    
            if(archivePublicAccess):
                zip_file.put(Body=binary.getvalue(), ACL='public-read')
            else:
                zip_file.put(Body=binary.getvalue())
            # for obj in page.objects.filter(Prefix='images/'):
            #     print('{0}:{1}'.format(page.name, obj.key))

        link = link_from_object(bucketNameDest, archiveNameDest)

        return function_return(True, "Files successfully compressed!", link)
    
    except Exception as err:
        return function_return(False, "Exception :" + str(err))