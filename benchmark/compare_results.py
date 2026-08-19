import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = ROOT / "results"


DATABASES = [
    "cognodb",
    "neo4j",
    "memgraph",
    "falkordb",
    "arangodb",
]


OPERATIONS = {
    "traversal_1": "1-hop traversal",
    "traversal_2": "2-hop traversal",
    "traversal_3": "3-hop traversal",
    "point_lookup": "Point lookup",
    "indexed_lookup": "Indexed lookup",
    "aggregation": "Aggregation",
}


def load_json(database):

    path = RESULTS_DIR / f"{database}_latency.json"

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def get_measurements(data):

    # Neo4j / Memgraph / FalkorDB / CognoDB
    if "measurements" in data:
        return data["measurements"]

    # ArangoDB
    if "results" in data:

        measurements = {}

        for operation_name, result in data["results"].items():

            operation = result["operation"]

            measurements[operation] = {
                "statistics": {
                    "p50_ms": result["p50_ms"],
                    "p95_ms": result["p95_ms"],
                    "mean_ms": result.get(
                        "average_ms"
                    ),
                    "min_ms": result.get(
                        "min_ms"
                    ),
                    "max_ms": result.get(
                        "max_ms"
                    ),
                    "count": result["successful"],
                },
                "successful_iterations": result[
                    "successful"
                ],
                "failed_iterations": result[
                    "failed"
                ],
            }

        return measurements

    raise ValueError(
        "Unknown JSON structure"
    )


def extract_result(data, operation):

    measurements = get_measurements(data)

    if operation not in measurements:
        return None

    item = measurements[operation]

    statistics = item.get(
        "statistics",
        item
    )

    p50 = statistics.get("p50_ms")
    p95 = statistics.get("p95_ms")
    mean = statistics.get("mean_ms")

    successful = item.get(
        "successful_iterations",
        statistics.get("count", 0)
    )

    failed = item.get(
        "failed_iterations",
        0
    )

    return {
        "p50_ms": p50,
        "p95_ms": p95,
        "mean_ms": mean,
        "successful": successful,
        "failed": failed,
    }


def main():

    print()
    print("======================================")
    print("GRAPH DATABASE BENCHMARK COMPARISON")
    print("======================================")

    all_results = {}

    # ======================================
    # LOAD ALL DATABASES
    # ======================================

    for database in DATABASES:

        try:

            data = load_json(database)

            all_results[database] = data

            print(
                f"Loaded: {database}"
            )

        except FileNotFoundError:

            print(
                f"WARNING: "
                f"{database}_latency.json "
                f"not found"
            )


    # ======================================
    # P50 TABLE
    # ======================================

    print()
    print("======================================")
    print("P50 LATENCY (ms)")
    print("======================================")

    header = (
        f"{'Operation':<22}"
        + "".join(
            f"{db:<14}"
            for db in all_results
        )
    )

    print(header)
    print("-" * len(header))


    comparison = {}


    for operation, display_name in OPERATIONS.items():

        comparison[operation] = {}

        row = f"{display_name:<22}"

        for database, data in all_results.items():

            result = extract_result(
                data,
                operation
            )

            if result is None:
                row += f"{'N/A':<14}"
                continue

            p50 = result["p50_ms"]

            if p50 is None:

                row += f"{'FAILED':<14}"

            else:

                row += f"{p50:<14.3f}"

                comparison[operation][database] = {
                    **result
                }

        print(row)


    # ======================================
    # P95 TABLE
    # ======================================

    print()
    print("======================================")
    print("P95 LATENCY (ms)")
    print("======================================")

    print(header)
    print("-" * len(header))


    for operation, display_name in OPERATIONS.items():

        row = f"{display_name:<22}"

        for database, data in all_results.items():

            result = extract_result(
                data,
                operation
            )

            if result is None:

                row += f"{'N/A':<14}"
                continue

            p95 = result["p95_ms"]

            if p95 is None:

                row += f"{'FAILED':<14}"

            else:

                row += f"{p95:<14.3f}"

        print(row)


    # ======================================
    # SUCCESS RATE
    # ======================================

    print()
    print("======================================")
    print("SUCCESS RATE")
    print("======================================")

    print(header)
    print("-" * len(header))


    for operation, display_name in OPERATIONS.items():

        row = f"{display_name:<22}"

        for database, data in all_results.items():

            result = extract_result(
                data,
                operation
            )

            if result is None:

                row += f"{'N/A':<14}"
                continue

            successful = result["successful"]
            failed = result["failed"]

            total = successful + failed

            if total == 0:

                row += f"{'N/A':<14}"

            else:

                rate = (
                    successful / total
                ) * 100

                row += (
                    f"{rate:.1f}%"
                    f"{'':<9}"
                )

        print(row)


    # ======================================
    # FASTEST DATABASE
    # ======================================

    print()
    print("======================================")
    print("FASTEST DATABASE BY OPERATION")
    print("======================================")


    fastest = {}


    for operation, display_name in OPERATIONS.items():

        candidates = {}

        for database, data in all_results.items():

            result = extract_result(
                data,
                operation
            )

            if result is None:
                continue

            p50 = result["p50_ms"]

            successful = result["successful"]
            failed = result["failed"]

            # Only consider databases where
            # every measured iteration succeeded.
            if (
                p50 is not None
                and failed == 0
                and successful > 0
            ):

                candidates[database] = p50


        if candidates:

            winner = min(
                candidates,
                key=candidates.get
            )

            fastest[operation] = {
                "database": winner,
                "p50_ms": candidates[winner]
            }

            print(
                f"{display_name:<22}"
                f"{winner:<12}"
                f"{candidates[winner]:.3f} ms"
            )

        else:

            fastest[operation] = None

            print(
                f"{display_name:<22}"
                f"No valid result"
            )


    # ======================================
    # OVERALL AVERAGE P50
    # ======================================

    print()
    print("======================================")
    print("OVERALL AVERAGE P50")
    print("======================================")


    overall = {}


    for database, data in all_results.items():

        values = []

        for operation in OPERATIONS:

            result = extract_result(
                data,
                operation
            )

            if result is None:
                continue

            p50 = result["p50_ms"]

            if (
                p50 is not None
                and result["failed"] == 0
            ):

                values.append(p50)


        if values:

            average = sum(values) / len(values)

            overall[database] = {
                "average_p50_ms": average,
                "operations_count": len(values)
            }

            print(
                f"{database:<14}"
                f"{average:.3f} ms"
            )


    # ======================================
    # SAVE
    # ======================================

    output = {
        "databases": list(
            all_results.keys()
        ),
        "operations": OPERATIONS,
        "comparison": comparison,
        "fastest": fastest,
        "overall_average_p50": overall,
    }


    output_file = (
        RESULTS_DIR
        / "benchmark_comparison.json"
    )


    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            output,
            file,
            indent=2
        )


    print()
    print("======================================")
    print("COMPARISON COMPLETE")
    print("======================================")

    print()
    print(
        f"Results saved to:\n{output_file}"
    )


if __name__ == "__main__":
    main()