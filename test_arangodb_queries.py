import sys
from pathlib import Path


# ======================================
# PROJECT ROOT
# ======================================

ROOT = (
    Path(__file__)
    .resolve()
    .parent
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
# RESULT COUNT HELPER
# ======================================

def result_count(result):

    if isinstance(result, int):
        return result

    if isinstance(result, list):
        return len(result)

    return 1


# ======================================
# MAIN
# ======================================

def main():

    print()
    print(
        "======================================"
    )
    print(
        "TESTING ARANGODB QUERIES"
    )
    print(
        "======================================"
    )


    database = ArangoDBAdapter()


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

        print(
            f"1-hop result: "
            f"{result_count(result)}"
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

        print(
            f"2-hop result: "
            f"{result_count(result)}"
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

        print(
            f"3-hop result: "
            f"{result_count(result)}"
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
            f"Point lookup result: "
            f"{result_count(result)}"
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

        print(
            f"Indexed lookup result: "
            f"{result_count(result)}"
        )


        # ==================================
        # AGGREGATION
        # ==================================

        result = database.run(
            "aggregation",
            {}
        )

        print(
            "Aggregation result:"
        )

        for row in result:

            print(
                f"Group: {row['group']}, "
                f"Count: {row['count']}"
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


        # ==================================
        # COMPLETE
        # ==================================

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


# ======================================
# ENTRY POINT
# ======================================

if __name__ == "__main__":
    main()