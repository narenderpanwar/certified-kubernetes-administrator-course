# Pods

- Take me to [Video Tutorial](https://kodekloud.com/topic/pods-2/)

In this section, we will take a look at PODS.

- POD introduction
- How to deploy pod?

#### Kubernetes doesn't deploy containers directly on the worker node but into a Kubernetes object called a Pod.

#### A Pod Manisfest yaml is nothing but a running definition fo a Docker container.

![pod](../../images/pod.PNG)

#### Here is a single node kubernetes cluster with single instance of your application running in a single docker container encapsulated in the pod.

![pod1](../../images/pod1.PNG)

#### Pod will have a one-to-one relationship with containers running your application.

![pod2](../../images/pod2.PNG)

## Multi-Container PODs

- A single pod can have multiple containers except for the fact that they are usually not multiple containers of the **`same kind`**.
- Both the containers share the same volume or storage and network, hence they can communicate using localhost.
  
  ![pod3](../../images/pod3.PNG)

## Docker Example (Docker Link)

![pod4](../../images/pod4.PNG)

## How to deploy pods?

Lets now take a look to create a nginx pod using **`kubectl`**.

- To deploy a docker container by creating a POD.
  
  ```
  $ kubectl run nginx --image nginx
  ```
- To get the list of pods
  
  ```
  $ kubectl get pods
  ```

What does the `READY` column in the output of the `kubectl get pods` command indicate?

```
Number of running containers in Pod/Total number of containers in Pod
```

![kubectl](../../images/kubectl.PNG)

K8s Reference Docs:

- https://kubernetes.io/docs/concepts/workloads/pods/pod/
- https://kubernetes.io/docs/concepts/workloads/pods/pod-overview/
- https://kubernetes.io/docs/tutorials/kubernetes-basics/explore/explore-intro/

