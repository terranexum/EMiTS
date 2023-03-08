import boto3
import os

# Define AWS clients
ecs = boto3.client('ecs')
codebuild = boto3.client('codebuild')

# Define function to start an ECS task to build Docker images
def start_ecs_task(event, context):
    # Define the ECR repository and tag for the Docker image
    ecr_repo = os.environ['ECR_REPO']
    ecr_tag = os.environ['ECR_TAG']

    # Define the ECS task parameters
    task_params = {
        'taskDefinition': os.environ['ECS_TASK_DEFINITION'],
        'cluster': os.environ['ECS_CLUSTER'],
        'launchType': 'FARGATE',
        'networkConfiguration': {
            'awsvpcConfiguration': {
                'subnets': os.environ['ECS_SUBNETS'].split(','),
                'securityGroups': os.environ['ECS_SECURITY_GROUPS'].split(','),
                'assignPublicIp': 'DISABLED'
            }
        },
        'overrides': {
            'containerOverrides': [
                {
                    'name': 'build',
                    'environment': [
                        {
                            'name': 'GITHUB_TOKEN',
                            'value': os.environ['GITHUB_TOKEN']
                        },
                        {
                            'name': 'REPO_URL_OPENMETA',
                            'value': 'https://github.com/metamorph-inc/OpenMETA'
                        },
                        {
                            'name': 'REPO_URL_OPENROAD',
                            'value': 'https://github.com/The-OpenROAD-Project/OpenROAD'
                        },
                        {
                            'name': 'REPO_URL_GDS2WEBGL',
                            'value': 'https://github.com/s-holst/GDS2WebGL'
                        },
                        {
                            'name': 'DOCKER_REPO',
                            'value': f'{ecr_repo}:{ecr_tag}'
                        }
                    ],
                    'command': [
                        '/bin/bash', '-c',
                        'pip3 install awscli && \
                        git clone $REPO_URL_OPENMETA && \
                        git clone $REPO_URL_OPENROAD && \
                        git clone $REPO_URL_GDS2WEBGL && \
                        cd OpenMETA && \
                        make docker-build && \
                        cd ../OpenROAD && \
                        make tools && \
                        cd ../GDS2WebGL && \
                        make && \
                        docker build -t $DOCKER_REPO .'
                    ],
                }
            ]
        },
        'count': 1,
        'platformVersion': 'LATEST'
    }

    # Start the ECS task
    response = ecs.run_task(**task_params)

    # Return the ARN of the started task
    return response['tasks'][0]['taskArn']
