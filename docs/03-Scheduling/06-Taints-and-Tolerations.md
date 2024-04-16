# Taints and Tolerations

- Take me to [Video Tutorial](https://kodekloud.com/topic/taints-and-tolerations-2/)

In this section, we will take a look at taints and tolerations.

- Pod to node relationship and how you can restrict what pods are placed on what nodes.

#### Taints and Tolerations are used to set restrictions on what pods can be scheduled on a node.

- Only pods which are tolerant to the particular taint on a node will get scheduled on that node.
  
  ![tandt](../../images/tandt.PNG)

## Taints

- Use **`kubectl taint nodes`** command to taint a node.
  
  Syntax
  
  ```
  $ kubectl taint nodes <node-name> key=value:taint-effect
  ```
  
  Example
  
  ```
  $ kubectl taint nodes node1 app=blue:NoSchedule
  ```
- The taint-effect explains what would happen to Pods that do not tolerate the taint.
- There are 3 taint effects
  
  - **`NoSchedule`** : When a node has a taint with the "NoSchedule" effect, it means that pods without a matching toleration will not be scheduled to run on that node. Essentially, it tells Kubernetes not to place any pods on that node unless they specifically tolerate the taint.
  - **`PreferNoSchedule`**: This effect is similar to "NoSchedule," but it's a softer restriction. Pods without a matching toleration will still be scheduled on the node, but Kubernetes will try to avoid doing so if possible. It's a preference rather than a hard rule.
  - **`NoExecute`** : This effect is a bit different. When a node has a taint with the "NoExecute" effect, it means that any existing pods on that node that don't tolerate the taint will be evicted (removed) from the node.

  ![tn](../../images/tn.PNG)

## Tolerations

- Tolerations are added to pods by adding a **`tolerations`** section in pod definition.
  ```
  apiVersion: v1
  kind: Pod
  metadata:
   name: myapp-pod
  spec:
   containers:
   - name: nginx-container
     image: nginx
   tolerations:
   - key: "app"
     operator: "Equal"
     value: "blue"
     effect: "NoSchedule"
  ```

  ![tp](../../images/tp.PNG)

#### Taints and Tolerations do not tell the pod to go to a particular node. Instead, they tell the node to only accept pods with certain tolerations. Hence, it is possible that the pod with toleration can go to any of the Nodes available.

---

A scheduler does not schedule any pods on the master node.

This is because, when the Kubernetes cluster is first set up, a taint is set on the master node automatically that prevents any pods from being scheduled on this node.

- To see this taint, run the below command
  ```
  $ kubectl describe node kubemaster |grep Taint
  ```

---

![tntm](../../images/tntm.PNG)

#### K8s Reference Docs

- https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/

