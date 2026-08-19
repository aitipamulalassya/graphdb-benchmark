import json
import os
import random
import sys
import time
from pathlib import Path


# ==========================================
# PROJECT ROOT
# ==========================================

ROOT = Path(
    __file__
).resolve().parent.parent

sys.path.insert(
    0,
    str(ROOT)
)


# ==========================================
# IMPORTS
# ==========================================

from dotenv import load_dotenv

from connectors.neo4j import Neo4jAdapter
from benchmark.stats import calculate_statistics


# ==========================================
# LOAD ENVIRONMENT
# ==========================================

load_dotenv()


# ==========================================
# PATHS
# ==========================================

START_NODES_FILE = (
    ROOT
    / "data"
    / "prepared"
    / "start_nodes.json"
)

RESULTS_DIR = (
    ROOT
    / "results"
)

RESULTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ==========================================
# BENCHMARK CONFIGURATION
# ==========================================

ITERATIONS = int(
    os.getenv(
        "BENCH_ITERATIONS",
        "20"
    )
)

WARMUP = int(
    os.getenv(
        "BENCH_WARMUP",
        "5"
    )
)

SEED = int(
    os.getenv(
        "BENCH_SEED",
        "20260819"
    )
)


# ==========================================
# LOAD START NODES
# ==========================================

