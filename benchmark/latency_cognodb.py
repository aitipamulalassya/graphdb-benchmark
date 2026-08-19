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

from connectors.cognodb import CognoDBAdapter
from benchmark.stats import calculate_statistics


# ==========================================
# ENVIRONMENT
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
# CONFIGURATION
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
# SINGLE QUERY
# ==========================================

def measure_query(
    database,
    operation,
    params
):

    start = time.perf_counter()

    database.run(
        operation,
        params
    )

    end = time.perf_counter()

    return (
        end - start
    ) * 1000


# ==========================================
# SAFE QUERY
# ==========================================

def safe_measure(
    database,
    operation,
    params
):

    try:

        latency = measure_query(
            database,
            operation,
            params
        )

        return {
            "success": True,
            "latency_ms": latency,
            "error": None
        }

    except Exception as error:

        return {
            "success": False,
            "latency_ms": None,
            "error": (
                type(error).__name__
                + ": "
                + str(error)
            )
        }


# ==========================================
# WARMUP
# ==========================================

def warm_up(
    database,
    start_nodes
):

    print()
    print(
        f"Warm-up: {WARMUP} iterations"
    )

    generator = random.Random(
        SEED
    )

    successful = 0

    failed = 0

    for _ in range(WARMUP):

        start_node = generator.choice(
            start_nodes
        )

        result = safe_measure(
            database,
            "traversal_1",
            {
                "start": start_node
            }
        )

        if result["success"]:

            successful += 1

        else:

            failed += 1

    print(
        f"Warm-up complete. "
        f"Successful: {successful}, "
        f"Failed: {failed}"
    )


# ==========================================
# GENERIC BENCHMARK
# ==========================================

def benchmark_operation(
    database,
    operation,
    parameter_generator,
    label
):

    print()
    print(
        f"Benchmarking {label}..."
    )

    latencies = []

    failures = []

    unavailable = False

    for iteration in range(
        ITERATIONS
    ):

        # ----------------------------------
        # If database became unavailable,
        # don't keep hammering it.
        # ----------------------------------

        if unavailable:

            failures.append(
                {
                    "iteration":
                        iteration + 1,

                    "error":
                        "Database unavailable "
                        "after previous connection failure"
                }
            )

            continue


        params = parameter_generator(
            iteration
        )

        result = safe_measure(
            database,
            operation,
            params
        )


        if result["success"]:

            latencies.append(
                result["latency_ms"]
            )

        else:

            error_message = result[
                "error"
            ]

            failures.append(
                {
                    "iteration":
                        iteration + 1,

                    "error":
                        error_message
                }
            )

            print(
                f"  Iteration "
                f"{iteration + 1} failed:"
            )

            print(
                f"  {error_message}"
            )

            # ----------------------------------
            # Try ONE reconnect only.
            # ----------------------------------

            try:

                database.reconnect()

                print(
                    "  Reconnection attempted."
                )

            except Exception as reconnect_error:

                print(
                    "  Reconnection failed."
                )

                print(
                    f"  {type(reconnect_error).__name__}: "
                    f"{reconnect_error}"
                )

                unavailable = True


    # ======================================
    # STATISTICS
    # ======================================

    if latencies:

        statistics = calculate_statistics(
            latencies
        )

    else:

        statistics = {

            "count": 0,

            "min_ms": None,

            "p50_ms": None,

            "p95_ms": None,

            "mean_ms": None,

            "max_ms": None
        }


    successful_count = len(
        latencies
    )

    failed_count = len(
        failures
    )


    # ======================================
    # PRINT
    # ======================================

    print()

    print(
        f"{label} successful: "
        f"{successful_count}/{ITERATIONS}"
    )

    print(
        f"{label} failed: "
        f"{failed_count}/{ITERATIONS}"
    )


    if latencies:

        print(
            f"{label} p50: "
            f"{statistics['p50_ms']:.3f} ms"
        )

        print(
            f"{label} p95: "
            f"{statistics['p95_ms']:.3f} ms"
        )

    else:

        print(
            f"{label} p50: N/A"
        )

        print(
            f"{label} p95: N/A"
        )


    return {

        "statistics":
            statistics,

        "successful_iterations":
            successful_count,

        "failed_iterations":
            failed_count,

        "failures":
            failures

    }


# ==========================================
# TRAVERSALS
# ==========================================

