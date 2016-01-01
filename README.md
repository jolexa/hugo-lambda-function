# hugo-lambda-function
AWS Lambda function to build a Hugo website. Inspired by Ryan Brown's [hugo-lambda](https://github.com/ryansb/hugo-lambda)

Blog Post, https://blog.jolexa.net/post/writing-a-lambda-function-for-hugo/

## Files
`main.py` - The actual function that gets ran

`build-package.sh` - Helper information to build the zip file

## Ideology
The idea of this repo is to build a zip package that you can deploy to AWS Lambda. The lambda function fires on a SNS event, which is publishing GitHub events. In a nutshell,

1. Publish the site contents repo to a AWS SNS Topic. In GitHub, repo settings -> Webhooks
  * Recommended: IAM user for the credentials in GitHub.
2. Subscribe the AWS Lambda function to the SNS topic. (No special IAM permissions are needed for this)
3. Lambda function's job is to build the static content and push to a S3 bucket of the same name as the repo name
  * Lambda function will need to have IAM permissions to read/list/put/delete S3 bucket objects and Cloudwatch Logging permissions.
 

## Zip File
The zip file was needed because the function needs boto3 library (for ease, the awscli libraries) - an alternative implementation might re-write `aws s3 sync` in native python then this zip file becomes mostly moot.

1. Launch a t2.nano, running the published supported AMI (https://docs.aws.amazon.com/lambda/latest/dg/current-supported-versions.html)
2. Run `build-package.sh`
3. Fetch resulting zip file
4. Upload to AWS Lambda
5. Remember to shutdown the t2.nano if not being used

## Future
* It might be nice to package up the zip file generation in a CloudFormation Stack
* It would be very nice to package up the entire function/SNS topic in a CloudFormation Stack as well
