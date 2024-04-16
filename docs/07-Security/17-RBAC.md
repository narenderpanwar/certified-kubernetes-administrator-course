# RBAC

- Take me to [Video Tutorial](https://kodekloud.com/topic/role-based-access-controls/)
- With role-based access controls, instead of directly associating a user or a group with a set of permissions (as we did in ABAC), we define a Role.
- In this case for developers, we create a role with the set of permissions required for developers then we associate all the developers to that role. Similarly, create a role for security users with the right set of permissions required for them then associate the user to that role.
- Now whenever a change needs to be made to the user's access we simply modify the role and it reflects on all developers immediately. Hence, Role-based access controls provide a more standard approach to managing access within the Kubernetes cluster.

## How do we create a role?

- Each role has 3 sections
  
  - **`apiGroups`** : For core group, you can leave the API group section as blank. For any other group, you specify the group name.
  - **`resources`**
  - **`verbs`**: The actions that they can perform.
  
  ```
  apiVersion: rbac.authorization.k8s.io/v1
  kind: Role
  metadata:
  name: developer
  rules:
  - apiGroups: [""] # "" indicates the core API group
  resources: ["pods"]
  verbs: ["get", "list", "update", "delete", "create"]
  - apiGroups: [""]
  resources: ["ConfigMap"]
  verbs: ["create"]
  ```
  
  ```
  $ kubectl create -f developer-role.yaml
  ```

## The next step is to link the **`User`** to that **`Role`**.

- For this we create another object called **`RoleBinding`**. This role binding object links a user object to a role.
  
  ```
  apiVersion: rbac.authorization.k8s.io/v1
  kind: RoleBinding
  metadata:
  name: devuser-developer-binding
  subjects:
  - kind: User
  name: dev-user # "name" is case sensitive
  apiGroup: rbac.authorization.k8s.io
  roleRef:
  kind: Role
  name: developer
  apiGroup: rbac.authorization.k8s.io
  ```
  
  ```
  $ kubectl create -f devuser-developer-binding.yaml
  ```
- Also note that the roles and role bindings fall under the scope of namespace. So here the dev user gets access to pod and config maps within the default namespace. If you want to limit the dev user's access within a different name space then specify the namespace within the metadata of the definition file while creating them.
  
  ![rbac1](../../images/rbac1.PNG)

## View RBAC

- To list roles
  
  ```
  $ kubectl get roles
  ```
- To list rolebindings
  
  ```
  $ kubectl get rolebindings
  ```
- To describe role
  
  ```
  $ kubectl describe role developer
  ```
  
  ![rbac2](../../images/rbac2.PNG)
- To describe rolebinding
  
  ```
  $ kubectl describe rolebinding devuser-developer-binding
  ```
  
  ![rbac3](../../images/rbac3.PNG)

#### What if you being a user would like to see if you have access to a particular resource in the cluster.

## Check Access

- You can use the kubectl auth command
  
  ```
  $ kubectl auth can-i create deployments
  $ kubectl auth can-i delete nodes
  ```
  
  ```
  $ kubectl auth can-i create deployments --as dev-user
  $ kubectl auth can-i create pods --as dev-user
  ```
  
  ```
  $ kubectl auth can-i create pods --as dev-user --namespace test
  ```
  
  ![rbac5](../../images/rbac5.PNG)

## Resource Names

- We just saw how you can provide access to users for resources like pods within the namespace.
- For example, say you have five parts in namespace you wanna give access to a user to pods, but not all pods. You can restrict access to the blue and orange pod alone by adding a resource names field to the rule. Well, the sit for this lecture,
  
  ```
  apiVersion: rbac.authorization.k8s.io/v1
  kind: Role
  metadata:
    name: developer
  rules:
  - apiGroups: [""] # "" indicates the core API group
    resources: ["pods"]
    verbs: ["get", "update", "create"]
    resourceNames: ["blue", "orange"]
  ```
  
  ![rbac4](../../images/rbac4.PNG)

#### K8s Reference Docs

- https://kubernetes.io/docs/reference/access-authn-authz/rbac/
- https://kubernetes.io/docs/reference/access-authn-authz/rbac/#command-line-utilities