def load_start_nodes():

    with open(
        START_NODES_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# ==========================================
# MEASURE QUERY
# ==========================================

def measure_query(
    database,
    operation,
    params
):

    start_time = time.perf_counter()

    result = database.run(
        operation,
        params
    )

    end_time = time.perf_counter()

    latency_ms = (
        end_time - start_time
    ) * 1000

    return latency_ms, result


# ==========================================
# WARM UP
# ==========================================

def warm_up(
    database,
    start_nodes
):

    print()
    print(
        f"Warm-up: {WARMUP} iterations"
    )

    random_generator = random.Random(
        SEED
    )

    successful = 0
    failed = 0

    for i in range(WARMUP):

        start_node = random_generator.choice(
            start_nodes
        )

        try:

            database.run(
                "traversal_1",
                {
                    "start": start_node
                }
            )

            successful += 1

        except Exception as error:

            failed += 1

            print(
                f"Warm-up iteration {i + 1} failed:"
            )

            print(
                f"  {type(error).__name__}: {error}"
            )

    print(
        f"Warm-up complete. "
        f"Successful: {successful}, "
        f"Failed: {failed}"
    )


# ==========================================
# BENCHMARK TRAVERSAL
# ==========================================

def benchmark_traversal(
    database,
    depth,
    start_nodes
):

    print()
    print(
        f"Benchmarking {depth}-hop traversal..."
    )

    random_generator = random.Random(
        SEED + depth
    )

    latencies = []

    successful = 0
    failed = 0

    for i in range(ITERATIONS):

        start_node = random_generator.choice(
            start_nodes
        )

        try:

            latency, result = measure_query(
                database,
                f"traversal_{depth}",
                {
                    "start": start_node
                }
            )

            latencies.append(
                latency
            )

            successful += 1

        except Exception as error:

            failed += 1

            print()
            print(
                f"  Iteration {i + 1} failed:"
            )

            print(
                f"  {type(error).__name__}: {error}"
            )

    print()
    print(
        f"{depth}-hop traversal successful: "
        f"{successful}/{ITERATIONS}"
    )

    print(
        f"{depth}-hop traversal failed: "
        f"{failed}/{ITERATIONS}"
    )

    if not latencies:

        raise RuntimeError(
            f"All {depth}-hop traversal "
            f"iterations failed."
        )

    statistics = calculate_statistics(
        latencies
    )

    print(
        f"{depth}-hop traversal p50: "
        f"{statistics['p50_ms']:.3f} ms"
    )

    print(
        f"{depth}-hop traversal p95: "
        f"{statistics['p95_ms']:.3f} ms"
    )

    statistics["successful_iterations"] = successful
    statistics["failed_iterations"] = failed

    return statistics


# ==========================================
# POINT LOOKUP
# ==========================================

def benchmark_point_lookup(
    database,
    start_nodes
):

    print()
    print(
        "Benchmarking Point lookup..."
    )

    random_generator = random.Random(
        SEED + 100
    )

    latencies = []

    successful = 0
    failed = 0

    for i in range(ITERATIONS):

        user_id = random_generator.choice(
            start_nodes
        )

        try:

            latency, result = measure_query(
                database,
                "point_lookup",
                {
                    "user_id": user_id
                }
            )

            latencies.append(
                latency
            )

            successful += 1

        except Exception as error:

            failed += 1

            print()
            print(
                f"  Iteration {i + 1} failed:"
            )

            print(
                f"  {type(error).__name__}: {error}"
            )

    print()
    print(
        f"Point lookup successful: "
        f"{successful}/{ITERATIONS}"
    )

    print(
        f"Point lookup failed: "
        f"{failed}/{ITERATIONS}"
    )

    if not latencies:

        raise RuntimeError(
            "All point lookup iterations failed."
        )

    statistics = calculate_statistics(
        latencies
    )

    print(
        f"Point lookup p50: "
        f"{statistics['p50_ms']:.3f} ms"
    )

    print(
        f"Point lookup p95: "
        f"{statistics['p95_ms']:.3f} ms"
    )

    statistics["successful_iterations"] = successful
    statistics["failed_iterations"] = failed

    return statistics


# ==========================================
# INDEXED LOOKUP
# ==========================================

def benchmark_indexed_lookup(
    database
):

    print()
    print(
        "Benchmarking Indexed lookup..."
    )

    random_generator = random.Random(
        SEED + 200
    )

    latencies = []

    successful = 0
    failed = 0

    for i in range(ITERATIONS):

        group = random_generator.randrange(
            10
        )

        try:

            latency, result = measure_query(
                database,
                "indexed_lookup",
                {
                    "group": group
                }
            )

            latencies.append(
                latency
            )

            successful += 1

        except Exception as error:

            failed += 1

            print()
            print(
                f"  Iteration {i + 1} failed:"
            )

            print(
                f"  {type(error).__name__}: {error}"
            )

    print()
    print(
        f"Indexed lookup successful: "
        f"{successful}/{ITERATIONS}"
    )

    print(
        f"Indexed lookup failed: "
        f"{failed}/{ITERATIONS}"
    )

    if not latencies:

        raise RuntimeError(
            "All indexed lookup iterations failed."
        )

    statistics = calculate_statistics(
        latencies
    )

    print(
        f"Indexed lookup p50: "
        f"{statistics['p50_ms']:.3f} ms"
    )

    print(
        f"Indexed lookup p95: "
        f"{statistics['p95_ms']:.3f} ms"
    )

    statistics["successful_iterations"] = successful
    statistics["failed_iterations"] = failed

    return statistics


# ==========================================
# AGGREGATION
# ==========================================

def benchmark_aggregation(
    database
):

    print()
    print(
        "Benchmarking Aggregation..."
    )

    latencies = []

    successful = 0
    failed = 0

    for i in range(ITERATIONS):

        try:

            latency, result = measure_query(
                database,
                "aggregation",
                {}
            )

            latencies.append(
                latency
            )

            successful += 1

        except Exception as error:

            failed += 1

            print()
            print(
                f"  Iteration {i + 1} failed:"
            )

            print(
                f"  {type(error).__name__}: {error}"
            )

    print()
    print(
        f"Aggregation successful: "
        f"{successful}/{ITERATIONS}"
    )

    print(
        f"Aggregation failed: "
        f"{failed}/{ITERATIONS}"
    )

    if not latencies:

        raise RuntimeError(
            "All aggregation iterations failed."
        )

    statistics = calculate_statistics(
        latencies
    )

    print(
        f"Aggregation p50: "
        f"{statistics['p50_ms']:.3f} ms"
    )

    print(
        f"Aggregation p95: "
        f"{statistics['p95_ms']:.3f} ms"
    )

    statistics["successful_iterations"] = successful
    statistics["failed_iterations"] = failed

    return statistics


# ==========================================
# MAIN
# ==========================================

def main():

    print()
    print("======================================")
    print("NEO4J LATENCY BENCHMARK")
    print("======================================")


    print()
    print(
        f"Measured iterations: {ITERATIONS}"
    )

    print(
        f"Warm-up iterations: {WARMUP}"
    )

    print(
        f"Random seed: {SEED}"
    )


    # --------------------------------------
    # Load start nodes
    # --------------------------------------

    start_nodes = load_start_nodes()

    print()
    print(
        f"Start nodes available: "
        f"{len(start_nodes)}"
    )


    # --------------------------------------
    # Connect
    # --------------------------------------

    database = Neo4jAdapter()

    try:

        database.connect()

        database.verify()


        # ----------------------------------
        # Warm up
        # ----------------------------------

        warm_up(
            database,
            start_nodes
        )


        # ----------------------------------
        # Measurements
        # ----------------------------------

        measurements = {}


        # 1-hop

        measurements[
            "traversal_1"
        ] = benchmark_traversal(
            database,
            1,
            start_nodes
        )


        # 2-hop

        measurements[
            "traversal_2"
        ] = benchmark_traversal(
            database,
            2,
            start_nodes
        )


        # 3-hop

        measurements[
            "traversal_3"
        ] = benchmark_traversal(
            database,
            3,
            start_nodes
        )


        # Point lookup

        measurements[
            "point_lookup"
        ] = benchmark_point_lookup(
            database,
            start_nodes
        )


        # Indexed lookup

        measurements[
            "indexed_lookup"
        ] = benchmark_indexed_lookup(
            database
        )


        # Aggregation

        measurements[
            "aggregation"
        ] = benchmark_aggregation(
            database
        )


        # ----------------------------------
        # Save results
        # ----------------------------------

        results = {

            "platform": "neo4j",

            "database": database.database,

            "iterations": ITERATIONS,

            "warmup_iterations": WARMUP,

            "random_seed": SEED,

            "dataset": {

                "nodes": 7115,

                "relationships": 103689

            },

            "indexed_properties": [

                "user_id",

                "group"

            ],

            "measurements": measurements

        }


        output_file = (
            RESULTS_DIR
            / "neo4j_latency.json"
        )


        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                results,
                file,
                indent=2
            )


        # ----------------------------------
        # Complete
        # ----------------------------------

        print()
        print("======================================")
        print("NEO4J LATENCY BENCHMARK COMPLETE")
        print("======================================")

        print()
        print(
            "Results saved to:"
        )

        print(
            output_file
        )


    finally:

        database.close()


# ==========================================
# ENTRY POINT
# ==========================================

if __name__ == "__main__":

    main()