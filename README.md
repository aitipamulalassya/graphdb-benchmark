# GraphDB Benchmark

A comparative performance benchmark of five graph database systems using the Wiki-Vote dataset.

## 1. Databases Tested

- CognoDB
- Neo4j
- Memgraph
- FalkorDB
- ArangoDB

## 2. Dataset

The benchmark uses the **Wiki-Vote** dataset.

| Metric | Value |
|---|---:|
| Nodes | 7,115 |
| Relationships | 103,689 |

The same dataset was loaded into all five database systems.

### Dataset Files

```text
data/
└── prepared/
    ├── nodes.json
    ├── edges.json
    └── start_nodes.json
```

Example node:

```json
{
  "user_id": 3,
  "group": 3
}
```

Example relationship:

```json
{
  "src": 30,
  "dst": 1412
}
```

---

## 3. Benchmark Operations

The following six operations were evaluated:

1. 1-hop traversal
2. 2-hop traversal
3. 3-hop traversal
4. Point lookup
5. Indexed lookup
6. Aggregation

### 1-Hop Traversal

Traverses the graph from a starting node through one relationship level.

### 2-Hop Traversal

Traverses the graph through two relationship levels.

### 3-Hop Traversal

Traverses the graph through three relationship levels.

### Point Lookup

Retrieves a specific node using its `user_id`.

### Indexed Lookup

Retrieves nodes using the indexed `group` property.

### Aggregation

Groups nodes by `group` and counts the nodes in each group.

---

## 4. Benchmark Methodology

The same prepared dataset and equivalent logical workloads were used for all databases.

### Configuration

| Parameter | Value |
|---|---:|
| Warm-up iterations | 5 |
| Measured iterations | 20 |
| Random seed | 20260819 |
| Start nodes | 100 |
| Metrics | P50, P95, Success Rate |

Five warm-up iterations were executed before the measured iterations.

### Metrics

**P50 latency** is the median query latency.

**P95 latency** represents the tail latency at the 95th percentile.

**Success Rate** is calculated as:

```text
Successful iterations / Total iterations × 100
```

Lower latency is better.

Higher success rate is better.

---

## 5. Environment

The benchmark was executed using:

| Environment | Value |
|---|---|
| Operating System | Windows |
| Python | 3.12 |
| Environment | Python virtual environment |
| Dataset | Wiki-Vote |
| Nodes | 7,115 |
| Relationships | 103,689 |

The databases were accessed using their respective Python client libraries/drivers.

Some database instances were hosted remotely. Therefore, measured latency includes network communication between the benchmark machine and the database instance.

### Deployment

| Database | Deployment |
|---|---|
| CognoDB | Remote/free-tier instance |
| Neo4j | Remote/free-tier instance |
| Memgraph | Remote/free-tier instance |
| FalkorDB | Remote/free-tier instance |
| ArangoDB | Remote/free-tier instance |

> Exact CPU and RAM specifications were not consistently available across all free-tier deployments. Therefore, the results should be interpreted as an application-level latency comparison rather than a controlled hardware benchmark.

---

## 6. Requirements

- Python 3.12
- Internet connection
- Database accounts/access
- Database connection credentials

---

## 7. Installation

Clone the repository:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd <YOUR_REPOSITORY_DIRECTORY>
```

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

---

## 8. Database Configuration

Configure the database connection details in a local `.env` file.

Example:

```text
COGNODB_URI=...
COGNODB_USERNAME=...
COGNODB_PASSWORD=...

NEO4J_URI=...
NEO4J_USERNAME=...
NEO4J_PASSWORD=...
NEO4J_DATABASE=...

MEMGRAPH_URI=...
MEMGRAPH_USERNAME=...
MEMGRAPH_PASSWORD=...

FALKORDB_HOST=...
FALKORDB_PORT=...
FALKORDB_USERNAME=...
FALKORDB_PASSWORD=...

ARANGODB_HOST=...
ARANGODB_DATABASE=...
ARANGODB_USERNAME=...
ARANGODB_PASSWORD=...
```

Do not commit credentials or secrets to GitHub.

Add `.env` to `.gitignore`:

```text
.env
.venv/
__pycache__/
```

---

## 9. Project Structure

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
└── README.md
```

---

# 10. Data Loading

Each database can be populated using its corresponding loader.

