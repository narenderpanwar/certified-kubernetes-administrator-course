# Namespaces

- Take me to [Video Tutorial](https://kodekloud.com/topic/namespaces/)

So far in this course we have created **`Objects`** such as **`PODs`**, **`Deployments`** and **`Services`** in our cluster. Whatever we have been doing we have been doing in a **`NAMESPACE`**.

- This namespace is the **`default`** namespace in kubernetes. It is automatically created when kubernetes is setup initially.
  
  ![ns](../../images/ns.PNG)
- You can create your own namespaces as well.
  
  ![ns3](../../images/ns3.PNG)
- To list the pods in default namespace
  
  ```
  $ kubectl get pods
  ```
- To list the pods in another namespace. Use **`kubectl get pods`** command along with the **`--namespace`** flag or argument.
  
  ```
  $ kubectl get pods --namespace=kube-system
  ```
  
  ![ns8](../../images/ns8.PNG)


```
$ kubectl create -f pod-definition.yaml
```

- To create the pod with the pod-definition file in another namespace, use the **`--namespace`** option.
  
  ```
  $ kubectl create -f pod-definition.yaml --namespace=dev
  ```
  
  ![ns9](../../images/ns9.PNG)
- If you want to make sure that this pod gets you created in the **`dev`** env all the time, even if you don't specify in the command line, you can move the **`--namespace`** definition into the pod-definition file.

```
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
  namespace: dev
  labels:
     app: myapp
     type: front-end
spec:
  containers:
  - name: nginx-container
    image: nginx
```


- To create a new namespace, create a namespace definition as shown below and then run **`kubectl create`**

```
apiVersion: v1
kind: Namespace
metadata:
  name: dev
```

```
$ kubectl create -f namespace-dev.yaml
```

Another way to create a namespace

```
$ kubectl create namespace dev
```

-----------------------

What if a frontend pod in `dev` namespace needs to communicate with a backend pod in another namespace say `prod`?

- We can use Kubernetes DNS-based service discovery to access services across namespaces. When you create a service for the backend pod, you can access it from the frontend pod using the service name as a DNS entry.
- For example, if your backend service is named `backend-svc`in the`prod`namespace, the frontend pod can access it using`backend-svc.prod.svc.cluster.local`.

----------------------

![ns11](../../images/ns11.PNG)

- By default, we will be in a **`default`** namespace. To switch to a particular namespace permenently run the below command.
  
  ```
  $ kubectl config set-context $(kubectl config current-context) --namespace=dev
  ```
- To view pods in all namespaces
  
  ```
  $ kubectl get pods --all-namespaces
  ```
  
  ![ns12](../../images/ns12.PNG)
- To limit resources in a namespace, create a resource quota. To create one start with **`ResourceQuota`** definition file.

```
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-quota
  namespace: dev
spec:
  hard:
    pods: "10"
    requests.cpu: "4"
    requests.memory: 5Gi
    limits.cpu: "10"
    limits.memory: 10Gi
```

```
$ kubectl create -f compute-quota.yaml
```


![ns13](../../images/ns13.PNG)

K8s Reference Docs:

- https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/
- https://kubernetes.io/docs/tasks/administer-cluster/namespaces-walkthrough/
- https://kubernetes.io/docs/tasks/administer-cluster/namespaces/
- https://kubernetes.io/docs/tasks/administer-cluster/manage-resources/quota-memory-cpu-namespace/
- https://kubernetes.io/docs/tasks/access-application-cluster/list-all-running-container-images/

