# lambda-zipper

 A lambda function which zip files using in-memory with selected files given by data sent from a user.
 The selected files are stored in a bucket and will be zipped to a destination bucket to permit the end user download them. 

 The result is a secure link where you can download your images (Pokemon and Yu-gi-oh!) cards, the link expires in 90 seconds.
# Purpose

This repository is intended to show how a Lambda function can compress files using in-memory streaming with selected files given by data sent from an API (which has been invoked by a user).

The workflow is the following one: 

![Workflow](img/readme/workflow.png)

# Specifics used for Lambda

- Runtime: Python 3.7
- Handler: lambda_function.main_handler
- Architecture: x86_64
# Resources needed

Although in this repository you will only find the lambda function plus the images used (not the deployed resources in AWS), this is what I have used in AWS:

- S3 buckets (2): 
    - tkw-priv (Access defined: Bucket and objects not public): Contains the images that can be used to create the zip file.
    - tkw-itgaiden-bucket (Access: Objects can be public): Stores the zip files that has been requested by the users.
- An API of some type, here I have used a simple HTTP one provided by AWS (API Gateway) to not complicate myself more.
- Cloudwatch: Important to troubleshoot your own Lambda function.
- IAM configuration:
The Lambda function uses a role (TKW_function-role) which has a Policy attached.
In that policy is where the permissions are defined, it looks similar to this:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "logs:CreateLogGroup",
            "Resource": "arn:aws:logs:us-east-2:6024xxxx:*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": [
                "arn:aws:logs:us-east-2:6024xxxxx:log-group:/aws/lambda/TKW_function:*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:PutObjectAcl",
                "s3:GetObject",
                "s3:GetObjectAcl",
                "s3:DeleteObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::tkw-itgaiden-bucket",
                "arn:aws:s3:::tkw-priv"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:PutObjectAcl",
                "s3:GetObject",
                "s3:GetObjectAcl",
                "s3:DeleteObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::tkw-itgaiden-bucket/*",
                "arn:aws:s3:::tkw-priv/*"
            ]
        }
    ]
}
```
# How-to

All files within the img folder are the ones that can be downloaded from the private S3 bucket.

You can download a zip file with the images that you want from there. Be aware that you must use a JSON file with the structure as "images.json" in this repository.



You must invoke the API and pass the your JSON file using *curl*, an example:

``` bash
curl -s -X POST -d "@images.json" -H "Content-Type: application/json"  https://2mbfznw9f7.execute-api.us-east-2.amazonaws.com/
```

This command will invoke the API endpoint that will trigger the lambda function.

If there are no issues, an output with a huge link will appear:

``` bash
Download your ZIP file (expires in 90s): https://tkw-itgaiden-bucket.s3.amazonaws.com/gpu65mqth.zip?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIAYYQ7G3ETA5HW6UOY%2F20211106%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Date=20211106T152703Z&X-Amz-Expires=90&X-Amz-SignedHeaders=host&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEOf%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMiJHMEUCIQDfu6mCe76ocBUxG%2BCCEGsjFRfgCFrUnoUb4UZpLAIQqwIgAdu8c5zKOqFMNvcfb0cLcQoB9f0%2Fyv9rTZrilclYKioqmgIIkP%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2MDI0MzQ2MjM3ODIiDIg71txLcZL5YxbbjiruASsyiZyV%2BHVOJu9Nh%2B%2BPnZTKKvB1kFyHa1KvTRyzwL409vQb1Y47PHOM1ucmfCciE4QrceW8NGpKroUWnRBg%2FyyX4uH4varkZfT1qzocIae1PROfO%2FuNQB3YgcrBP61m3OHRodMZ06kpbm0CkcRnO6Sn6Fv22dTGmj5C0sbOoP1Dupfhv6hUEml0rZqXRu9h5BI6UBfrowVi0mxURdGdOKBua%2BV49sBZFUnuQh9dgow9%2BYry8Z0YSqqQJG7PaDuetMjSIQ7xNbOuTfMMkyChdCMnV3qZRSpFkOiBtvFAF8rD9skklVxbdbvBcMDwJ4AwqbqajAY6mgGnhm9sNiNNHPcpiDiPrB%2B%2BLx1ZUmlBE7nbs8UoAKatPqJH%2Brenm6sE72mUqEpQvq7kXkhrcWNjMfFiHmA5IBUS7H9vr7ll6SuAbgLbfr7e6IEyRRdZL%2FW9man4RkQGsHE1smB9PoV1X9RjiTN1ILsTZEkQI%2FJLfKFaKphIp9dFePrTAXaSTcMYrMP9ppNrpyLD2ha7Su%2FwQzdw&X-Amz-Signature=57bca034cc06c2a3b7f9e5cebb86b54aa79e20a67c252759511dede107b0932c 
```

In case you try to access the link after 90 seconds, something like this will appear:

![Link Expired](img/readme/link_expired.png)

# References used

- https://docs.aws.amazon.com/lambda/latest/dg/services-apigateway.html
- https://dev.to/lineup-ninja/zip-files-on-s3-with-aws-lambda-and-node-1nm1
- https://medium.com/dev-bits/ultimate-guide-for-working-with-i-o-streams-and-zip-archives-in-python-3-6f3cf96dca50
- https://boto3.amazonaws.com/v1/documentation/api/latest/guide/collections.html
- https://docs.python.org/3.7/library/zipfile.html#zipfile.ZipFile.writestr