### CognoDB

```powershell
python load_cognodb.py
```

### Neo4j

```powershell
python load_neo4j.py
```

### Memgraph

```powershell
python load_memgraph.py
```

### FalkorDB

```powershell
python load_falkordb.py
```

### ArangoDB

```powershell
python load_arangodb.py
```

Each loader:

1. Connects to the database.
2. Clears existing benchmark data.
3. Creates required indexes/collections.
4. Loads 7,115 nodes.
5. Loads 103,689 relationships.
6. Verifies the loaded data.

Expected dataset size:

```text
Nodes: 7,115
Relationships: 103,689
```

---

# 11. Query Validation

Before running latency benchmarks, validate the database queries.

### CognoDB

```powershell
python test_cognodb_queries.py
```

### Neo4j

```powershell
python test_neo4j_queries.py
```

### Memgraph

```powershell
python test_memgraph.py
```

### FalkorDB

```powershell
python test_falkordb.py
```

### ArangoDB

```powershell
python test_arangodb_queries.py
```

The validation tests cover:

- 1-hop traversal
- 2-hop traversal
- 3-hop traversal
- Point lookup
- Indexed lookup
- Aggregation
- Write operation

This ensures that the data and queries are working before measuring latency.

---

# 12. Running the Benchmarks

Run the latency benchmark for each database.

### CognoDB

```powershell
python benchmark/latency_cognodb.py
```

### Neo4j

```powershell
python benchmark/latency_neo4j.py
```

### Memgraph

```powershell
python benchmark/latency_memgraph.py
```

### FalkorDB

```powershell
python benchmark/latency_falkordb.py
```

### ArangoDB

```powershell
python benchmark/latency_arangodb.py
```

Each benchmark performs:

```text
Connect
   ↓
Select start nodes
   ↓
5 warm-up iterations
   ↓
20 measured iterations
   ↓
Calculate P50
   ↓
Calculate P95
   ↓
Calculate success rate
   ↓
Save JSON results
```

---

# 13. Generate Final Comparison

After all five benchmarks have completed:

```powershell
python benchmark/compare_results.py
```

The combined results are saved to:

```text
results/benchmark_comparison.json
```

---

# 14. Complete Results

## 14.1 P50 Latency

Lower is better.

All values are in milliseconds.

| Operation | CognoDB | Neo4j | Memgraph | FalkorDB | ArangoDB |
|---|---:|---:|---:|---:|---:|
| 1-hop traversal | 307.743 | 86.491 | 169.587 | **56.176** | 311.050 |
| 2-hop traversal | 307.024 | 85.689 | 205.669 | **56.887** | 345.912 |
| 3-hop traversal | 307.343 | 85.276 | 172.803 | **58.708** | 352.176 |
| Point lookup | 295.053 | 85.148 | 173.481 | **58.231** | 308.841 |
| Indexed lookup | 306.905 | 84.526 | 171.460 | **55.920** | 897.547 |
| Aggregation | 306.461 | 92.921 | 174.705 | **56.811** | 335.664 |

---

## 14.2 P95 Latency

Lower is better.

All values are in milliseconds.

| Operation | CognoDB | Neo4j | Memgraph | FalkorDB | ArangoDB |
|---|---:|---:|---:|---:|---:|
| 1-hop traversal | 374.291 | 98.599 | 183.180 | **73.059** | 439.034 |
| 2-hop traversal | 328.901 | 99.890 | 207.192 | **70.260** | 412.411 |
| 3-hop traversal | 1639.945 | 112.568 | 205.934 | **78.467** | 522.280 |
| Point lookup | 327.472 | 103.394 | 184.272 | **72.440** | 386.596 |
| Indexed lookup | 331.467 | 105.560 | 179.086 | **67.902** | 1039.788 |
| Aggregation | 318.537 | 113.143 | 182.127 | **64.802** | 379.947 |

---

## 14.3 Success Rate

Higher is better.

| Operation | CognoDB | Neo4j | Memgraph | FalkorDB | ArangoDB |
|---|---:|---:|---:|---:|---:|
| 1-hop traversal | 100% | 100% | 100% | 100% | 100% |
| 2-hop traversal | 100% | 100% | 100% | 100% | 100% |
| 3-hop traversal | 95% | 100% | 100% | 100% | 100% |
| Point lookup | 100% | 100% | 100% | 100% | 100% |
| Indexed lookup | 100% | 100% | 100% | 100% | 100% |
| Aggregation | 100% | 100% | 100% | 100% | 100% |

