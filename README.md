# hugo-lambda-function
AWS Lambda function to build a Hugo website

## Files
`main.py` - The actual function that gets ran

`build-package.sh` - Helper information to build the zip file

## Ideology
The idea of this repo is to build a zip package that you can deploy to AWS Lambda. The lambda function fires on a SNS event, which is publishing GitHub events. In a nutshell,

1. Publish the site contents repo to a AWS SNS Topic. In GitHub, repo settings -> Webhooks
  * Recommended: IAM user for the credentials in GitHub.
2. Subscribe the AWS Lambda function to the SNS topic. (No special IAM permissions are needed for this)
3. Lambda function's job is to build the static content and push to a S3 bucket of the same name as the repo name
  * Lambda function will need to have IAM permissions to read/list/put/delete S3 bucket objects and basic execution permission.