def benchmark_traversal(
    database,
    depth,
    start_nodes
):

    generator = random.Random(
        SEED + depth
    )

    def parameters(_):

        return {
            "start":
                generator.choice(
                    start_nodes
                )
        }

    return benchmark_operation(
        database,

        f"traversal_{depth}",

        parameters,

        f"{depth}-hop traversal"
    )


# ==========================================
# POINT LOOKUP
# ==========================================

def benchmark_point_lookup(
    database,
    start_nodes
):

    generator = random.Random(
        SEED + 100
    )

    def parameters(_):

        return {
            "user_id":
                generator.choice(
                    start_nodes
                )
        }

    return benchmark_operation(
        database,

        "point_lookup",

        parameters,

        "Point lookup"
    )


# ==========================================
# INDEXED LOOKUP
# ==========================================

def benchmark_indexed_lookup(
    database
):

    generator = random.Random(
        SEED + 200
    )

    def parameters(_):

        return {
            "group":
                generator.randrange(
                    10
                )
        }

    return benchmark_operation(
        database,

        "indexed_lookup",

        parameters,

        "Indexed lookup"
    )


# ==========================================
# AGGREGATION
# ==========================================

def benchmark_aggregation(
    database
):

    def parameters(_):

        return {}

    return benchmark_operation(
        database,

        "aggregation",

        parameters,

        "Aggregation"
    )


# ==========================================
# MAIN
# ==========================================

def main():

    print()
    print(
        "======================================"
    )

    print(
        "COGNODB LATENCY BENCHMARK"
    )

    print(
        "======================================"
    )

    print()

    print(
        f"Measured iterations: "
        f"{ITERATIONS}"
    )

    print(
        f"Warm-up iterations: "
        f"{WARMUP}"
    )

    print(
        f"Random seed: "
        f"{SEED}"
    )


    # --------------------------------------
    # START NODES
    # --------------------------------------

    start_nodes = load_start_nodes()

    print(
        f"Start nodes available: "
        f"{len(start_nodes)}"
    )


    # --------------------------------------
    # CONNECT
    # --------------------------------------

    database = CognoDBAdapter()

    measurements = {}


    try:

        database.connect()

        database.verify()


        # ----------------------------------
        # WARMUP
        # ----------------------------------

        warm_up(
            database,
            start_nodes
        )


        # ----------------------------------
        # 1-HOP
        # ----------------------------------

        measurements[
            "traversal_1"
        ] = benchmark_traversal(
            database,
            1,
            start_nodes
        )


        # ----------------------------------
        # 2-HOP
        # ----------------------------------

        measurements[
            "traversal_2"
        ] = benchmark_traversal(
            database,
            2,
            start_nodes
        )


        # ----------------------------------
        # 3-HOP
        # ----------------------------------

        measurements[
            "traversal_3"
        ] = benchmark_traversal(
            database,
            3,
            start_nodes
        )


        # ----------------------------------
        # POINT LOOKUP
        # ----------------------------------

        measurements[
            "point_lookup"
        ] = benchmark_point_lookup(
            database,
            start_nodes
        )


        # ----------------------------------
        # INDEXED LOOKUP
        # ----------------------------------

        measurements[
            "indexed_lookup"
        ] = benchmark_indexed_lookup(
            database
        )


        # ----------------------------------
        # AGGREGATION
        # ----------------------------------

        measurements[
            "aggregation"
        ] = benchmark_aggregation(
            database
        )


    except Exception as error:

        print()
        print(
            "Benchmark-level error:"
        )

        print(
            f"{type(error).__name__}: "
            f"{error}"
        )


    finally:

        database.close()


    # ======================================
    # SAVE RESULTS
    # ======================================

    results = {

        "platform":
            "cognodb",

        "iterations":
            ITERATIONS,

        "warmup_iterations":
            WARMUP,

        "random_seed":
            SEED,

        "indexed_properties": [

            "user_id",

            "group"

        ],

        "measurements":
            measurements

    }


    output_file = (
        RESULTS_DIR
        / "cognodb_latency.json"
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


    # ======================================
    # FINAL MESSAGE
    # ======================================

    print()
    print(
        "======================================"
    )

    print(
        "LATENCY BENCHMARK COMPLETE"
    )

    print(
        "======================================"
    )

    print()

    print(
        "Results saved to:"
    )

    print(
        output_file
    )

    print()

    print(
        "CognoDB benchmark finished."
    )


# ==========================================
# ENTRY POINT
# ==========================================

if __name__ == "__main__":

    main()