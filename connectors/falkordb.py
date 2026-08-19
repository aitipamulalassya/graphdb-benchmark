import os

import redis
from dotenv import load_dotenv


load_dotenv()


class FalkorDBAdapter:

    def __init__(self):

        self.host = os.getenv("FALKORDB_HOST")
        self.port = int(
            os.getenv("FALKORDB_PORT", "6379")
        )

        self.username = os.getenv(
            "FALKORDB_USERNAME"
        )

        self.password = os.getenv(
            "FALKORDB_PASSWORD"
        )

        self.ssl = (
            os.getenv(
                "FALKORDB_SSL",
                "false"
            ).lower() == "true"
        )

        self.graph_name = os.getenv(
            "FALKORDB_GRAPH",
            "benchmark"
        )

        self.client = None


    # ======================================
    # CONNECT
    # ======================================

    def connect(self):

        if not self.host:
            raise ValueError(
                "FALKORDB_HOST is not configured."
            )

        if not self.password:
            raise ValueError(
                "FALKORDB_PASSWORD is not configured."
            )

        self.client = redis.Redis(
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            ssl=self.ssl,
            decode_responses=False,
            socket_connect_timeout=30,
            socket_timeout=120,
            health_check_interval=30
        )

        self.client.ping()

        print(
            "FalkorDB connection successful"
        )


    # ======================================
    # GRAPH QUERY
    # ======================================

    def query(
        self,
        cypher,
        params=None
    ):

        if self.client is None:
            raise RuntimeError(
                "FalkorDB is not connected."
            )

        params = params or {}

        # Replace simple named parameters.
        # This is sufficient for our benchmark
        # because parameters are integers.

        prepared_query = cypher

        for key, value in params.items():

            prepared_query = prepared_query.replace(
                f"${key}",
                str(value)
            )

        response = self.client.execute_command(
            "GRAPH.QUERY",
            self.graph_name,
            prepared_query,
            "--compact"
        )

        return response


    # ======================================
    # RUN OPERATION
    # ======================================

    def run(
        self,
        operation,
        params=None
    ):

        params = params or {}


        if operation == "traversal_1":

            return self.query(
                """
                MATCH (
                    start:User {
                        user_id: $start
                    }
                )
                -[:VOTE]->
                (neighbor)

                RETURN count(
                    DISTINCT neighbor
                ) AS count
                """,
                params
            )


        if operation == "traversal_2":

            return self.query(
                """
                MATCH (
                    start:User {
                        user_id: $start
                    }
                )
                -[:VOTE*2]->
                (neighbor)

                RETURN count(
                    DISTINCT neighbor
                ) AS count
                """,
                params
            )


        if operation == "traversal_3":

            return self.query(
                """
                MATCH (
                    start:User {
                        user_id: $start
                    }
                )
                -[:VOTE*3]->
                (neighbor)

                RETURN count(
                    DISTINCT neighbor
                ) AS count
                """,
                params
            )


        if operation == "point_lookup":

            return self.query(
                """
                MATCH (
                    u:User {
                        user_id: $user_id
                    }
                )

                RETURN u.user_id AS user_id
                """,
                params
            )


        if operation == "indexed_lookup":

            return self.query(
                """
                MATCH (
                    u:User {
                        group: $group
                    }
                )

                RETURN count(u) AS count
                """,
                params
            )


        if operation == "aggregation":

            return self.query(
                """
                MATCH (u:User)

                RETURN
                    u.group AS group,
                    count(u) AS count

                ORDER BY group
                """
            )


        if operation == "write":

            return self.query(
                """
                CREATE (
                    temp:BenchmarkTemp {
                        temp_id: $temp_id
                    }
                )

                RETURN true AS success
                """,
                params
            )


        if operation == "delete_temp":

            return self.query(
                """
                MATCH (
                    temp:BenchmarkTemp {
                        temp_id: $temp_id
                    }
                )

                DELETE temp

                RETURN true AS success
                """,
                params
            )


        raise ValueError(
            f"Unknown operation: {operation}"
        )


    # ======================================
    # CLEAR GRAPH
    # ======================================

    def clear(self):

        self.query(
            """
            MATCH (n)
            DETACH DELETE n
            """
        )


    # ======================================
    # CREATE INDEX
    # ======================================

    def create_indexes(self):

        indexes = [
            """
            CREATE INDEX FOR (u:User)
            ON (u.user_id)
            """,

            """
            CREATE INDEX FOR (u:User)
            ON (u.group)
            """
        ]

        for statement in indexes:

            try:

                self.query(statement)

            except Exception as error:

                message = str(
                    error
                ).lower()

                if (
                    "already exists"
                    not in message
                    and
                    "already indexed"
                    not in message
                ):

                    raise


    # ======================================
    # CLOSE
    # ======================================

    def close(self):

        if self.client is not None:

            try:
                self.client.close()

            except Exception:
                pass

            self.client = None