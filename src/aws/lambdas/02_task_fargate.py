import boto3
import os

# Define the S3 bucket where input/output files will be stored
bucket_name = "my-s3-bucket"

# Define the input and output file paths
input_file_path = "input_files/input.txt"
output_file_path = "output_files/output.txt"

def lambda_handler(event, context):
    # Create an ECS client
    ecs_client = boto3.client('ecs')

    # Define the ECS task parameters
    task_params = {
        'taskDefinition': 'my-task-def:1',
        'cluster': 'my-cluster',
        'launchType': 'FARGATE',
        'networkConfiguration': {
            'awsvpcConfiguration': {
                'subnets': [
                    'subnet-0123456789abcdef',
                    'subnet-0123456789abcdef'
                ],
                'assignPublicIp': 'ENABLED'
            }
        },
        'overrides': {
            'containerOverrides': [
                {
                    'name': 'openmeta-container',
                    'environment': [
                        {
                            'name': 'INPUT_FILE',
                            'value': f's3://{bucket_name}/{input_file_path}'
                        },
                        {
                            'name': 'OUTPUT_FILE',
                            'value': f's3://{bucket_name}/{output_file_path}'
                        }
                    ]
                },
                {
                    'name': 'openroad-container',
                    'environment': [
                        {
                            'name': 'INPUT_FILE',
                            'value': f's3://{bucket_name}/{output_file_path}'
                        },
                        {
                            'name': 'OUTPUT_FILE',
                            'value': f's3://{bucket_name}/{output_file_path}'
                        }
                    ]
                },
                {
                    'name': 'gds2webgl-container',
                    'environment': [
                        {
                            'name': 'INPUT_FILE',
                            'value': f's3://{bucket_name}/{output_file_path}'
                        },
                        {
                            'name': 'OUTPUT_FILE',
                            'value': f's3://{bucket_name}/{output_file_path}'
                        }
                    ]
                }
            ]
        }
    }

    # Run the ECS task
    response = ecs_client.run_task(**task_params)

    return response
