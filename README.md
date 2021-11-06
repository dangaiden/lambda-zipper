# lambda-zipper

# Purpose
Lambda function to zip files from S3 bucket.


# Requirements

Although in this repository you will only find the lambda function plus the images used (not the deployed resources), this is what I have used in AWS:

- S3 buckets (2): One will completely private with the images and another one will be used for the end-users to download the zipped file with their images.
- Roles and permissions
- An API of some type, here I have used a simple HTTP one provided by AWS (API Gateway)
- Cloudwatch: Important to troubleshoot your own Lambda function.
# How-to
All files within the img folder are the ones that can be downloaded from a private S3.

To download a zip file with the images that you want, you must use a JSON file with the structure as "images.json" in this repository.

You can invoke the API and pass the your JSON file using *curl*, an example:

``` bash
curl -s -X POST -d "@images.json" -H "Content-Type: application/json"  https://2mbfznw9f7.execute-api.us-east-2.amazonaws.com/
```

This command will invoke the API endpoint that will trigger the lambda function.
If there are no issues, an output with a huge link will appear:

``` bash
Download your ZIP file: >>>>https://tkw-itgaiden-bucket.s3.amazonaws.com/gpu65mqth.zip?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIAYYQ7G3ETA5HW6UOY%2F20211106%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Date=20211106T152703Z&X-Amz-Expires=90&X-Amz-SignedHeaders=host&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEOf%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMiJHMEUCIQDfu6mCe76ocBUxG%2BCCEGsjFRfgCFrUnoUb4UZpLAIQqwIgAdu8c5zKOqFMNvcfb0cLcQoB9f0%2Fyv9rTZrilclYKioqmgIIkP%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2MDI0MzQ2MjM3ODIiDIg71txLcZL5YxbbjiruASsyiZyV%2BHVOJu9Nh%2B%2BPnZTKKvB1kFyHa1KvTRyzwL409vQb1Y47PHOM1ucmfCciE4QrceW8NGpKroUWnRBg%2FyyX4uH4varkZfT1qzocIae1PROfO%2FuNQB3YgcrBP61m3OHRodMZ06kpbm0CkcRnO6Sn6Fv22dTGmj5C0sbOoP1Dupfhv6hUEml0rZqXRu9h5BI6UBfrowVi0mxURdGdOKBua%2BV49sBZFUnuQh9dgow9%2BYry8Z0YSqqQJG7PaDuetMjSIQ7xNbOuTfMMkyChdCMnV3qZRSpFkOiBtvFAF8rD9skklVxbdbvBcMDwJ4AwqbqajAY6mgGnhm9sNiNNHPcpiDiPrB%2B%2BLx1ZUmlBE7nbs8UoAKatPqJH%2Brenm6sE72mUqEpQvq7kXkhrcWNjMfFiHmA5IBUS7H9vr7ll6SuAbgLbfr7e6IEyRRdZL%2FW9man4RkQGsHE1smB9PoV1X9RjiTN1ILsTZEkQI%2FJLfKFaKphIp9dFePrTAXaSTcMYrMP9ppNrpyLD2ha7Su%2FwQzdw&X-Amz-Signature=57bca034cc06c2a3b7f9e5cebb86b54aa79e20a67c252759511dede107b0932c <<<<
```