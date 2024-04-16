# OS Upgrades

- The lecture begins by highlighting scenarios where you might need to take down nodes in your cluster for maintenance purposes, such as upgrading base software or applying patches like security updates.

1. ​**Impact of Node Downtime on Pods**​:
   
   - When a node goes down, the pods running on that node become inaccessible. Depending on how the pods were deployed, user access to applications may be impacted.
   - For example, if there are multiple replicas of a pod, users accessing the application served by those replicas might not be affected, whereas if there's only one instance of a pod, users accessing that application would be impacted.
     
     ![os](../../images/os.png)
2. ​**Handling Node Downtime in Kubernetes**​:
   
   * If a node comes back online immediately, the kubelet process starts, and the pods on that node come back online as well.
   * If the node was down for more than 5 minutes, Kubernetes considers the pods on that node as dead, and they are terminated. This time limit is known as the "pod-eviction-timeout" and has a default value of five minutes, set on the controller manager.
     
     ![os](../../images/os1.png)
3. ​**Recovery Process for Pods**​:
   
   * If the pods were part of a replica set, they are recreated on other nodes after being terminated.
   * If a node comes back online after the pod-eviction-timeout, it comes up empty without any pods scheduled on it.
     
     ![os](../../images/os2.png)
4. ​**Maintenance Strategies**​:
   
   * If you have maintenance tasks to perform on a node, and you are certain it will be back online within 5 minutes, and the workloads have replicas and can afford downtime, you can quickly upgrade and reboot the node.
   * `A safer approach is to drain the node of all workloads, which gracefully terminates the pods and recreates them on other nodes in the cluster. The node is also cordoned or marked as unschedulable to prevent new pods from being scheduled on it until the maintenance is complete.`
5. **Drain and Uncordon Commands**:
   
   * `drain`: This command gracefully terminates the pods on the node and moves them to other nodes in the cluster. It also marks the node as unschedulable.
     
     ```
     kubectl drain node01
     ```
   * `uncordon`: This command removes the unschedulable mark from a node, allowing pods to be scheduled on it again. When the node is back online after maintenance, it is still unschedulable. You then need to uncordon it.
     
     ```
     kubectl uncordon node01
     ```
   * `cordon`: This command marks a node as unschedulable, but unlike `drain`, it does not terminate or move existing pods.
     
     ```
     kubectl cordon node01
     ```




