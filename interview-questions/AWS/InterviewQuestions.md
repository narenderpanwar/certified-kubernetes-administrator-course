# Question 1:

#### How to Shift RDS from One Region to Another with Zero Downtime?

#### **With Zero Downtime Using AWS DMS:**

1. **Create a Replication Instance**: In the AWS DMS console, create a new replication instance in the target AWS region. This replication instance will be used to perform the data migration. [1][5]
2. **Create Source and Target Endpoints**: Define the source and target endpoints for the migration. For the source, select the existing RDS instance you want to migrate. For the target, specify the details of the new RDS instance you want to create in the target region. [1][2][5]
3. **Enable Logging and CDC**: Ensure that the source RDS instance has binary logging (binlog) enabled to support Change Data Capture (CDC). This will allow the migration to capture and replicate ongoing changes to the data during the migration process. [1][4]
4. **Create a Migration Task**: In the AWS DMS console, create a new migration task that specifies the source and target endpoints, and configure the task settings as needed (e.g., full load, CDC, etc.). [1][5]
5. **Start the Migration Task**: Begin the migration task. AWS DMS will perform a full load of the data from the source RDS instance to the target RDS instance in the new region, and then continue to replicate changes in real-time using CDC. [1][4][5]
6. **Monitor the Migration**: Monitor the progress of the migration task in the AWS DMS console. Ensure that the data is being replicated successfully and that there are no errors. [1][5]
7. **Cutover to the New Region**: Once the migration is complete, you can cutover your application to the new RDS instance in the target region. This may involve updating connection strings, DNS records, or other application configurations. [1]
8. **Clean Up**: After the cutover, you can delete the old RDS instance, the replication instance, and other resources created for the migration process. [5]

Key considerations during the migration process include:

- Replicating any Secrets Manager secrets used by the RDS database to the target region [1]
- Migrating backup processes and automation to the target region [1]
- Ensuring proper network configuration (VPC, security groups, etc.) in the target region [1]
- Handling any external user access dependencies, such as Active Directory integration [1]
- Updating application configurations to use the new RDS endpoint [1]

#### **With Some Downtime:**

1. **Create a snapshot of the existing RDS instance**: First, create a manual snapshot of the RDS instance you want to migrate. This will capture the entire database state.
2. **Copy the snapshot to the destination region**: In the RDS console, locate the snapshot you created and use the "Copy Snapshot" action to copy it to the destination AWS region. This will create a duplicate snapshot in the target region.
3. **Create a new RDS instance in the destination region**: In the RDS console of the destination region, use the "Restore from Snapshot" option to create a new RDS instance based on the copied snapshot. This will provision a new RDS instance in the target region with the same data as the source.

# Question 2:

#### What is an S3 Bucket Policy?

