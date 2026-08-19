import os

from dotenv import load_dotenv
from neo4j import GraphDatabase

from .base import BenchmarkAdapter


# ==========================================
# LOAD ENVIRONMENT
# ==========================================

load_dotenv()


class Neo4jAdapter(BenchmarkAdapter):

    name = "neo4j"

    # ======================================
    # INITIALIZATION
    # ======================================

    def __init__(self):

        self.uri = os.getenv(
            "NEO4J_URI"
        )

        self.username = os.getenv(
            "NEO4J_USERNAME",
            "neo4j"
        )

        self.password = os.getenv(
            "NEO4J_PASSWORD"
        )

        self.database = os.getenv(
            "NEO4J_DATABASE",
            "neo4j"
        )

        self.driver = None

        if not self.uri:

            raise ValueError(
                "NEO4J_URI is missing from .env"
            )

        if not self.password:

            raise ValueError(
                "NEO4J_PASSWORD is missing from .env"
            )


    # ======================================
    # CREATE DRIVER
    # ======================================

    def _create_driver(self):

        self.driver = GraphDatabase.driver(
            self.uri,
            auth=(
                self.username,
                self.password
            )
        )


    # ======================================
    # CONNECT
    # ======================================

    def connect(self):

        if self.driver is None:

            self._create_driver()


    # ======================================
    # VERIFY
    # ======================================

    def verify(self):

        if self.driver is None:

            self.connect()

        self.driver.verify_connectivity()

        print(
            "Neo4j connection successful"
        )


    # ======================================
    # CLOSE
    # ======================================

    def close(self):

        if self.driver:

            try:

                self.driver.close()

            except Exception:

                pass

            self.driver = None


    # ======================================
    # READ QUERY
    # ======================================

    def _execute_read(
        self,
        query,
        parameters=None
    ):

        if self.driver is None:

            self.connect()

        with self.driver.session(
            database=self.database
        ) as session:

            result = session.run(
                query,
                parameters or {}
            )

            records = list(result)

            result.consume()

            return records


    # ======================================
    # WRITE QUERY
    # ======================================

    def _execute_write(
        self,
        query,
        parameters=None
    ):

        if self.driver is None:

            self.connect()

        with self.driver.session(
            database=self.database
        ) as session:

            result = session.run(
                query,
                parameters or {}
            )

            result.consume()


    # ======================================
    # RESET DATABASE
    # ======================================

    def reset(self):

        self._execute_write(
            """
            MATCH (n)
            DETACH DELETE n
            """
        )

        print(
            "Existing Neo4j data cleared."
        )


    # ======================================
    # CREATE SCHEMA
    # ======================================

    def create_schema(self):

        queries = [

            """
            CREATE INDEX user_id_index IF NOT EXISTS
            FOR (u:User)
            ON (u.user_id)
            """,

            """
            CREATE INDEX group_index IF NOT EXISTS
            FOR (u:User)
            ON (u.group)
            """

        ]

        for query in queries:

            self._execute_write(
                query
            )

        print(
            "Neo4j indexes created."
        )


    # ======================================
    # LOAD NODES
    # ======================================

    def load_nodes(
        self,
        rows,
        batch_size=1000
    ):

        query = """
        UNWIND $rows AS row

        CREATE (
            :User {
                user_id: row.user_id,
                group: row.group
            }
        )
        """

        total = len(rows)

        for start in range(
            0,
            total,
            batch_size
        ):

            batch = rows[
                start:start + batch_size
            ]

            self._execute_write(
                query,
                {
                    "rows": batch
                }
            )

            loaded = min(
                start + batch_size,
                total
            )

            print(
                f"Nodes loaded: "
                f"{loaded:,}/{total:,}"
            )


    # ======================================
    # LOAD RELATIONSHIPS
    # ======================================

    def load_relationships(
        self,
        rows,
        batch_size=1000
    ):

        query = """
        UNWIND $rows AS row

        MATCH (
            source:User {
                user_id: row.src
            }
        )

        MATCH (
            destination:User {
                user_id: row.dst
            }
        )

        CREATE (
            source
        )-[:VOTES]->(
            destination
        )
        """

        total = len(rows)

        for start in range(
            0,
            total,
            batch_size
        ):

            batch = rows[
                start:start + batch_size
            ]

            self._execute_write(
                query,
                {
                    "rows": batch
                }
            )

            loaded = min(
                start + batch_size,
                total
            )

            print(
                f"Relationships loaded: "
                f"{loaded:,}/{total:,}"
            )


    # ======================================
    # RUN BENCHMARK OPERATION
    # ======================================

    def run(
        self,
        operation,
        params
    ):

        # ----------------------------------
        # COUNT NODES
        # ----------------------------------

        if operation == "count_nodes":

            records = self._execute_read(
                """
                MATCH (u:User)

                RETURN count(u) AS count
                """
            )

            return records[0]["count"]


        # ----------------------------------
        # COUNT RELATIONSHIPS
        # ----------------------------------

        if operation == "count_relationships":

            records = self._execute_read(
                """
                MATCH ()-[r:VOTES]->()

                RETURN count(r) AS count
                """
            )

            return records[0]["count"]


        # ----------------------------------
        # 1-HOP
        # ----------------------------------

        if operation == "traversal_1":

            records = self._execute_read(
                """
                MATCH (
                    start:User {
                        user_id: $start
                    }
                )

                MATCH (
                    start
                )-[:VOTES]->(
                    target:User
                )

                RETURN count(target) AS count
                """,
                {
                    "start": params["start"]
                }
            )

            return records[0]["count"]


        # ----------------------------------
        # 2-HOP
        # ----------------------------------

        if operation == "traversal_2":

            records = self._execute_read(
                """
                MATCH (
                    start:User {
                        user_id: $start
                    }
                )

                MATCH (
                    start
                )-[:VOTES*2]->(
                    target:User
                )

                RETURN count(target) AS count
                """,
                {
                    "start": params["start"]
                }
            )

            return records[0]["count"]


        # ----------------------------------
        # 3-HOP
        # ----------------------------------

        if operation == "traversal_3":

            records = self._execute_read(
                """
                MATCH (
                    start:User {
                        user_id: $start
                    }
                )

                MATCH (
                    start
                )-[:VOTES*3]->(
                    target:User
                )

                RETURN count(target) AS count
                """,
                {
                    "start": params["start"]
                }
            )

            return records[0]["count"]


        # ----------------------------------
        # POINT LOOKUP
        # ----------------------------------

        if operation == "point_lookup":

            records = self._execute_read(
                """
                MATCH (
                    u:User {
                        user_id: $user_id
                    }
                )

                RETURN u.user_id AS user_id
                """,
                {
                    "user_id": params["user_id"]
                }
            )

            if records:

                return records[0]["user_id"]

            return None


        # ----------------------------------
        # INDEXED LOOKUP
        # ----------------------------------

        if operation == "indexed_lookup":

            records = self._execute_read(
                """
                MATCH (
                    u:User {
                        group: $group
                    }
                )

                RETURN count(u) AS count
                """,
                {
                    "group": params["group"]
                }
            )

            return records[0]["count"]


        # ----------------------------------
        # AGGREGATION
        # ----------------------------------

        if operation == "aggregation":

            records = self._execute_read(
                """
                MATCH (u:User)

                RETURN
                    u.group AS group,
                    count(u) AS count

                ORDER BY group
                """
            )

            return records


        # ----------------------------------
        # WRITE
        # ----------------------------------

        if operation == "write":

            temp_id = params["temp_id"]

            self._execute_write(
                """
                CREATE (
                    :User {
                        user_id: $temp_id,
                        group: 999
                    }
                )
                """,
                {
                    "temp_id": temp_id
                }
            )

            self._execute_write(
                """
                MATCH (
                    u:User {
                        user_id: $temp_id
                    }
                )

                DETACH DELETE u
                """,
                {
                    "temp_id": temp_id
                }
            )

            return True


        raise ValueError(
            f"Unknown benchmark operation: "
            f"{operation}"
        )


    # ======================================
    # RESOURCE INFORMATION
    # ======================================

    def resource_info(self):

        return {

            "platform": "neo4j",

            "database":
                self.database,

            "resource_note":
                "Neo4j AuraDB Free instance."

        }