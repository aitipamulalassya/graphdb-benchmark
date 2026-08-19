import json
import time
from pathlib import Path

from dotenv import load_dotenv

from connectors.cognodb import CognoDBAdapter


# -------------------------------------
# Load environment variables
# -------------------------------------

load_dotenv()


# -------------------------------------
# Project paths
# -------------------------------------
ROOT = Path(
    __file__
).resolve().parent

NODES_FILE = (
    ROOT
    / "data"
    / "prepared"
    / "nodes.json"
)

EDGES_FILE = (
    ROOT
    / "data"
    / "prepared"
    / "edges.json"
)

# -------------------------------------
# Configuration
# -------------------------------------

BATCH_SIZE = 1000


# -------------------------------------
# Load JSON
# -------------------------------------

def load_json(path):

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# -------------------------------------
# Main
# -------------------------------------

def main():

    print()
    print("======================================")
    print("COGNODB DATA LOADING")
    print("======================================")

    print()
    print("Reading nodes...")

    nodes = load_json(
        NODES_FILE
    )

    print(
        f"Nodes found: {len(nodes):,}"
    )

    print()
    print("Reading relationships...")

    relationships = load_json(
        EDGES_FILE
    )

    print(
        f"Relationships found: "
        f"{len(relationships):,}"
    )


    # ---------------------------------
    # Connect
    # ---------------------------------

    database = CognoDBAdapter()

    try:

        database.connect()

        database.verify()


        # ---------------------------------
        # Clear previous benchmark data
        # ---------------------------------

        database.reset()


        # ---------------------------------
        # Create indexes
        # ---------------------------------

        database.create_schema()


        # ---------------------------------
        # Load nodes
        # ---------------------------------

        print()
        print("Loading nodes...")

        start_time = time.perf_counter()

        database.load_nodes(
            nodes,
            BATCH_SIZE
        )

        node_time = (
            time.perf_counter()
            - start_time
        )


        # ---------------------------------
        # Load relationships
        # ---------------------------------

        print()
        print("Loading relationships...")

        start_time = time.perf_counter()

        database.load_relationships(
            relationships,
            BATCH_SIZE
        )

        relationship_time = (
            time.perf_counter()
            - start_time
        )


        # ---------------------------------
        # Verify counts
        # ---------------------------------

        print()
        print("Verifying database...")

        database_nodes = database.run(
            "count_nodes",
            {}
        )

        database_relationships = database.run(
            "count_relationships",
            {}
        )


        # ---------------------------------
        # Print results
        # ---------------------------------

        print()
        print("======================================")
        print("COGNODB LOAD COMPLETE")
        print("======================================")

        print(
            f"Expected nodes: "
            f"{len(nodes):,}"
        )

        print(
            f"Database nodes: "
            f"{database_nodes:,}"
        )

        print()

        print(
            f"Expected relationships: "
            f"{len(relationships):,}"
        )

        print(
            f"Database relationships: "
            f"{database_relationships:,}"
        )

        print()

        print(
            f"Node loading time: "
            f"{node_time:.2f} seconds"
        )

        print(
            f"Relationship loading time: "
            f"{relationship_time:.2f} seconds"
        )

        print()

        print(
            f"Nodes/second: "
            f"{len(nodes) / node_time:.2f}"
        )

        print(
            f"Relationships/second: "
            f"{len(relationships) / relationship_time:.2f}"
        )

        print("======================================")


        # ---------------------------------
        # Validate
        # ---------------------------------

        if database_nodes != len(nodes):

            raise RuntimeError(
                "NODE COUNT DOES NOT MATCH!"
            )


        if database_relationships != len(
            relationships
        ):

            raise RuntimeError(
                "RELATIONSHIP COUNT DOES NOT MATCH!"
            )


        print()
        print(
            "SUCCESS: Dataset matches exactly."
        )


    finally:

        database.close()


# -------------------------------------
# Run
# -------------------------------------

if __name__ == "__main__":

    main()