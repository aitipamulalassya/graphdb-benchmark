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
# MAIN
# ======================================

def main():

    print()
    print("======================================")
    print("TESTING ARANGODB CONNECTION")
    print("======================================")

    database = ArangoDBAdapter()

    try:

        database.connect()

        print(
            "ArangoDB connection successful"
        )

        print()
        print(
            "Running RETURN 1..."
        )

        result = database.run(
            "return_1",
            {}
        )

        print(
            f"RETURN 1 result: {result}"
        )

        print()
        print(
            "Testing database..."
        )

 

        result = database.verify()

        print(
    f"Database version: {result}"
)

        print()
        print("======================================")
        print("ARANGODB CONNECTION TEST PASSED")
        print("======================================")


    except Exception as error:

        print()
        print("======================================")
        print("ARANGODB CONNECTION TEST FAILED")
        print("======================================")

        print(
            f"Error type: "
            f"{type(error).__name__}"
        )

        print(
            f"Error: {error}"
        )

        raise


    finally:

        database.close()


if __name__ == "__main__":

    main()