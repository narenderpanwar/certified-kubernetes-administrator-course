# ETCD in HA

## What is etcd?

- etcd is a distributed key-value store that offers high availability, reliability, and security. It's designed to store and retrieve data in a simple and fast way. Here's a breakdown of its key features:
  
  * **Distributed:** Data is stored across multiple servers, ensuring redundancy and fault tolerance. Even if one server fails, the data remains accessible.
  * **Reliable:** etcd uses the Raft consensus algorithm to guarantee data consistency across all servers. This means that writes are replicated and agreed upon by the majority of nodes before being committed.
  * **Secure:** etcd supports secure communication using Transport Layer Security (TLS) and optional client certificate authentication.

## Stepping into the Cluster

- A single etcd server might be okay for basic scenarios, but for critical data, distribution is key.
- This is where etcd clusters come in.
- You can have multiple etcd servers running together, each maintaining an identical copy of the data. This redundancy ensures that even if one server fails, the data remains available on the others.

## Maintaining Consistency: The Role of Raft

- With reads, it's easy. Since the same data is available across all nodes, you can easily read it from any nodes.
- But that is not the case with writes. What if two writes requests coming on two different instances? Which one goes through?
- For example, I have writes coming in for the name set to John on one end, with the name Joe on the other. Of course, we cannot have two different data on two different nodes.
- But how do we ensure all servers in the cluster have the same data?
- This is where the Raft consensus algorithm comes into play. Raft works by electing a leader node among the servers. The leader is responsible for processing write requests and replicating them to all followers (other servers in the cluster).

  Here's a simplified example of how Raft works in a three-node cluster:

1. **Leader Election:** Initially, there's no leader. Each server initiates a random timer. The first server to finish its timer becomes the leader and informs the others.
2. **Write Requests:** When a client wants to write data, it sends the request to any server.
   * If it reaches the leader, the leader processes the write and replicates it to the followers.
   * If it reaches a follower, the follower forwards the request to the leader, who then performs the replication process.
3. **Consistency:** The write is only considered successful once the leader replicates it to a majority of the servers (quorum). This ensures that all servers have the latest data version.

## Leader Failure and Re-election

- The leader plays a crucial role, but what happens if it fails? Raft handles this by triggering a re-election process among the remaining nodes. A new leader is then elected, and the cluster continues to operate without interruption.

## Quorum: The Key to Availability

- For a cluster to function correctly and process writes, a minimum number of servers need to be available.
- This minimum number is called the quorum. In etcd, the quorum is calculated as the total number of nodes divided by 2 plus 1.
- For example, in a three-node cluster, the quorum is 2 (as 3/2 + 1 = 2). This means that even if one node fails, the remaining two nodes can still form a quorum and process writes.

## Why Odd is Better Than Even

Having an odd number of servers in your etcd cluster is generally recommended. Here's why:

* **Network Partitioning:** Imagine a network issue that splits the cluster into two partitions, each with an equal number of nodes (e.g., a four-node cluster split into two groups of two). In this scenario, neither partition would have a quorum, making the cluster unavailable.
* **Tiebreaker:** With an odd number of nodes, there's always a clear majority during leader election, avoiding potential ties.

## Choosing the Right Cluster Size

- The ideal number of servers in your etcd cluster depends on your specific needs. Here's a breakdown to consider:
  
  * **Minimum for HA (High Availability):** Three nodes is the minimum required for a highly available cluster. This ensures that even if one node fails, the cluster remains operational.
  * **Balancing Fault Tolerance and Cost:** Five nodes offer a higher level of fault tolerance compared to three. However, with more nodes comes increased cost and complexity.
  * **Beyond Five: Not Always Necessary** Generally, a cluster with five nodes provides sufficient fault tolerance for most deployments. Adding more nodes beyond that might not offer significant benefits.
  
  Ultimately, the choice depends on your environment's fault tolerance requirements and resource constraints.