- An S3 bucket policy is a JSON-based access policy that specifies who can access your Amazon S3 bucket and what actions they can perform on the objects within the bucket. These policies are attached to S3 buckets and help define permissions for various operations such as read, write, delete, and list.

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
      "Effect": "Deny",
      "Principal": {
        "AWS": "arn:aws:iam::123456789012:user/example-user"
      },
      "Action": "s3:PutObject",
      "Resource": "arn:aws:s3:::example-bucket/*"
    }
  ]
}
```

# Question 3:

#### How would you delete 500TB of data from S3 quickly and efficiently?

- To delete an AWS S3 bucket with 500TB of data, the fastest and most cost-effective solution would be to use the S3 Lifecycle configuration.
- The S3 Lifecycle configuration can be used to automate the deletion of objects based on their age or version. By setting up a Lifecycle policy to expire objects in the bucket, you can gradually delete the contents of the bucket over time or in specified timeframe.
- Here is a step-by-step guide to help you:
  
  1. Log in to the AWS Management Console and navigate to the S3 bucket you want to delete.
  2. Open the "Lifecycle" configuration tab for the bucket.
  3. Create a new lifecycle policy, and set the expiration rules to delete objects that are over a certain age or version.
  4. Set the expiration period to a time frame that makes sense for your data, such as 1day, 2day or 7 days.
  5. Save the policy and apply it to the bucket.
- With this policy in place, S3 will automatically delete the objects that meet the expiration criteria, and you can gradually reduce the size of the bucket over time. This is a more cost-effective, less time-consuming and stress-less approach as amazon takes care of running this process rather than manually deleting all of the objects at once as manual processes can break in middle for many reasons.

# Question 4:

#### What does ALB Logs contains? Where can we check ALB Logs?

- Elastic Load Balancing provides access logs that capture detailed information about requests sent to your load balancer.
- Each log contains information such as the time the request was received, the client's IP address, latencies, request paths, and server responses. You can use these access logs to analyze traffic patterns and troubleshoot issues.
- Access logs is an optional feature of Elastic Load Balancing that is disabled by default.
- After you enable access logs for your load balancer, Elastic Load Balancing captures the logs and stores them in the Amazon S3 bucket that you specify as compressed files.

# Question 5:

#### What Load Balancer would you suggest to a Developer?

**ALB (Application Load Balancer):**

* Ideal for HTTP and HTTPS traffic.
* Supports content-based routing, allowing you to route requests based on the content of the request (like URL path or host headers).
* Suited for applications built using microservices architecture or container-based applications.
* Offers advanced features like SSL termination, WebSocket support, and integration with AWS services like AWS Lambda and Amazon ECS.

**NLB (Network Load Balancer):**

* Recommended for TCP traffic, including TCP traffic on custom ports.
* Ideal for handling high volumes of traffic and maintaining low latencies.
* Works well for applications that require static IP addresses for clients, as NLB provides static IP addresses.
* Suitable for UDP traffic, including VoIP, gaming, and IoT applications.

In general, if you're dealing with HTTP or HTTPS traffic and need more advanced routing capabilities, ALB would be a better choice. If your application requires handling TCP traffic at scale with low latency or needs static IP addresses, NLB might be the better option.

Consider your specific requirements, such as the type of traffic your application will handle, scalability needs, and whether you require advanced routing features, to make an informed decision between ALB and NLB.

# Question 6:

#### How can an EC2 instance in Account 1 access S3 of Account 2?

To allow an EC2 instance in one AWS account to access S3 buckets in another AWS account, you typically need to set up cross-account IAM roles and policies. Here's a general outline of the steps involved:

1. **Create an IAM Role in the Account with the S3 Bucket (Account 2)**:
   
   - In the AWS Management Console, navigate to the IAM service.
   - Create a new IAM role with permissions to access the S3 bucket. This role will be assumed by the EC2 instance in Account 1.
   - Attach a policy to this role that grants the necessary permissions to access the S3 bucket. This policy should specify the actions allowed on the S3 bucket and any resources it contains.
2. **Define a Trust Relationship for the IAM Role**:
   
   - Edit the trust relationship of the IAM role created in Step 1 to trust the AWS account ID of the account where the EC2 instance resides (Account 1). The trust relationship should specify the principal as the EC2 service in Account 1.
   
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Principal": {
           "AWS": "arn:aws:iam::ACCOUNT-ID-OF-EC2-INSTANCE:root"
         },
         "Action": "sts:AssumeRole"
       }
     ]
   }
   ```
3. **Assign an IAM Role to the EC2 Instance**:
   
   - Assign the IAM role created in Step 1 to the EC2 instance. This allows the instance to assume the permissions defined in the IAM role.
4. **Access S3 from the EC2 Instance**:
   
   - Use the AWS SDK or CLI with appropriate credentials to access the S3 bucket in Account 2. The SDK or CLI will automatically use the IAM role attached to the EC2 instance for authentication and authorization.

# Question 7:

#### What would happen if you allow an IP in Rule 1 of NACL and then deny that same IP in Rule 2?

