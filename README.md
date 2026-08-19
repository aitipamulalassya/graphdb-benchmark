# GraphDB Benchmark

A comparative performance benchmark of five graph database systems using the Wiki-Vote dataset.

The project evaluates:

- CognoDB
- Neo4j
- Memgraph
- FalkorDB
- ArangoDB

The benchmark measures graph traversal, lookup, indexed lookup, and aggregation performance using P50 latency, P95 latency, and success rate.

---

## 1. Project Objective

The objective of this project is to compare the performance of different graph database systems using the same dataset and equivalent logical workloads.

The benchmark evaluates:

1. Query correctness
2. Data loading
3. Graph traversal latency
4. Point lookup latency
5. Indexed lookup latency
6. Aggregation latency
7. P50 latency
8. P95 latency
9. Success rate

---

## 2. Databases Evaluated

The following five graph database systems were benchmarked:

| Database | Evaluated |
|---|---|
| CognoDB | Yes |
| Neo4j | Yes |
| Memgraph | Yes |
| FalkorDB | Yes |
| ArangoDB | Yes |

---

## 3. Dataset

The benchmark uses the Wiki-Vote dataset.

### Dataset Statistics

| Metric | Count |
|---|---:|
| Nodes | 7,115 |
| Relationships | 103,689 |

The same prepared dataset was loaded into all five database systems.

### Prepared Data

```text
data/
└── prepared/
    ├── nodes.json
    ├── edges.json
    └── start_nodes.json
```

### Node Format

```json
{
    "user_id": 3,
    "group": 3
}
```

### Edge Format

```json
{
    "src": 30,
    "dst": 1412
}
```

---

## 4. Benchmark Operations

Six logical operations were tested.

### 4.1 1-Hop Traversal

Traverses the graph from a starting node through one relationship level.

### 4.2 2-Hop Traversal

Traverses the graph through two relationship levels.

### 4.3 3-Hop Traversal

Traverses the graph through three relationship levels.

### 4.4 Point Lookup

Retrieves a specific node using its user identifier.

### 4.5 Indexed Lookup

Retrieves nodes using the indexed `group` property.

### 4.6 Aggregation

Groups nodes by the `group` property and counts the nodes in each group.

---

## 5. Benchmark Configuration

| Parameter | Value |
|---|---:|
| Warm-up iterations | 5 |
| Measured iterations | 20 |
| Random seed | 20260819 |
| Start nodes | 100 |
| Metrics | P50, P95, Success Rate |

Five warm-up iterations were performed before the measured iterations.

---

## 6. Project Structure

```text
graphdb-benchmark/
│
├── benchmark/
│   ├── latency_cognodb.py
│   ├── latency_neo4j.py
│   ├── latency_memgraph.py
│   ├── latency_falkordb.py
│   ├── latency_arangodb.py
│   └── compare_results.py
│
├── connectors/
│   ├── cognodb.py
│   ├── neo4j.py
│   ├── memgraph.py
│   ├── falkordb.py
│   └── arangodb.py
│
├── data/
│   └── prepared/
│       ├── nodes.json
│       ├── edges.json
│       └── start_nodes.json
│
├── results/
│   ├── cognodb_latency.json
│   ├── neo4j_latency.json
│   ├── memgraph_latency.json
│   ├── falkordb_latency.json
│   ├── arangodb_latency.json
│   └── benchmark_comparison.json
│
├── test_cognodb_queries.py
├── test_neo4j_queries.py
├── test_memgraph.py
├── test_falkordb.py
├── test_arangodb_queries.py
│
├── load_cognodb.py
├── load_neo4j.py
├── load_memgraph.py
├── load_falkordb.py
├── load_arangodb.py
│
├── requirements.txt
├── README.md
└── report/
    └── graphdb_benchmark_report.pdf
```

---

# 7. Requirements

The project uses Python.

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate the virtual environment:

```powershell
.venv\Scripts\Activate.ps1
```

Install the required dependencies:

```powershell
pip install -r requirements.txt
```

---

# 8. Database Configuration

Each database requires its corresponding connection configuration.

The benchmark uses the respective database client/driver for each system.

Make sure the required database instances are running and accessible before executing the tests.

Do not commit:

- Passwords
- API keys
- Authentication tokens
- Private connection credentials
- Other secrets

Use environment variables or a local configuration file for sensitive values.

---

# 9. Data Loading

The general data loading workflow is:

