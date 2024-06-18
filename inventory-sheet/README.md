# Jenkins Pipeline for AWS Inventory Report Generation

This Jenkins pipeline automates the process of generating an AWS inventory report using the provided Python script (`main.py`). The pipeline includes stages for cleaning the workspace, pulling the repository, downloading artifacts from S3, executing the Python script, and handling post-build actions.

## Pipeline Configuration

### Parameters

- `ENV`: Choose the environment name (e.g., 'non-prod').
- `BRANCH`: Git branch name (default: 'master').

### Options

- Build Discarder: Retains 5 builds and 5 artifacts.
- Timestamps: Adds timestamps to build output.

### Environment Variables

- `DEFAULT_ENV`: Default environment name ('non-prod').
- `DEFAULT_BRANCH`: Default Git branch name ('main').
- `GIT_URL`: Git repository URL.
- `GIT_PATH`: Path to the inventory script within the Git repository.
- `REGION_NAME`: AWS region name ('us-east-1').
- `REPOSITORY_NUMBER`: AWS account/repository number.
- `PROJECT_NAME`: Project name ('Generic').
- `SNS_TOPIC_NAME`: SNS topic name for alerts ('non-prod-generic-infra-alert').
- `S3_BUCKET_NAME`: S3 bucket name for configuration ('non-prod-generic-config').
- `S3_BUCKET_PATH`: Path to the configuration file in S3 ('aws-resource-utilization/inputs.yml').

### Triggers

The pipeline is triggered daily at 9 AM using the cron expression `H 9 * * *`.

## Pipeline Stages

1. **Setting Build:**
   
   - Assigns a display name and description to the build.
2. **Cleaning the Workspace:**
   
   - Cleans up the Jenkins workspace using the WsCleanup plugin.
3. **Pulling the Repository:**
   
   - Checks out the specified Git branch from the configured repository.
4. **Download Artifacts from S3:**
   
   - Downloads the configuration file (`inputs.yml`) from the specified S3 bucket.
5. **Execute Python Script:**
   
   - Sets up a Python virtual environment, installs dependencies, and executes the Python script (`main.py`) to generate the AWS inventory report.

## Post-Build Actions

- **On Failure:**
  - Sends an SNS notification in case of build failure, providing details about the failed deployment.

## Usage

1. Configure the Jenkins pipeline with the required parameters, options, and environment variables.
2. Update the values in this `inputs.yml` file according to your AWS environment and preferences.
3. Upload inputs.yml configration file to your specified S3 bucket in jenkins pipeline.
4. Run the Jenkins pipeline, and it will automatically trigger the AWS inventory report generation based on the specified schedule.