---

# 15. Overall Average P50

The overall average is calculated across the six benchmark operations.

| Rank | Database | Average P50 |
|---:|---|---:|
| 1 | **FalkorDB** | **57.122 ms** |
| 2 | Neo4j | 86.675 ms |
| 3 | Memgraph | 177.951 ms |
| 4 | CognoDB | 304.637 ms |
| 5 | ArangoDB | 425.198 ms |

---

# 16. Fastest Database by Operation

| Operation | Fastest Database | P50 |
|---|---|---:|
| 1-hop traversal | **FalkorDB** | 56.176 ms |
| 2-hop traversal | **FalkorDB** | 56.887 ms |
| 3-hop traversal | **FalkorDB** | 58.708 ms |
| Point lookup | **FalkorDB** | 58.231 ms |
| Indexed lookup | **FalkorDB** | 55.920 ms |
| Aggregation | **FalkorDB** | 56.811 ms |

FalkorDB was the fastest database for all six operations.

---

# 17. Analysis

### FalkorDB

FalkorDB achieved the best overall performance.

Its P50 latency remained between approximately 55.9 ms and 58.7 ms across all six operations.

It also achieved a 100% success rate for every operation.

### Neo4j

Neo4j was the second-fastest database.

Its P50 latency ranged from 84.526 ms to 92.921 ms, with a 100% success rate across all operations.

### Memgraph

Memgraph achieved an overall average P50 latency of 177.951 ms.

All six operations completed successfully.

### CognoDB

CognoDB achieved an overall average P50 latency of 304.637 ms.

Five operations achieved a 100% success rate.

One 3-hop iteration experienced a transient connection failure, resulting in a 95% success rate for that operation.

The 3-hop P95 latency was 1639.945 ms, which was significantly higher than its P50 latency.

### ArangoDB

ArangoDB achieved an overall average P50 latency of 425.198 ms.

Indexed lookup was its slowest operation:

| Metric | Value |
|---|---:|
| P50 | 897.547 ms |
| P95 | 1039.788 ms |

All six operations completed successfully.

---

# 18. Key Findings

- **FalkorDB was the fastest database in all six operations.**
- FalkorDB achieved the lowest overall average P50 latency of **57.122 ms**.
- Neo4j ranked second with **86.675 ms**.
- Memgraph ranked third with **177.951 ms**.
- CognoDB ranked fourth with **304.637 ms**.
- ArangoDB ranked fifth with **425.198 ms**.
- All databases achieved 100% success for 1-hop traversal.
- All databases achieved 100% success for 2-hop traversal.
- CognoDB had one transient failure during the 3-hop benchmark.
- ArangoDB had the highest indexed lookup latency.
- FalkorDB showed the most consistent latency across the tested operations.

---

# 19. Caveats

- Only the Wiki-Vote dataset was evaluated.
- Only six query workloads were tested.
- Each operation used 20 measured iterations.
- Five warm-up iterations were performed.
- Some database instances were hosted remotely.
- Network latency may affect the measured results.
- Hardware and instance configurations were not identical across all platforms.
- CPU, memory, storage usage, and throughput were not measured.
- CognoDB experienced one transient connection failure during 3-hop traversal.
- The results represent the tested environment and should not be considered a universal ranking of graph databases.

---

# 20. Result Files

```text
results/
├── cognodb_latency.json
├── neo4j_latency.json
├── memgraph_latency.json
├── falkordb_latency.json
├── arangodb_latency.json
└── benchmark_comparison.json
```

---

# 21. Conclusion

For the Wiki-Vote dataset and benchmark configuration used in this project, **FalkorDB demonstrated the best overall latency performance**.

### Final Ranking

```text
1. FalkorDB  - 57.122 ms
2. Neo4j     - 86.675 ms
3. Memgraph  - 177.951 ms
4. CognoDB   - 304.637 ms
5. ArangoDB  - 425.198 ms
```

FalkorDB achieved:

- **57.122 ms overall average P50**
- **100% success rate**
- **6/6 fastest operations**

Therefore, FalkorDB was the best-performing database in this benchmark under the tested environment and workload.
