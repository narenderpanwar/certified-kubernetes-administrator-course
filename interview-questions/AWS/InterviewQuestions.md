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

