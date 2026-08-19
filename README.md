# Graph Database Performance Benchmark

A comparative performance benchmark of five graph database systems using the Wiki-Vote dataset and a common set of graph workloads.

## Databases Evaluated

The benchmark evaluates:

1. CognoDB
2. Neo4j
3. Memgraph
4. FalkorDB
5. ArangoDB

The objective is to compare latency and reliability across equivalent logical workloads.

---

## Dataset

The benchmark uses the Wiki-Vote dataset.

| Metric | Count |
|---|---:|
| Nodes | 7,115 |
| Relationships | 103,689 |

The same prepared dataset was loaded into all five database systems.

Prepared data:

```text
data/
└── prepared/
    ├── nodes.json
    ├── edges.json
    └── start_nodes.json