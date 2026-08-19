from connectors.cognodb import CognoDBAdapter


def main():

    database = CognoDBAdapter()

    try:

        database.connect()

        database.verify()

        print()
        print("======================================")
        print("TESTING COGNODB QUERIES")
        print("======================================")


        # ---------------------------------
        # 1-hop
        # ---------------------------------

        result = database.run(
            "traversal_1",
            {
                "start": 3
            }
        )

        print(
            "1-hop result:",
            result
        )


        # ---------------------------------
        # 2-hop
        # ---------------------------------

        result = database.run(
            "traversal_2",
            {
                "start": 3
            }
        )

        print(
            "2-hop result:",
            result
        )


        # ---------------------------------
        # 3-hop
        # ---------------------------------

        result = database.run(
            "traversal_3",
            {
                "start": 3
            }
        )

        print(
            "3-hop result:",
            result
        )


        # ---------------------------------
        # Point lookup
        # ---------------------------------

        result = database.run(
            "point_lookup",
            {
                "user_id": 3
            }
        )

        print(
            "Point lookup result:",
            result
        )


        # ---------------------------------
        # Indexed lookup
        # ---------------------------------

        result = database.run(
            "indexed_lookup",
            {
                "group": 3
            }
        )

        print(
            "Indexed lookup result:",
            result
        )


        # ---------------------------------
        # Aggregation
        # ---------------------------------

        result = database.run(
            "aggregation",
            {}
        )

        print(
            "Aggregation result:"
        )

        for record in result:

            print(record)


        # ---------------------------------
        # Write
        # ---------------------------------

        result = database.run(
            "write",
            {
                "temp_id": 999999999
            }
        )

        print(
            "Write result:",
            result
        )


        print()
        print("======================================")
        print("ALL QUERIES EXECUTED SUCCESSFULLY")
        print("======================================")


    finally:

        database.close()


if __name__ == "__main__":

    main()