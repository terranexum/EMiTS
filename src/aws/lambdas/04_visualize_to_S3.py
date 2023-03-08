import boto3
import os

s3 = boto3.client('s3')
gds2webgl = boto3.client('lambda')

def lambda_handler(event, context):
    # Get the bucket and key of the uploaded GDSII file
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    # Create a unique name for the output HTML file
    html_key = os.path.splitext(key)[0] + '.html'
    # Set the input and output paths for the GDS2WebGL Lambda function
    input_path = '/tmp/input.gds'
    output_path = '/tmp/output.html'
    # Download the GDSII file from S3
    s3.download_file(bucket, key, input_path)
    # Invoke the GDS2WebGL Lambda function
    gds2webgl.invoke(
        FunctionName='gds2webgl-lambda-function',
        Payload={
            'input_path': input_path,
            'output_path': output_path
        }
    )
    # Upload the resulting HTML file to S3
    s3.upload_file(output_path, bucket, html_key)
    return {
        'statusCode': 200,
        'body': 'HTML file generated successfully'
    }
