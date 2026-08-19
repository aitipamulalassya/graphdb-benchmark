import json
import random
import statistics
import sys
import time
from pathlib import Path


# ======================================
# PROJECT ROOT
# ======================================

ROOT = (
    Path(__file__)
    .resolve()
    .parent.parent
)

sys.path.insert(
    0,
    str(ROOT)
)


# ======================================
# IMPORT
# ======================================

from connectors.arangodb import ArangoDBAdapter


# ======================================
# CONFIGURATION
# ======================================

MEASURED_ITERATIONS = 20
WARMUP_ITERATIONS = 5
RANDOM_SEED = 20260819

NODES_FILE = (
    ROOT
    / "data"
    / "prepared"
    / "nodes.json"
)

RESULTS_DIR = (
    ROOT
    / "results"
)

RESULTS_FILE = (
    RESULTS_DIR
    / "arangodb_latency.json"
)


# ======================================
# LOAD START NODES
# ======================================

def load_start_nodes():

    with open(
        NODES_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        nodes = json.load(file)


    node_ids = [
        int(node["user_id"])
        for node in nodes
    ]


    random.seed(
        RANDOM_SEED
    )


    start_nodes = random.sample(
        node_ids,
        min(
            100,
            len(node_ids)
        )
    )


    return start_nodes


# ======================================
# MEASURE ONE QUERY
# ======================================

def measure_query(
    database,
    operation,
    params
):

    start = time.perf_counter()


    try:

        database.run(
            operation,
            params
        )

        end = time.perf_counter()

        latency_ms = (
            end - start
        ) * 1000

        return (
            True,
            latency_ms,
            None
        )


    except Exception as error:

        end = time.perf_counter()

        latency_ms = (
            end - start
        ) * 1000

        return (
            False,
            latency_ms,
            str(error)
        )


# ======================================
# PERCENTILE
# ======================================

def percentile(
    values,
    percentage
):

    if not values:
        return None


    values = sorted(
        values
    )


    index = (
        (len(values) - 1)
        * percentage
        / 100
    )


    lower = int(index)

    upper = (
        lower + 1
    )


    if upper >= len(values):

        return values[
            lower
        ]


    weight = (
        index - lower
    )


    return (
        values[lower]
        * (1 - weight)
        +
        values[upper]
        * weight
    )


# ======================================
# RUN BENCHMARK
# ======================================

def benchmark_operation(
    database,
    name,
    operation,
    params_list
):

    print()
    print(
        f"Benchmarking {name}..."
    )


    # ----------------------------------
    # Warm-up
    # ----------------------------------

    warmup_params = (
        params_list[:WARMUP_ITERATIONS]
    )


    warmup_successful = 0


    for params in warmup_params:

        success, _, _ = measure_query(
            database,
            operation,
            params
        )

        if success:
            warmup_successful += 1


    print(
        f"Warm-up complete. "
        f"Successful: "
        f"{warmup_successful}, "
        f"Failed: "
        f"{WARMUP_ITERATIONS - warmup_successful}"
    )


    # ----------------------------------
    # Measured iterations
    # ----------------------------------

    latencies = []

    successful = 0
    failed = 0

    errors = []


    for i in range(
        MEASURED_ITERATIONS
    ):

        params = params_list[
            i % len(params_list)
        ]


        success, latency, error = (
            measure_query(
                database,
                operation,
                params
            )
        )


        if success:

            successful += 1

            latencies.append(
                latency
            )

        else:

            failed += 1

            errors.append(
                error
            )

            print(
                f"  Iteration "
                f"{i + 1} failed:"
            )

            print(
                f"  {error}"
            )


    # ----------------------------------
    # Results
    # ----------------------------------

    p50 = percentile(
        latencies,
        50
    )

    p95 = percentile(
        latencies,
        95
    )


    average = (
        statistics.mean(
            latencies
        )
        if latencies
        else None
    )


    minimum = (
        min(latencies)
        if latencies
        else None
    )


    maximum = (
        max(latencies)
        if latencies
        else None
    )


    print()
    print(
        f"{name} successful: "
        f"{successful}/"
        f"{MEASURED_ITERATIONS}"
    )

    print(
        f"{name} failed: "
        f"{failed}/"
        f"{MEASURED_ITERATIONS}"
    )


    if p50 is not None:

        print(
            f"{name} p50: "
            f"{p50:.3f} ms"
        )

        print(
            f"{name} p95: "
            f"{p95:.3f} ms"
        )


    return {
        "operation": operation,
        "successful": successful,
        "failed": failed,
        "p50_ms": p50,
        "p95_ms": p95,
        "average_ms": average,
        "min_ms": minimum,
        "max_ms": maximum,
        "errors": errors
    }


# ======================================
# MAIN
# ======================================

def main():

    print()
    print(
        "======================================"
    )

    print(
        "ARANGODB LATENCY BENCHMARK"
    )

    print(
        "======================================"
    )

    print()

    print(
        f"Measured iterations: "
        f"{MEASURED_ITERATIONS}"
    )

    print(
        f"Warm-up iterations: "
        f"{WARMUP_ITERATIONS}"
    )

    print(
        f"Random seed: "
        f"{RANDOM_SEED}"
    )


    # ==================================
    # START NODES
    # ==================================

    start_nodes = load_start_nodes()


    print()

    print(
        f"Start nodes available: "
        f"{len(start_nodes)}"
    )


    # ==================================
    # DATABASE
    # ==================================

    database = ArangoDBAdapter()


    try:

        database.connect()


        # ==================================
        # INITIAL WARM-UP
        # ==================================

        print()

        print(
            f"Warm-up: "
            f"{WARMUP_ITERATIONS} iterations"
        )


        for node_id in start_nodes[
            :WARMUP_ITERATIONS
        ]:

            try:

                database.run(
                    "traversal_1",
                    {
                        "start": node_id
                    }
                )

            except Exception:

                pass


        print(
            "Warm-up complete. "
            "Starting benchmarks..."
        )


        # ==================================
        # PARAMETER LISTS
        # ==================================

        traversal_params = [
            {
                "start": node_id
            }
            for node_id in start_nodes
        ]


        point_params = [
            {
                "user_id": node_id
            }
            for node_id in start_nodes
        ]


        # Use group 3 for indexed lookup.
        indexed_params = [
            {
                "group": 3
            }
            for _ in range(
                len(start_nodes)
            )
        ]


        aggregation_params = [
            {}
            for _ in range(
                len(start_nodes)
            )
        ]


        # ==================================
        # RESULTS
        # ==================================

        results = {}


        # ==================================
        # 1-HOP
        # ==================================

        results["1-hop traversal"] = (
            benchmark_operation(
                database,
                "1-hop traversal",
                "traversal_1",
                traversal_params
            )
        )


        # ==================================
        # 2-HOP
        # ==================================

        results["2-hop traversal"] = (
            benchmark_operation(
                database,
                "2-hop traversal",
                "traversal_2",
                traversal_params
            )
        )


        # ==================================
        # 3-HOP
        # ==================================

        results["3-hop traversal"] = (
            benchmark_operation(
                database,
                "3-hop traversal",
                "traversal_3",
                traversal_params
            )
        )


        # ==================================
        # POINT LOOKUP
        # ==================================

        results["Point lookup"] = (
            benchmark_operation(
                database,
                "Point lookup",
                "point_lookup",
                point_params
            )
        )


        # ==================================
        # INDEXED LOOKUP
        # ==================================

        results["Indexed lookup"] = (
            benchmark_operation(
                database,
                "Indexed lookup",
                "indexed_lookup",
                indexed_params
            )
        )


        # ==================================
        # AGGREGATION
        # ==================================

        results["Aggregation"] = (
            benchmark_operation(
                database,
                "Aggregation",
                "aggregation",
                aggregation_params
            )
        )


        # ==================================
        # SAVE RESULTS
        # ==================================

        RESULTS_DIR.mkdir(
            parents=True,
            exist_ok=True
        )


        output = {
            "database": "ArangoDB",

            "measured_iterations":
                MEASURED_ITERATIONS,

            "warmup_iterations":
                WARMUP_ITERATIONS,

            "random_seed":
                RANDOM_SEED,

            "start_nodes":
                len(start_nodes),

            "results":
                results
        }


        with open(
            RESULTS_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                output,
                file,
                indent=2
            )


        # ==================================
        # COMPLETE
        # ==================================

        print()

        print(
            "======================================"
        )

        print(
            "ARANGODB LATENCY BENCHMARK COMPLETE"
        )

        print(
            "======================================"
        )

        print()

        print(
            "Results saved to:"
        )

        print(
            RESULTS_FILE
        )


    finally:

        database.close()


# ======================================
# ENTRY POINT
# ======================================

if __name__ == "__main__":

    main()