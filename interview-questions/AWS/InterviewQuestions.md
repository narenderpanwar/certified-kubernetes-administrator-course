# Question 1:

#### How to Shift RDS from One Region to Another with Zero Downtime?

#### 1. Prepare for the Migration:

- Ensure you have appropriate permissions in both the source and destination regions.
- Check for any regional limitations or differences that might affect your RDS instance.

#### 2. Set Up the Destination RDS Instance:

- Create a new RDS instance in the destination region with the same configuration (DB engine, instance type, storage, etc.) as the source RDS instance.
- Make sure the destination instance is in the same VPC and subnet group as the source instance if applicable.

#### 3. Initiate Data Replication:

- Use AWS Database Migration Service (DMS) to replicate data from the source RDS instance to the destination RDS instance.
- Configure DMS to continuously replicate changes from the source to the destination to minimize downtime during the final cutover.

#### 4. Perform a Test Migration:

- Before the final migration, perform a test migration to ensure everything works as expected.
- Verify that data is replicating correctly and that applications can connect to the destination RDS instance without issues.

#### 5. Final Data Synchronization:

- Once the test migration is successful, stop application writes to the source RDS instance.
- Allow DMS to catch up with any remaining changes on the source RDS instance and replicate them to the destination.

#### 6. Switch DNS or Application Connection:

- Update your application's connection string or DNS records to point to the destination RDS instance.
- This step is critical for achieving zero downtime, so ensure DNS TTL (Time to Live) values are set appropriately to minimize propagation delay.

#### 7. Verify and Monitor:

- After switching over to the destination RDS instance, thoroughly test your application to ensure everything is functioning correctly.
- Monitor the new RDS instance for any performance issues or errors, especially during peak usage times.

#### 8. Clean Up:

- Once you're confident that the migration was successful, delete the source RDS instance and any associated resources in the source region.
- Update any other AWS services or configurations that were pointing to the old RDS instance.

# Question 2:

#### What is an S3 Bucket Policy?

#### An S3 bucket policy is a JSON-based access policy that specifies who can access your Amazon S3 bucket and what actions they can perform on the objects within the bucket. These policies are attached to S3 buckets and help define permissions for various operations such as read, write, delete, and list.

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::example-bucket/*"
    },
    {
      "Sid": "AllowPutObject",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::123456789012:user/example-user"
      },
      "Action": "s3:PutObject",
      "Resource": "arn:aws:s3:::example-bucket/*"
    }
  ]
}

```





