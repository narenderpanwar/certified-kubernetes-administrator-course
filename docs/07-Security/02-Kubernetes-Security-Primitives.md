# Kubernetes Security Primitives

- Take me to [Video Tutorial](https://kodekloud.com/topic/kubernetes-security-primitives/)

In this section, we will take a look at kubernetes security primitives

## 1) Secure Hosts forming the Cluster:

- Disable root access.
- Disable password-based authentication.
- Enable SSH key-based authentication.
- Implement additional security measures for physical or virtual infrastructure hosting Kubernetes.

![sech](../../images/sech.PNG)

## 2) Securing Kubernetes Cluster:

- **`Authentication Mechanisms:`**
  
  - Determine who can access the cluster.
  - Authentication methods include:
    - User IDs and passwords stored in static files.
    - Tokens.
    - Certificates.
    - Integration with external authentication providers like LDAP.
    - Creation of service accounts for machines.
- **`Authorization Mechanisms:`**
  
  - Determine what actions users can perform.
  - Implemented through role-based access controls (RBAC).
  - Users associated with groups having specific permissions.
  - Other authorization modules include attribute-based access control, Node authorizers, and webhooks.

![seck](../../images/seck.PNG)

## 3) TLS Certificates

- All communication with the cluster, between the various components such as the ETCD Cluster, kube-controller-manager, scheduler, api server, as well as those running on the working nodes such as the kubelet and kubeproxy is secured using TLS encryption.

![tls](../../images/tls.PNG)

## 4) Network Policies

- By default, all Pods can access each other within the cluster.
- Access between Pods can be restricted using **`Network Policies`**.

![np](../../images/np.PNG)

