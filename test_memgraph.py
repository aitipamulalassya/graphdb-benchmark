from connectors.memgraph import MemgraphAdapter


def main():

    print()
    print("======================================")
    print("TESTING MEMGRAPH CONNECTION")
    print("======================================")


    database = MemgraphAdapter()


    try:

        database.connect()


        # ==================================
        # SIMPLE QUERY
        # ==================================

        result = database.run(
            "RETURN 1 AS value"
        )


        print(
            f"RETURN 1 result: "
            f"{result[0]['value']}"
        )


        # ==================================
        # NODE COUNT
        # ==================================

        result = database.run(
            """
            MATCH (n)
            RETURN count(n) AS count
            """
        )


        node_count = result[0]["count"]


        print(
            f"Current Memgraph nodes: "
            f"{node_count}"
        )


        # ==================================
        # RELATIONSHIP COUNT
        # ==================================

        result = database.run(
            """
            MATCH ()-[r]->()
            RETURN count(r) AS count
            """
        )


        relationship_count = (
            result[0]["count"]
        )


        print(
            f"Current Memgraph relationships: "
            f"{relationship_count}"
        )


        # ==================================
        # SUCCESS
        # ==================================

        print()
        print("======================================")
        print("MEMGRAPH CONNECTION TEST PASSED")
        print("======================================")


    except Exception as error:

        print()
        print("======================================")
        print("MEMGRAPH CONNECTION FAILED")
        print("======================================")


        print()
        print(
            f"Error type: "
            f"{type(error).__name__}"
        )

        print()
        print(
            f"Error: {error}"
        )


    finally:

        database.close()


if __name__ == "__main__":

    main()