# lambda-zipper
Lambda function to zip files from S3 bucket.


All files within the img folder are the ones that can be downloaded from a private S3.

To download a zip file with the images that you want, you must use a JSON file with the structure as "images.json" in this repository.

You can invoke the API and pass the your JSON file using *curl*, an example:

```
curl -s -X POST -d "@images.json" -H "Content-Type: application/json"  https://2mbfznw9f7.execute-api.us-east-2.amazonaws.com/
```

This will invoke the API that will trigger the lambda function.