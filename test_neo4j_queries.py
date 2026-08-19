from connectors.neo4j import Neo4jAdapter


def main():

    print()
    print("======================================")
    print("TESTING NEO4J QUERIES")
    print("======================================")


    database = Neo4jAdapter()


    try:

        database.connect()

        database.verify()


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
            f"1-hop result: {result}"
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
            f"2-hop result: {result}"
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
            f"3-hop result: {result}"
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

        print(
            f"Indexed lookup result: {result}"
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

        for record in result:

            print(record)


        # ==================================
        # WRITE TEST
        # ==================================

        result = database.run(
            "write",
            {
                "temp_id": 999999999
            }
        )

        print(
            f"Write result: {result}"
        )


        # ==================================
        # SUCCESS
        # ==================================

        print()
        print("======================================")
        print("ALL QUERIES EXECUTED SUCCESSFULLY")
        print("======================================")


    finally:

        database.close()


if __name__ == "__main__":

    main()