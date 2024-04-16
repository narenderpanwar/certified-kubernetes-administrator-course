# ETCD for Beginners

- Take me to the [Video Tutorial](https://kodekloud.com/topic/etcd-for-beginners/)

In this section, we will take a quick look at introduction to ETCD for beginners.

- What is ETCD?
- What is a Key-Value Store?
- How to get started quickly with ETCD?
- How to operate ETCD?

## What is ETCD?

- ETCD is a distributed reliable key-value store that is simple, secure & Fast. It stores the information about the whole cluster as shown below:

```json
{
  "/registry/nodes/node1.example.com": {
    "metadata": {
      "name": "node1.example.com",
      "labels": {
        "role": "worker",
        "zone": "us-west1-a"
      }
    },
    "spec": {
      "capacity": {
        "cpu": "4",
        "memory": "16Gi"
      },
      "addresses": [
        {
          "type": "InternalIP",
          "address": "10.240.0.3"
        },
        {
          "type": "ExternalIP",
          "address": "203.0.113.1"
        }
      ]
    },
    "status": {
      "conditions": [
        {
          "type": "Ready",
          "status": "True",
          "lastHeartbeatTime": "2024-02-29T12:00:00Z"
        }
      ],
      "allocatable": {
        "cpu": "3",
        "memory": "14Gi"
      }
    }
  },
  "/registry/pods/default/my-pod": {
    "metadata": {
      "name": "my-pod",
      "namespace": "default",
      "labels": {
        "app": "nginx"
      }
    },
    "spec": {
      "containers": [
        {
          "name": "nginx",
          "image": "nginx:latest",
          "ports": [
            {
              "containerPort": 80,
              "protocol": "TCP"
            }
          ]
        }
      ]
    },
    "status": {
      "phase": "Running",
      "podIP": "10.240.1.5",
      "startTime": "2024-02-29T12:05:00Z"
    }
  },
  "/registry/services/default/my-service": {
    "metadata": {
      "name": "my-service",
      "namespace": "default"
    },
    "spec": {
      "selector": {
        "app": "nginx"
      },
      "ports": [
        {
          "protocol": "TCP",
          "port": 80,
          "targetPort": 80
        }
      ]
    }
  }
}

```

## What is a Key-Value Store

- Traditionally, databases have been in tabular format, you must have heared about SQL or Relational databases. They store data in rows and columns

  ![relational-dbs](../../images/relational-dbs.PNG)
- A Key-Value Store stores information in a Key and Value format.

  ![key-value](../../images/key-value.PNG)

## Install ETCD

- Its easy to install and get started with **`ETCD`**.

  - Download the relevant binary for your operating system from github releases page (https://github.com/etcd-io/etcd/releases)

    For Example: To download ETCD v3.5.6, run the below curl command

    ```
    $ curl -LO https://github.com/etcd-io/etcd/releases/download/v3.5.6/etcd-v3.5.6-linux-amd64.tar.gz
    ```
  - Extract it.

    ```
    $ tar xvzf etcd-v3.5.6-linux-amd64.tar.gz
    ```
  - Run the ETCD Service

    ```
    $ ./etcd
    ```
  - When you start **`ETCD`** it will by default listens on port **`2379`**
  - The default client that comes with **`ETCD`** is the [**`etcdctl`**](https://github.com/etcd-io/etcd/tree/main/etcdctl) client. You can use it to store and retrieve key-value pairs.

    ```
    Syntax: To Store a Key-Value pair
    $ ./etcdctl put key1 value1
    ```
    ```
    Syntax: To retrieve the stored data
    $ ./etcdctl get key1
    ```
    ```
    Syntax: To view more commands. Run etcdctl without any arguments
    $ ./etcdctl
    ```
    ![etcdctl](../../images/etcdctl.PNG)

  K8s Reference Docs:

  - https://kubernetes.io/docs/concepts/overview/components/
  - https://etcd.io/docs/
  - https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/
