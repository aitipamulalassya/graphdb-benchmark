import os

from arango import ArangoClient
from dotenv import load_dotenv


load_dotenv()


class ArangoDBAdapter:

    def __init__(self):

        self.url = os.getenv("ARANGO_URL")
        self.username = os.getenv("ARANGO_USERNAME")
        self.password = os.getenv("ARANGO_PASSWORD")

        self.database_name = os.getenv(
            "ARANGO_DATABASE",
            "benchmark"
        )

        self.client = None
        self.db = None

        self.vertex_collection = "users"
        self.edge_collection = "votes"


    # ======================================
    # CONNECT
    # ======================================

    def connect(self):

        if not self.url:
            raise ValueError(
                "ARANGO_URL is not configured"
            )

        if not self.username:
            raise ValueError(
                "ARANGO_USERNAME is not configured"
            )

        if not self.password:
            raise ValueError(
                "ARANGO_PASSWORD is not configured"
            )

        self.client = ArangoClient(
            hosts=self.url
        )

        self.db = self.client.db(
            self.database_name,
            username=self.username,
            password=self.password
        )

        # Force real connection
        self.db.version()

        print(
            "ArangoDB connection successful"
        )


    # ======================================
    # CLOSE
    # ======================================

    def close(self):

        self.client = None
        self.db = None


    # ======================================
    # VERIFY
    # ======================================

    def verify(self):

        if self.db is None:
            raise RuntimeError(
                "ArangoDB is not connected"
            )

        return self.db.version()


    # ======================================
    # RUN
    # ======================================

    def run(
        self,
        operation,
        params=None
    ):

        if params is None:
            params = {}


        # ==================================
        # RETURN 1
        # ==================================

        if operation == "return_1":

            cursor = self.db.aql.execute(
                "RETURN 1"
            )

            return next(cursor)


        # ==================================
        # NODE COUNT
        # ==================================

        if operation == "node_count":

            query = f"""
            RETURN LENGTH(
                FOR u IN `{self.vertex_collection}`
                    RETURN u
            )
            """

            cursor = self.db.aql.execute(
                query
            )

            return next(cursor)


        # ==================================
        # 1-HOP TRAVERSAL
        # ==================================

        if operation == "traversal_1":

            query = f"""
            WITH `{self.vertex_collection}`
            FOR v, e, p IN 1..1
                OUTBOUND @start
                `{self.edge_collection}`
                OPTIONS {{
                    uniqueVertices: "path"
                }}
                COLLECT WITH COUNT INTO count
                RETURN count
            """

            start_vertex = (
                f"{self.vertex_collection}/"
                f"{params['start']}"
            )

            cursor = self.db.aql.execute(
                query,
                bind_vars={
                    "start": start_vertex
                }
            )

            return next(cursor)


        # ==================================
        # 2-HOP TRAVERSAL
        # ==================================

        if operation == "traversal_2":

            query = f"""
            WITH `{self.vertex_collection}`
            FOR v, e, p IN 2..2
                OUTBOUND @start
                `{self.edge_collection}`
                OPTIONS {{
                    uniqueVertices: "path"
                }}
                COLLECT WITH COUNT INTO count
                RETURN count
            """

            start_vertex = (
                f"{self.vertex_collection}/"
                f"{params['start']}"
            )

            cursor = self.db.aql.execute(
                query,
                bind_vars={
                    "start": start_vertex
                }
            )

            return next(cursor)


        # ==================================
        # 3-HOP TRAVERSAL
        # ==================================

        if operation == "traversal_3":

            query = f"""
            WITH `{self.vertex_collection}`
            FOR v, e, p IN 3..3
                OUTBOUND @start
                `{self.edge_collection}`
                OPTIONS {{
                    uniqueVertices: "path"
                }}
                COLLECT WITH COUNT INTO count
                RETURN count
            """

            start_vertex = (
                f"{self.vertex_collection}/"
                f"{params['start']}"
            )

            cursor = self.db.aql.execute(
                query,
                bind_vars={
                    "start": start_vertex
                }
            )

            return next(cursor)


        # ==================================
        # POINT LOOKUP
        # ==================================

        if operation == "point_lookup":

            query = f"""
            FOR u IN `{self.vertex_collection}`
                FILTER u.user_id == @user_id
                RETURN u
            """

            cursor = self.db.aql.execute(
                query,
                bind_vars={
                    "user_id": params["user_id"]
                }
            )

            return list(cursor)


        # ==================================
        # INDEXED LOOKUP
        # ==================================

        if operation == "indexed_lookup":

            query = f"""
            FOR u IN `{self.vertex_collection}`
                FILTER u.group == @group
                RETURN u
            """

            cursor = self.db.aql.execute(
                query,
                bind_vars={
                    "group": params["group"]
                }
            )

            return list(cursor)


        # ==================================
        # AGGREGATION
        # ==================================

        if operation == "aggregation":

            query = f"""
            FOR u IN `{self.vertex_collection}`
                COLLECT group = u.group
                AGGREGATE count = COUNT()
                SORT group
                RETURN {{
                    group: group,
                    count: count
                }}
            """

            cursor = self.db.aql.execute(
                query
            )

            return list(cursor)


        # ==================================
        # WRITE
        # ==================================

        if operation == "write":

            temp_id = params.get(
                "temp_id",
                999999
            )

            query = f"""
            INSERT {{
                _key: @key,
                user_id: @user_id,
                group: 0
            }}
            INTO `{self.vertex_collection}`
            RETURN true
            """

            cursor = self.db.aql.execute(
                query,
                bind_vars={
                    "key": str(temp_id),
                    "user_id": temp_id
                }
            )

            return next(cursor)


        # ==================================
        # DELETE TEMP
        # ==================================

        if operation == "delete_temp":

            query = f"""
            FOR u IN `{self.vertex_collection}`
                FILTER u.user_id == @user_id
                REMOVE u
                IN `{self.vertex_collection}`
            """

            self.db.aql.execute(
                query,
                bind_vars={
                    "user_id": params["temp_id"]
                }
            )

            return True


        # ==================================
        # UNKNOWN OPERATION
        # ==================================

        raise ValueError(
            f"Unknown operation: {operation}"
        )