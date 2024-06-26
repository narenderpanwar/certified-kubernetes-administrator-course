# StatefulSet in Kubernetes:

- StatefulSets are kubernetes resource that allow us to deploy and manage `Stateful` applications.
- `Stateful applications` are those applications that require a persistent storage to function properly. Example - database.
  
  ![state](../../images/statefulset.png)
- But can we not deploy or manage a Database with Deployment object?
- Deployment vs Statefulset:
  
  - Lets say we have a web application deployed as Deployment and to make it highly available, there are three replicas of it.
  - The Application data is stored in database and we have deployed the database as Deployment too.
    
    ![state](../../images/statefulset1.png)
  - Everything is fine here, Application works fine but we have made our Application Highly Available but what about Database?
  - Let's scale the Database pods now.
    ![state](../../images/statefulset2.png)
  - Now the application wants to connect to the database for read and write operation.
  - Obviosly the traffic from web pod will go through the service of the database, and this service can route traffic to any of the backend database pods randomly.
    ![state](../../images/statefulset3.png)
  - This means that data can we written in any pod and read from any other pod. This is the biggest problem of Data inconsistency.
  - There must be something like-
    ![state](../../images/statefulset4.png)
    
    - A centralized pod where application writes data to this pod only.
    - Rest all pods should replicate the data from this pod.
    - Problems:
      - How do we tell the application that, say Pod01 is to be used for only write operations? A pod's IP gets changed if recreated and there is no proper DNS assigned for Pods.
      - How do we tell the other pods to replicate the data from the Pod01?

## StatefulSets:

- To resolve the above problems, we have Statefulsets in kubernetes that has the following features:
- **Stable Identity**:
  Every pod managed by a StatefulSet gets a unique and stable identifier, usually in the form of an ordinal index (e.g., web-0, web-1, web-2). This identity remains consistent even if the pod is deleted and recreated.
- **Ordered Deployment**:
  StatefulSets ensure that pods are deployed and scaled in a predictable order. This means that pods are created one by one, and each pod is not started until the previous one is running and ready.
- **Persistent Storage**:
  StatefulSets are designed to work well with stateful applications that require persistent storage. They can automatically provision and attach persistent volumes to each pod in a consistent and predictable manner.
- **Headless Service**:
  By default, StatefulSets automatically create a DNS record for each pod, allowing other services to discover and connect to individual pods directly. This is useful for applications like databases where each pod might have its own IP address and need to be addressed individually.
- **Updating Pods**:
  When updating a StatefulSet, pods are updated in a rolling fashion, similar to Deployments. However, StatefulSets ensure that each pod is updated one at a time, maintaining the order and identity of the pods throughout the update process.

#### Lets see how these features are solving the problems we faced earlier:

- Let's say we have told out applciation to use the pod mysql-0 for write operations using its hostname.
  ![state](../../images/statefulset5.png)
- If we increase the replias to 3 now, the statefulset will create a pod with mysql-1 name, clones the data from mysql-0 pod and keeps the hostname of mysql-0 into it as centralized hostname so that it can connect to it and replicate the data from it.
  ![state](../../images/statefulset8.png)
- Once the pod mysql-1 completes all these tasks and comes in ready state, Statefulset will deploy another pod mysql-2 which will copy the data from mysql-1 pod and keep the hostname of mysql-0 for future replications.
  
  ![state](../../images/statefulset6.png)
- If the StatefulSet needs to scale down the Pods, It will delete the pods in reverse order like mysql-2 will be deleted first then mysql-1 and so on.