```text
Connect to database
        ↓
Clear existing data
        ↓
Create collections / indexes
        ↓
Load 7,115 nodes
        ↓
Load 103,689 relationships
        ↓
Verify node count
        ↓
Verify relationship count
```

Each database was loaded with the same Wiki-Vote dataset.

---

# 10. CognoDB

Run the query validation:

```powershell
python test_cognodb_queries.py
```

Run the latency benchmark:

```powershell
python benchmark/latency_cognodb.py
```

### CognoDB Query Validation

Final validation produced:

```text
1-hop result: 23
2-hop result: 523
3-hop result: 20698
Point lookup result: 3
Indexed lookup result: 721
Aggregation: Successful
Write result: True
```

### CognoDB Benchmark

| Operation | P50 | P95 | Success |
|---|---:|---:|---:|
| 1-hop traversal | 307.743 ms | 374.291 ms | 20/20 |
| 2-hop traversal | 307.024 ms | 328.901 ms | 20/20 |
| 3-hop traversal | 307.343 ms | 1639.945 ms | 19/20 |
| Point lookup | 295.053 ms | 327.472 ms | 20/20 |
| Indexed lookup | 306.905 ms | 331.467 ms | 20/20 |
| Aggregation | 306.461 ms | 318.537 ms | 20/20 |

One 3-hop iteration experienced a transient connection failure. The driver attempted reconnection and the benchmark continued.

---

# 11. Neo4j

Run query validation:

```powershell
python test_neo4j_queries.py
```

Run the latency benchmark:

```powershell
python benchmark/latency_neo4j.py
```

### Neo4j Data Validation

```text
Nodes: 7,115
Relationships: 103,689
```

### Neo4j Benchmark

| Operation | P50 | P95 | Success |
|---|---:|---:|---:|
| 1-hop traversal | 86.491 ms | 98.599 ms | 20/20 |
| 2-hop traversal | 85.689 ms | 99.890 ms | 20/20 |
| 3-hop traversal | 85.276 ms | 112.568 ms | 20/20 |
| Point lookup | 85.148 ms | 103.394 ms | 20/20 |
| Indexed lookup | 84.526 ms | 105.560 ms | 20/20 |
| Aggregation | 92.921 ms | 113.143 ms | 20/20 |

---

# 12. Memgraph

Run the connection/query test:

```powershell
python test_memgraph.py
```

Run the latency benchmark:

```powershell
python benchmark/latency_memgraph.py
```

### Memgraph Data Validation

```text
Nodes: 7,115
Relationships: 103,689
```

### Memgraph Benchmark

| Operation | P50 | P95 | Success |
|---|---:|---:|---:|
| 1-hop traversal | 169.587 ms | 183.180 ms | 20/20 |
| 2-hop traversal | 205.669 ms | 207.192 ms | 20/20 |
| 3-hop traversal | 172.803 ms | 205.934 ms | 20/20 |
| Point lookup | 173.481 ms | 184.272 ms | 20/20 |
| Indexed lookup | 171.460 ms | 179.086 ms | 20/20 |
| Aggregation | 174.705 ms | 182.127 ms | 20/20 |

---

# 13. FalkorDB

Run the connection/query test:

```powershell
python test_falkordb.py
```

Run the latency benchmark:

```powershell
python benchmark/latency_falkordb.py
```

### FalkorDB Data Validation

```text
Nodes: 7,115
Relationships: 103,689
```

### FalkorDB Benchmark

| Operation | P50 | P95 | Success |
|---|---:|---:|---:|
| 1-hop traversal | 56.176 ms | 73.059 ms | 20/20 |
| 2-hop traversal | 56.887 ms | 70.260 ms | 20/20 |
| 3-hop traversal | 58.708 ms | 78.467 ms | 20/20 |
| Point lookup | 58.231 ms | 72.440 ms | 20/20 |
| Indexed lookup | 55.920 ms | 67.902 ms | 20/20 |
| Aggregation | 56.811 ms | 64.802 ms | 20/20 |

---

# 14. ArangoDB

Run query validation:

```powershell
python test_arangodb_queries.py
```

Run the latency benchmark:

```powershell
python benchmark/latency_arangodb.py
```

### ArangoDB Data Validation

```text
Nodes: 7,115
Relationships: 103,689
```

### ArangoDB Benchmark

