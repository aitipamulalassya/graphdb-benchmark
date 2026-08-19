import os
import time

from dotenv import load_dotenv
from neo4j import GraphDatabase


load_dotenv()


class MemgraphAdapter:

    def __init__(self):

        self.host = os.getenv(
            "MEMGRAPH_HOST"
        )

        self.port = os.getenv(
            "MEMGRAPH_PORT",
            "7687"
        )

        self.username = os.getenv(
            "MEMGRAPH_USERNAME"
        )

        self.password = os.getenv(
            "MEMGRAPH_PASSWORD"
        )

        self.ssl = os.getenv(
            "MEMGRAPH_SSL",
            "true"
        ).lower() == "true"

        self.driver = None


    # ======================================
    # CONNECT
    # ======================================

    def connect(self):

        if not self.host:
            raise ValueError(
                "MEMGRAPH_HOST is not configured."
            )

        if not self.username:
            raise ValueError(
                "MEMGRAPH_USERNAME is not configured."
            )

        if not self.password:
            raise ValueError(
                "MEMGRAPH_PASSWORD is not configured."
            )


        if self.ssl:

            uri = (
                f"bolt+ssc://"
                f"{self.host}:"
                f"{self.port}"
            )

        else:

            uri = (
                f"bolt://"
                f"{self.host}:"
                f"{self.port}"
            )


        self.driver = GraphDatabase.driver(
            uri,
            auth=(
                self.username,
                self.password
            ),
            max_connection_lifetime=300,
            max_connection_pool_size=10,
            connection_timeout=30,
            connection_acquisition_timeout=30
        )


        self.verify()


        print(
            "Memgraph connection successful"
        )


    # ======================================
    # VERIFY
    # ======================================

    def verify(self):

        if self.driver is None:

            raise RuntimeError(
                "Memgraph driver is not connected."
            )


        self.driver.verify_connectivity()


    # ======================================
    # RUN QUERY
    # ======================================

    def run(
        self,
        query,
        params=None
    ):

        if self.driver is None:

            raise RuntimeError(
                "Memgraph driver is not connected."
            )


        if params is None:

            params = {}


        with self.driver.session() as session:

            result = session.run(
                query,
                params
            )

            return list(
                result
            )


    # ======================================
    # CLOSE
    # ======================================

    def close(self):

        if self.driver is not None:

            self.driver.close()

            self.driver = None