# Authentication

- Take me to [Video Tutorial](https://kodekloud.com/topic/authentication/)

In this section, we will take a look at authentication in a kubernetes cluster

## Accounts

![auth1](../../images/auth1.PNG)

- Different types of users access the cluster: Administrators, Developers, End users and third-party applications.
- End user security is managed internally by applications.
- So, we are left with 2 types of users :
  
  - Humans (**`Users`**) such as the administrator & developers, and
  - Robots such as other processes/services or applications that require access to the cluster (which we provide using **`Service accounts`**)
  
  ![acc1](../../images/acc1.PNG)
- Kubernetes does not natively manage **`User`** accounts. It relies on external sources like files with user & password details, certificates, or third-party identity services (e.g., LDAP). Hence, we cannot create Users `kubectl create user user1`  like this.
- However, incase of **`Service accounts`** Kubernetes can manage them. So we can create and manage Service accounts like `kubectl create sa sa1`

  ![acc2](../../images/acc2.PNG)

- All user access is managed by the kube apiserver and all of the requests goes through apiserver.
- The kube apiserver then authenticates before processing them.
  
  ![acc3](../../images/acc3.PNG)

## So how does the kube apiserver autheticates?

# Authentication Mechanisms

- There are different authentication mechanisms that can be configured.
  
  - Static user and password or token file.
  - Certificates.
  - Third-party authentication protocols (LDAP, Kerberos etc).
  
  ![auth2](../../images/auth2.PNG)

## Authentication Mechanisms - Basic

![auth3](../../images/auth3.PNG)

## Kube-apiserver configuration

- If you set up via kubeadm then update kube-apiserver.yaml manifest file with the option.
  
  ![auth4](../../images/auth4.PNG)

## Authenticate User

- To authenticate using the basic credentials while accessing the API server specify the **`username & password`** in a curl command.
  
  ```
  $ curl -v -k http://master-node-ip:6443/api/v1/pods -u "user1:password123"
  ```
  
  ![auth5](../../images/auth5.PNG)
- To authenticate using the **`token`**  while accessing the API server specify the **`token`** using Authorization: Bearer header in a curl command.
- We can have additional column in the user-details.csv file to assign users to specific groups.
  
  ```
  $ curl -v -k http://master-node-ip:6443/api/v1/pods --header "Authorization: Bearer KpjCVbI7rCFAgu1cUc48"
  ```
  
  ![auth6](../../images/auth6.PNG)

## Note

![note](../../images/note.PNG)

#### K8s Reference Docs

- https://kubernetes.io/docs/reference/access-authn-authz/authentication/

