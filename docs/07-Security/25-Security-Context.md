## Docker Security

* **User Permissions:** By default, containers run as the `root` user. This can be insecure. We can specify a non-root user to run the container process or set the user in the Docker image itself.
* **Capabilities:** Even with a non-root user, capabilities can be granted to provide specific privileges. By default, Docker limits these capabilities but we can further restrict or grant additional capabilities using the `cap-add` and `cap-drop` options in the `docker run` command.
  
  ```
  $ docker run --user=1001 ubuntu sleep 3600
  $ docker run -cap-add MAC_ADMIN ubuntu
  ```
  
  ![csec](../../images/csec.PNG)

## Security Context in Kubernetes

- Similar to Docker containers, Kubernetes pods allow you to define security configurations for processes running within them such as the ID of the user used to run the container, the Linux capabilities that can be added or removed from the container etc.
- There are two ways to configure security context in Kubernetes pods:
  
  * **Pod Level:** Security context settings defined at the pod level apply to all containers within that pod.
  * **Container Level:** Security context settings can be further specified for individual containers within a pod. In this case, container-level settings override any conflicting settings defined at the pod level.
- To add security context on the container add a field called **`securityContext`** under the spec section.
  
  ```
  apiVersion: v1
  kind: Pod
  metadata:
    name: web-pod
  spec:
    securityContext:
      runAsUser: 1000
    containers:
    - name: ubuntu
      image: ubuntu
      command: ["sleep", "3600"]
  ```
  
  ![sxc1](../../images/sxc1.PNG)
- To set the same context at the container level, then move the whole section under container section.
  
  ```
  apiVersion: v1
  kind: Pod
  metadata:
    name: web-pod
  spec:
    containers:
    - name: ubuntu
      image: ubuntu
      command: ["sleep", "3600"]
      securityContext:
        runAsUser: 1000
  ```
  
  ![sxc2](../../images/sxc2.PNG)
- To add capabilities use the **`capabilities`** option
  
  ```
  apiVersion: v1
  kind: Pod
  metadata:
    name: web-pod
  spec:
    containers:
    - name: ubuntu
      image: ubuntu
      command: ["sleep", "3600"]
      securityContext:
        runAsUser: 1000
        capabilities: 
          add: ["MAC_ADMIN"]
  ```
  
  ![cap](../../images/cap.PNG)

### K8s Reference Docs

- https://kubernetes.io/docs/tasks/configure-pod-container/security-context/