| Operation | P50 | P95 | Success |
|---|---:|---:|---:|
| 1-hop traversal | 311.050 ms | 439.034 ms | 20/20 |
| 2-hop traversal | 345.912 ms | 412.411 ms | 20/20 |
| 3-hop traversal | 352.176 ms | 522.280 ms | 20/20 |
| Point lookup | 308.841 ms | 386.596 ms | 20/20 |
| Indexed lookup | 897.547 ms | 1039.788 ms | 20/20 |
| Aggregation | 335.664 ms | 379.947 ms | 20/20 |

---

# 15. Query Validation

Before latency benchmarking, the query implementations were tested.

Representative results:

| Operation | Result |
|---|---:|
| 1-hop traversal | 23 |
| 2-hop traversal | 523 |
| 3-hop traversal | 20,698 |
| Point lookup | 3 |
| Indexed lookup | 721 |
| Aggregation | Successful |
| Write | Successful |

The aggregation query produced the expected group counts.

The databases were therefore validated before running the latency benchmarks.

---

# 16. Running All Benchmarks

After the databases are configured and the data is loaded, run:

```powershell
python benchmark/latency_cognodb.py
```

```powershell
python benchmark/latency_neo4j.py
```

```powershell
python benchmark/latency_memgraph.py
```

```powershell
python benchmark/latency_falkordb.py
```

```powershell
python benchmark/latency_arangodb.py
```

Then generate the final comparison:

```powershell
python benchmark/compare_results.py
```

---

# 17. Final Comparison

## P50 Latency

Lower latency is better.

| Operation | CognoDB | Neo4j | Memgraph | FalkorDB | ArangoDB |
|---|---:|---:|---:|---:|---:|
| 1-hop traversal | 307.743 ms | 86.491 ms | 169.587 ms | **56.176 ms** | 311.050 ms |
| 2-hop traversal | 307.024 ms | 85.689 ms | 205.669 ms | **56.887 ms** | 345.912 ms |
| 3-hop traversal | 307.343 ms | 85.276 ms | 172.803 ms | **58.708 ms** | 352.176 ms |
| Point lookup | 295.053 ms | 85.148 ms | 173.481 ms | **58.231 ms** | 308.841 ms |
| Indexed lookup | 306.905 ms | 84.526 ms | 171.460 ms | **55.920 ms** | 897.547 ms |
| Aggregation | 306.461 ms | 92.921 ms | 174.705 ms | **56.811 ms** | 335.664 ms |

---

# 18. P95 Latency

| Operation | CognoDB | Neo4j | Memgraph | FalkorDB | ArangoDB |
|---|---:|---:|---:|---:|---:|
| 1-hop traversal | 374.291 ms | 98.599 ms | 183.180 ms | **73.059 ms** | 439.034 ms |
| 2-hop traversal | 328.901 ms | 99.890 ms | 207.192 ms | **70.260 ms** | 412.411 ms |
| 3-hop traversal | 1639.945 ms | 112.568 ms | 205.934 ms | **78.467 ms** | 522.280 ms |
| Point lookup | 327.472 ms | 103.394 ms | 184.272 ms | **72.440 ms** | 386.596 ms |
| Indexed lookup | 331.467 ms | 105.560 ms | 179.086 ms | **67.902 ms** | 1039.788 ms |
| Aggregation | 318.537 ms | 113.143 ms | 182.127 ms | **64.802 ms** | 379.947 ms |

---

# 19. Success Rate

| Operation | CognoDB | Neo4j | Memgraph | FalkorDB | ArangoDB |
|---|---:|---:|---:|---:|---:|
| 1-hop traversal | 100% | 100% | 100% | 100% | 100% |
| 2-hop traversal | 100% | 100% | 100% | 100% | 100% |
| 3-hop traversal | 95% | 100% | 100% | 100% | 100% |
| Point lookup | 100% | 100% | 100% | 100% | 100% |
| Indexed lookup | 100% | 100% | 100% | 100% | 100% |
| Aggregation | 100% | 100% | 100% | 100% | 100% |

---

# 20. Overall Ranking

The overall average P50 latency was calculated across the six operations.

| Rank | Database | Average P50 |
|---:|---|---:|
| 1 | **FalkorDB** | **57.122 ms** |
| 2 | **Neo4j** | **86.675 ms** |
| 3 | **Memgraph** | **177.951 ms** |
| 4 | **CognoDB** | **304.637 ms** |
| 5 | **ArangoDB** | **425.198 ms** |

Lower latency is better.

---

# 21. Fastest Database by Operation

