# Authorization

- Take me to [Video Tutorial](https://kodekloud.com/topic/authorization/)

In this section, we will take a look at authorization in kubernetes

## Why do you need Authorization in your cluster?

- As an admin, we are able to perform any sort of operation but soon we will have others accessing the cluster as well such as the other administrators, developers, testers or other applications like monitoring applications or continuous delivery applications like Jenkins, etc.
- So, we will be creating accounts for them to access the cluster by creating usernames and passwords or tokens, or signed TLS certificates or service accounts. But we don't want all of them to have the same level of access as us.

  ![at1](../../images/at1.PNG)

## Authorization Mechanisms

- There are different authorization mechanisms supported by kubernetes
  - Node Authorization
  - Attribute-based Authorization (ABAC)
  - Role-Based Authorization (RBAC)
  - Webhook

## Node Authorization

![node-auth](../../images/node-auth.png)

## ABAC

- Attribute-based authorization is where you associate a user or a group of users with a set of permissions. (`kind`: `Policy`)
- In this case, we say the dev user can view, create and delete pods. You do this by creating a policy file with a set of policies defined in adjacent format as shown below and pass this file into the API server. Similarly, we create a policy definition file for each user or group in this file.
- Now, every time you need to add or make a change in the security, you must edit this policy file manually and restart the Kube API Server. That is why, the attribute-based access control configurations are difficult to manage.

  ![abac](../../images/abac.PNG)

## RBAC

- With role-based access controls, instead of directly associating a user or a group with a set of permissions (as we did in ABAC), we define a Role.
- In this case for developers, we create a role with the set of permissions required for developers then we associate all the developers to that role. Similarly, create a role for security users with the right set of permissions required for them then associate the user to that role.
- Now whenever a change needs to be made to the user's access we simply modify the role and it reflects on all developers immediately. Hence, Role-based access controls provide a more standard approach to managing access within the Kubernetes cluster.

  ![rbac](../../images/rbac.PNG)

## Webhook

- What if you want to manage authorization externally and not through the built-in mechanisms that we just discussed.
- For instance, Open Policy Agent is a third-party tool that helps with admission control and authorization. You can have Kubernetes make an API call to the Open Policy Agent with the information about the user and his access requirements, and have the Open Policy Agent decide if the user should be permitted or not. Based on that response, the user is granted access.

![webhook](../../images/webhook.PNG)

## Authorization Modes

- The mode options can be defined on the kube-apiserver

  ![mode](../../images/mode.PNG)
- When you specify multiple modes, it will authorize in the order in which it is specified

  ![mode1](../../images/mode1.PNG)

  #### K8s Reference Docs


  - https://kubernetes.io/docs/reference/access-authn-authz/authorization/
