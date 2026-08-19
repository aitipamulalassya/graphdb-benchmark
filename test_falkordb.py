from connectors.falkordb import FalkorDBAdapter


def main():

    print()
    print("======================================")
    print("TESTING FALKORDB CONNECTION")
    print("======================================")

    database = FalkorDBAdapter()

    try:

        database.connect()

        print(
            "Running PING..."
        )

        result = database.client.ping()

        print(
            f"PING result: {result}"
        )

        print()
        print(
            "Testing GRAPH.QUERY..."
        )

        result = database.run(
            """
            RETURN 1
            """
        )

        print(
            f"RETURN 1 result: {result}"
        )

        print()
        print(
            "======================================"
        )

        print(
            "FALKORDB CONNECTION TEST PASSED"
        )

        print(
            "======================================"
        )


    except Exception as error:

        print()
        print(
            "======================================"
        )

        print(
            "FALKORDB CONNECTION TEST FAILED"
        )

        print(
            "======================================"
        )

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