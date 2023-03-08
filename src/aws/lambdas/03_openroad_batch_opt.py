import boto3
import json
import os

def lambda_handler(event, context):
    # Get input file from S3
    s3 = boto3.client('s3')
    input_bucket = event['input_bucket']
    input_key = event['input_key']
    input_file = os.path.basename(input_key)
    s3.download_file(input_bucket, input_key, '/tmp/' + input_file)
    
    # Submit Batch job to run OpenROAD optimization
    batch = boto3.client('batch')
    job_name = 'openroad-optimization-' + input_file
    job_definition = 'openroad-optimization'
    job_queue = 'openroad-job-queue'
    environment = [
        {
            'name': 'INPUT_FILE',
            'value': '/tmp/' + input_file
        },
        {
            'name': 'OUTPUT_BUCKET',
            'value': event['output_bucket']
        },
        {
            'name': 'OUTPUT_KEY',
            'value': event['output_key']
        }
    ]
    job = batch.submit_job(
        jobName=job_name,
        jobQueue=job_queue,
        jobDefinition=job_definition,
        containerOverrides={
            'environment': environment
        }
    )
    job_id = job['jobId']
    
    # Return job ID to client
    return {
        'statusCode': 200,
        'body': json.dumps({
            'job_id': job_id
        })
    }
