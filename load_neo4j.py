import json
import sys
from pathlib import Path


# ==========================================
# PROJECT ROOT
# ==========================================

ROOT = Path(
    __file__
).resolve().parent


# ==========================================
# IMPORT CONNECTOR
# ==========================================

sys.path.insert(
    0,
    str(ROOT)
)

from connectors.neo4j import Neo4jAdapter


# ==========================================
# DATA FILES
# ==========================================

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


# ==========================================
# LOAD JSON
# ==========================================

def load_json(path):

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# ==========================================
# MAIN
# ==========================================

def main():

    print()
    print("======================================")
    print("NEO4J DATA LOADING")
    print("======================================")


    # --------------------------------------
    # Read nodes
    # --------------------------------------

    print()
    print("Reading nodes...")

    nodes = load_json(
        NODES_FILE
    )

    print(
        f"Nodes found: {len(nodes):,}"
    )


    # --------------------------------------
    # Read edges
    # --------------------------------------

    print()
    print("Reading relationships...")

    edges = load_json(
        EDGES_FILE
    )

    print(
        f"Relationships found: {len(edges):,}"
    )


    # --------------------------------------
    # Connect
    # --------------------------------------

    database = Neo4jAdapter()

    try:

        database.connect()

        database.verify()


        # ----------------------------------
        # Clear existing data
        # ----------------------------------

        print()
        print(
            "Clearing existing Neo4j data..."
        )

        database.reset()


        # ----------------------------------
        # Create indexes
        # ----------------------------------

        print()
        print(
            "Creating Neo4j indexes..."
        )

        database.create_schema()


        # ----------------------------------
        # Load nodes
        # ----------------------------------

        print()
        print(
            "Loading nodes..."
        )

        database.load_nodes(
            nodes,
            batch_size=500
        )


        # ----------------------------------
        # Load relationships
        # ----------------------------------

        print()
        print(
            "Loading relationships..."
        )

        database.load_relationships(
            edges,
            batch_size=500
        )


        # ----------------------------------
        # Verify nodes
        # ----------------------------------

        print()
        print(
            "Verifying node count..."
        )

        node_count = database.run(
            "count_nodes",
            {}
        )

        print(
            f"Neo4j nodes: "
            f"{node_count:,}"
        )


        # ----------------------------------
        # Verify relationships
        # ----------------------------------

        print()
        print(
            "Verifying relationship count..."
        )

        relationship_count = database.run(
            "count_relationships",
            {}
        )

        print(
            f"Neo4j relationships: "
            f"{relationship_count:,}"
        )


        # ----------------------------------
        # Verify expected values
        # ----------------------------------

        print()

        if node_count == len(nodes):

            print(
                "Node count verification: PASS"
            )

        else:

            print(
                "Node count verification: FAIL"
            )


        if relationship_count == len(edges):

            print(
                "Relationship count verification: PASS"
            )

        else:

            print(
                "Relationship count verification: FAIL"
            )


        # ----------------------------------
        # Final status
        # ----------------------------------

        print()
        print("======================================")
        print("NEO4J DATA LOADING COMPLETE")
        print("======================================")

        print()

        if (
            node_count == len(nodes)
            and
            relationship_count == len(edges)
        ):

            print(
                "STATUS: SUCCESS"
            )

            print()
            print(
                "All Wiki-Vote data was loaded "
                "successfully into Neo4j."
            )

        else:

            print(
                "STATUS: CHECK REQUIRED"
            )


    finally:

        database.close()


# ==========================================
# ENTRY POINT
# ==========================================

if __name__ == "__main__":

    main()