- In a Network Access Control List (NACL), rules are evaluated in order, starting from the lowest number and moving to the highest. Once a matching rule is found, further rule evaluation stops.
  
  1. **Allow then Deny (Rule 1 Allow, Rule 2 Deny):** In this case, the IP would be allowed by Rule 1, and the traffic from that IP would be permitted. Rule 2 would never be evaluated for this IP because the evaluation stops once a matching rule is found.
  2. **Deny then Allow (Rule 1 Deny, Rule 2 Allow):** If the IP is denied by Rule 1, it would be blocked regardless of what Rule 2 says. Rule 2 wouldn't be evaluated for this IP because the evaluation stops once a matching rule is found.

# Question 8:

#### How to Upgrade RDS Engine version with Zero Downtime?

#### **With Zero Downtime Using AWS DMS:**

1. Create parameter group for MySQL 8 version

    - Create a new parameter group for MySQL 8.0 version.
    - Ensure that the parameter group is compatible with the MySQL 8.0 engine.
    - Configure the necessary parameters in the parameter group as per your application requirements.
    - Associate the new parameter group with the MySQL 8.0 RDS instance.

 2. Create a read replica of MySQL 5.7 master RDS instance



    - Create a read replica of the existing MySQL 5.7 master RDS instance.
    - Ensure that the read replica is configured with the same database engine version (5.7) as the master.
    - Monitor the replication lag between the master and the read replica to ensure that the replica is in sync.

3. When the replica is in sync (lag is 0) start the upgrade process

    - Verify that the read replica is in sync with the master by checking the replication lag.
    - Once the lag is 0, you can proceed with the upgrade process.

4. Upgrade the read replica to MySQL 8.0.31 and enable backups as we need to create read replicas of this instance


    - Upgrade the read replica to MySQL 8.0.31 version.
    - During the upgrade process, ensure that the new parameter group for MySQL 8.0 is associated with the upgraded read replica.
    - Enable automated backups for the upgraded read replica instance to facilitate the creation of additional read replicas.

5. Create second-level replicas of upgraded MySQL 8 read replicas

    - Create additional read replicas of the upgraded MySQL 8.0.31 read replica instance.
    - These second-level read replicas will inherit the MySQL 8.0.31 version and the associated parameter group.
    - Monitor the replication lag between the upgraded read replica and its second-level replicas to ensure they remain in sync.

6. Promote the upgraded replica to a master
   
   - Once the upgrade process is complete and the read replicas are in sync, you can promote the upgraded read replica to become the new master instance.
   - This will make the upgraded MySQL 8.0.31 instance the new primary database, and the second-level read replicas will now replicate from this new master.
   - Ensure that any applications or services that were connected to the previous MySQL 5.7 master are now updated to connect to the new MySQL 8.0.31 master instance.

#### **With Minimal Downtime:**

* RDS Blue/Green Deployments help make and test database changes before implementing them in a production environment.
* RDS Blue/Green Deployment has the blue environment as the current production environment and the green environment as the staging environment.
* RDS Blue/Green Deployment creates a staging or green environment that exactly copies the production environment.
* Green environment is a copy of the topology of the production environment and includes the features used by the DB instance including the Multi-AZ deployment, read replicas, the storage configuration, DB snapshots, automated backups, Performance Insights, and Enhanced Monitoring.
* Green environment or the staging environment always stays in sync with the current production environment using logical replication.
* RDS DB instances in the green environment can be changed without affecting production workloads. Changes can include the upgrade of major or minor DB engine versions, upgrade of underlying file system configuration, or change of database parameters in the staging environment.
* Changes can be thoroughly tested in the green environment and when ready, the environments can be switched over to promote the green environment to be the new production environment.
* Switchover typically takes under a minute with no data loss and no need for application changes.
* Blue/Green Deployments are currently supported only for RDS for MariaDB, MySQL, and PostgreSQL

