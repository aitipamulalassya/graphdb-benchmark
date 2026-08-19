from connectors.neo4j import Neo4jAdapter


def main():

    print()
    print("======================================")
    print("TESTING NEO4J CONNECTION")
    print("======================================")

    database = Neo4jAdapter()

    try:

        database.connect()

        database.verify()

        print()
        print("Neo4j connection successful.")
        print()

        # Test a simple Cypher query
        result = database.run(
            "count_nodes",
            {}
        )

        print(
            f"Current Neo4j nodes: {result}"
        )

    except Exception as error:

        print()
        print("Neo4j connection FAILED.")
        print()
        print(
            f"{type(error).__name__}: {error}"
        )

    finally:

        database.close()


if __name__ == "__main__":

    main()