import sys
from pathlib import Path


ROOT = (
    Path(__file__)
    .resolve()
    .parent
)

sys.path.insert(
    0,
    str(ROOT)
)


from connectors.falkordb import FalkorDBAdapter


def get_count(response):
    """
    FalkorDB compact response format:

    [
        header,
        rows,
        metadata
    ]

    Example:

    [
        [[1, b'count']],
        [[3, 23]],
        [...]
    ]
    """

    try:

        rows = response[1]

        if not rows:
            return None

        value = rows[0][1]

        if isinstance(value, bytes):
            value = value.decode()

        return int(value)

    except Exception:

        return None


def main():

    print()
    print(
        "======================================"
    )

    print(
        "TESTING FALKORDB QUERIES"
    )

    print(
        "======================================"
    )


    database = FalkorDBAdapter()


    try:

        database.connect()


        # ==================================
        # 1-HOP
        # ==================================

        result = database.run(
            "traversal_1",
            {
                "start": 3
            }
        )

        count = get_count(
            result
        )

        print(
            f"1-hop result: {count}"
        )


        # ==================================
        # 2-HOP
        # ==================================

        result = database.run(
            "traversal_2",
            {
                "start": 3
            }
        )

        count = get_count(
            result
        )

        print(
            f"2-hop result: {count}"
        )


        # ==================================
        # 3-HOP
        # ==================================

        result = database.run(
            "traversal_3",
            {
                "start": 3
            }
        )

        count = get_count(
            result
        )

        print(
            f"3-hop result: {count}"
        )


        # ==================================
        # POINT LOOKUP
        # ==================================

        result = database.run(
            "point_lookup",
            {
                "user_id": 3
            }
        )

        print(
            f"Point lookup result: {result}"
        )


        # ==================================
        # INDEXED LOOKUP
        # ==================================

        result = database.run(
            "indexed_lookup",
            {
                "group": 3
            }
        )

        count = get_count(
            result
        )

        print(
            f"Indexed lookup result: {count}"
        )


        # ==================================
        # AGGREGATION
        # ==================================

        result = database.run(
            "aggregation"
        )

        print(
            "Aggregation result:"
        )

        print(
            result
        )


        # ==================================
        # WRITE
        # ==================================

        result = database.run(
            "write",
            {
                "temp_id": 999999
            }
        )

        print(
            f"Write result: {result}"
        )


        # ==================================
        # DELETE TEMP NODE
        # ==================================

        database.run(
            "delete_temp",
            {
                "temp_id": 999999
            }
        )


        print()
        print(
            "======================================"
        )

        print(
            "ALL QUERIES EXECUTED SUCCESSFULLY"
        )

        print(
            "======================================"
        )


    finally:

        database.close()


if __name__ == "__main__":

    main()