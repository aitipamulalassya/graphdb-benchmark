from connectors.memgraph import MemgraphAdapter


def main():

    print()
    print("======================================")
    print("TESTING MEMGRAPH QUERIES")
    print("======================================")


    database = MemgraphAdapter()


    try:

        database.connect()


        # ==================================
        # 1-HOP
        # ==================================

        result = database.run(
            """
            MATCH (start:User {user_id: $start})
                  -[:VOTE]->
                  (neighbor)
            RETURN count(DISTINCT neighbor) AS count
            """,
            {
                "start": 3
            }
        )

        print(
            f"1-hop result: {result[0]['count']}"
        )


        # ==================================
        # 2-HOP
        # ==================================

        result = database.run(
            """
            MATCH (start:User {user_id: $start})
                  -[:VOTE*2]->
                  (neighbor)
            RETURN count(DISTINCT neighbor) AS count
            """,
            {
                "start": 3
            }
        )

        print(
            f"2-hop result: {result[0]['count']}"
        )


        # ==================================
        # 3-HOP
        # ==================================

        result = database.run(
            """
            MATCH (start:User {user_id: $start})
                  -[:VOTE*3]->
                  (neighbor)
            RETURN count(DISTINCT neighbor) AS count
            """,
            {
                "start": 3
            }
        )

        print(
            f"3-hop result: {result[0]['count']}"
        )


        # ==================================
        # POINT LOOKUP
        # ==================================

        result = database.run(
            """
            MATCH (u:User {user_id: $user_id})
            RETURN u.user_id AS user_id
            """,
            {
                "user_id": 3
            }
        )

        point_value = (
            result[0]["user_id"]
            if result
            else None
        )

        print(
            f"Point lookup result: "
            f"{point_value}"
        )


        # ==================================
        # INDEXED LOOKUP
        # ==================================

        result = database.run(
            """
            MATCH (u:User {group: $group})
            RETURN count(u) AS count
            """,
            {
                "group": 3
            }
        )

        print(
            f"Indexed lookup result: "
            f"{result[0]['count']}"
        )


        # ==================================
        # AGGREGATION
        # ==================================

        result = database.run(
            """
            MATCH (u:User)
            RETURN
                u.group AS group,
                count(u) AS count
            ORDER BY group
            """
        )

        print(
            "Aggregation result:"
        )

        for record in result:

            print(record)


        # ==================================
        # WRITE
        # ==================================

        database.run(
            """
            CREATE (
                temp:BenchmarkTemp
            {
                temp_id: $temp_id
            })
            """,
            {
                "temp_id": 999999999
            }
        )


        database.run(
            """
            MATCH (temp:BenchmarkTemp
            {
                temp_id: $temp_id
            })
            DELETE temp
            """,
            {
                "temp_id": 999999999
            }
        )


        print(
            "Write result: True"
        )


        print()
        print("======================================")
        print("ALL QUERIES EXECUTED SUCCESSFULLY")
        print("======================================")


    finally:

        database.close()


if __name__ == "__main__":

    main()