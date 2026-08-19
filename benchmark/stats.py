import math


def percentile(values, percentile_value):

    if not values:
        return None

    sorted_values = sorted(values)

    position = (
        len(sorted_values) - 1
    ) * percentile_value

    lower_index = math.floor(position)
    upper_index = math.ceil(position)

    if lower_index == upper_index:
        return sorted_values[lower_index]

    lower_value = sorted_values[lower_index]
    upper_value = sorted_values[upper_index]

    return (
        lower_value
        + (
            upper_value - lower_value
        )
        * (position - lower_index)
    )


def calculate_statistics(values):

    if not values:

        return {
            "count": 0,
            "min_ms": None,
            "p50_ms": None,
            "p95_ms": None,
            "mean_ms": None,
            "max_ms": None
        }

    return {

        "count": len(values),

        "min_ms": min(values),

        "p50_ms": percentile(
            values,
            0.50
        ),

        "p95_ms": percentile(
            values,
            0.95
        ),

        "mean_ms": (
            sum(values)
            / len(values)
        ),

        "max_ms": max(values)
    }