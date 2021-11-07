import json
from io import BytesIO
import zipfile
import boto3
import random
import string

## Variables
s3 = boto3.resource('s3')
bucket_name_src = "tkw-priv"
bucket_name_dst = "tkw-itgaiden-bucket"

## Some useful functions
def random_zipname (len):
    random_string = ""
    letters_and_digits = string.ascii_lowercase + string.digits
    for number in range(len):
        random_string += random.choice(letters_and_digits)
    random_string += ".zip"
    return random_string

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

## Some declared variables
# Create a random name for zip file.
zip_name_dst = random_zipname(9)

# An object is a file and any metadata that describes that file.
s3_bucket = s3.Bucket(bucket_name_src)
summaries = s3_bucket.objects

### Handler starts here
def main_handler(event, context):
    try:
        print('Lambda starts:')

        # Delete old file if new file has the same name.
        delete_object_if_exists(bucket_name_dst, zip_name_dst)
        print('Target zip:', bucket_name_dst + '/' + zip_name_dst)

        # Get number of objects from bucket
        num_objects = count_objects(summaries)
        print("Source bucket files count:", num_objects)

        # Initialize the io
        zip_buffer = BytesIO()
        
        # Gather the content from the body and parse it (JSON)
        body = (event['body'])
        dataDic = json.loads(body)
        
        # Declare zipfile with the data content and the object metadata stored by Amazon S3
        zip_file = s3.Object(bucket_name_dst, zip_name_dst) 

        # Loop to iterate within the JSON file we received from "event" and was parsed.
        # We will gather each image and append it to a zipfile using IO (in-memory streaming).
        for item in dataDic['Images']:
            # Gather the file name (filtering by "Name")
            imgName = item['Name']
           
            print("Uploading files to ", zip_name_dst)
            
            # Here we gather the object (file) from the source bucket (the private one)
            obj = s3.Object(bucket_name_src, imgName)
            # Read it's content
            content = obj.get()['Body'].read()
            
            ## Open Zipfile (object in the destination bucket) and append each object that we are reading.
            with zipfile.ZipFile(zip_buffer, mode="a",compression=zipfile.ZIP_DEFLATED) as zf:
                # write image name and content within the archive.
                zf.writestr(imgName, content)
                print("File added to the zip (ZipInfo):", imgName)

        ## Out of the loop.
        # Set ACL for the ZIP as public-read
        print ("Images were successfully zipped in the file:", zip_file)
        zip_file.put(Body=zip_buffer.getvalue(), ACL='public-read')

        # We generate a presigned url with 90 secs of expiration and referencing the destination file (zipfile)
        url = boto3.client('s3').generate_presigned_url(ClientMethod='get_object', Params={'Bucket': bucket_name_dst, 'Key': zip_file.key}, ExpiresIn=90)
        print ("URL:", url)

        # This will be the output if there are no errors.
        return "Download your ZIP file (expires in 90s): "+ url + " "
    
    except Exception as err:
        return "Exception :" + str(err)