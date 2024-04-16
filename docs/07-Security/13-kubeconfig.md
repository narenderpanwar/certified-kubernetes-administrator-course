# KubeConfig

- Take me to [Video Tutorial](https://kodekloud.com/topic/kubeconfig/)

In this section, we will take a look at kubeconfig in kubernetes

#### Client uses the certificate file and key to query the kubernetes Rest API for listing of pods using curl.

- You can specify the same using kubectl
  
  ![kc1](../../images/kc1.PNG)
- We can move these information to a configuration file called kubeconfig. And the specify this file as the kubeconfig option in the command.
  
  ```
  $ kubectl get pods --kubeconfig config
  ```
- Obviously, passing those key and certs as flags every time is a tedious task, so you move this information to a configuration file called as **`kubeconfig`**.

## Kubeconfig File

- The kubeconfig file has 3 sections
  
  - Clusters : This section contains information about the various Kubernetes clusters that you need access to.
  - Users : These are the user accounts with which you have access to these clusters.
    For example, the admin user, a dev user, a prod user, etc. These users may have different privileges on different clusters.
  - Contexts : Contexts define which user account will be used to access which cluster.
    
    ![kc4](../../images/kc4.PNG)
    So how does it fit into our example?
    The server specification in our command goes into the cluster section. The admin user's keys and certificates goes into the user section.
    You then create a context that specifies to use the my kube admin user to access the my kube playground cluster.
    
    ![kc5](../../images/kc5.PNG)
- To view the current kubeconfig file that is being used:
  
  ```
  $ kubectl config view
  ```
- To view the custom kubeconfig file that is being used and is at different location than $HOME/.kube/config
  
  ```
  $ kubectl config veiw --kubeconfig=my-custom-config
  ```
  
  ![kc6](../../images/kc6.PNG)
- How do you update your current context? Or change the current context
  
  ```
  $ kubectl config use-context prod-user@production
  ```
  
  ![kc7](../../images/kc7.PNG)
- kubectl config help
  
  ```
  $ kubectl config -h
  ```
  
  ![kc8](../../images/kc8.PNG)

## What about namespaces?

- Each cluster may be configured with multiple namespaces within it. So can you configure a context to switch to a particular namespace?
- Yes. The context section in the kubeconfig file can take additional field called namespace where you can specify a particular namespace. This way, when you switch to that context, you will automatically be in a specific namespace. Finally, a word on certificates.

![kc9](../../images/kc9.PNG)

## Certificates in kubeconfig

![kc10](../../images/kc10.PNG)

![kc12](../../images/kc12.PNG)

![kc11](../../images/kc11.PNG)

#### K8s Reference Docs

- https://kubernetes.io/docs/tasks/access-application-cluster/configure-access-multiple-clusters/
- https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#config