| Operation | Fastest Database | P50 |
|---|---|---:|
| 1-hop traversal | **FalkorDB** | 56.176 ms |
| 2-hop traversal | **FalkorDB** | 56.887 ms |
| 3-hop traversal | **FalkorDB** | 58.708 ms |
| Point lookup | **FalkorDB** | 58.231 ms |
| Indexed lookup | **FalkorDB** | 55.920 ms |
| Aggregation | **FalkorDB** | 56.811 ms |

FalkorDB was the fastest database in all six tested operations.

---

# 22. Performance Analysis

## FalkorDB

FalkorDB achieved the best overall performance.

Its P50 latency remained between approximately 55.9 ms and 58.7 ms across all six operations.

It also achieved a 100% success rate for every benchmark operation.

## Neo4j

Neo4j was the second-fastest system.

Its P50 latency ranged from 84.526 ms to 92.921 ms.

All operations completed successfully.

## Memgraph

Memgraph achieved an overall average P50 latency of 177.951 ms.

All benchmark operations completed successfully.

## CognoDB

CognoDB achieved an overall average P50 latency of 304.637 ms.

Five operations achieved a 100% success rate.

One 3-hop iteration experienced a transient connection failure, resulting in a 95% success rate for that operation.

The 3-hop P95 latency was 1639.945 ms, which was substantially higher than its P50 latency.

## ArangoDB

ArangoDB achieved an overall average P50 latency of 425.198 ms.

Its indexed lookup operation had a comparatively high P50 latency of 897.547 ms and P95 latency of 1039.788 ms.

All benchmark operations completed successfully.

---



# 23. Limitations

The benchmark has the following limitations:

1. Only the Wiki-Vote dataset was evaluated.
2. Only six query workloads were tested.
3. Each operation used 20 measured iterations.
4. Five warm-up iterations were performed.
5. Network latency may affect the results because some database systems were hosted remotely.
6. Hardware and infrastructure configurations may differ between database deployments.
7. CPU utilization was not measured.
8. Memory consumption was not measured.
9. Storage consumption was not measured.
10. Throughput was not measured.
11. CognoDB experienced one transient connection failure during the 3-hop benchmark.
12. The results represent performance observed under this specific experimental environment and should not be interpreted as a universal ranking of graph databases.

---

# 24. Conclusion

Based on the benchmark results, FalkorDB achieved the best overall performance for the selected workload.

FalkorDB recorded the lowest P50 latency in all six tested operations:

- 1-hop traversal
- 2-hop traversal
- 3-hop traversal
- Point lookup
- Indexed lookup
- Aggregation

Its overall average P50 latency was:

**57.122 ms**

Neo4j was the second-fastest system with an overall average P50 latency of:

**86.675 ms**

FalkorDB also achieved a 100% success rate across all six operations.

Therefore, for the Wiki-Vote dataset, workload, benchmark configuration, and environment used in this project, **FalkorDB demonstrated the best overall latency performance among the five evaluated graph database systems.**

---

# 25. Result Files

The benchmark generates the following result files:

```text
results/
├── cognodb_latency.json
├── neo4j_latency.json
├── memgraph_latency.json
├── falkordb_latency.json
├── arangodb_latency.json
└── benchmark_comparison.json
```

The final combined comparison is stored in:

```text
results/benchmark_comparison.json
```

---

# 26. Reproducibility

To reproduce the benchmark:

### Step 1: Activate the virtual environment

```powershell
.venv\Scripts\Activate.ps1
```

### Step 2: Install dependencies

```powershell
pip install -r requirements.txt
```

### Step 3: Validate queries

```powershell
python test_cognodb_queries.py
python test_neo4j_queries.py
python test_memgraph.py
python test_falkordb.py
python test_arangodb_queries.py
```

### Step 4: Run latency benchmarks

```powershell
python benchmark/latency_cognodb.py
python benchmark/latency_neo4j.py
python benchmark/latency_memgraph.py
python benchmark/latency_falkordb.py
python benchmark/latency_arangodb.py
```

### Step 5: Generate final comparison

```powershell
python benchmark/compare_results.py
```

---

# 27. Final Result

## Winner: FalkorDB

**Overall Average P50: 57.122 ms**

**Fastest in 6 out of 6 operations**

**Success Rate: 100%**

Final ranking:

```text
1. FalkorDB   - 57.122 ms
2. Neo4j      - 86.675 ms
3. Memgraph   - 177.951 ms
4. CognoDB    - 304.637 ms
5. ArangoDB   - 425.198 ms
```

---

- [x] Final comparison generated
- [x] LaTeX report prepared
- [x] README prepared
