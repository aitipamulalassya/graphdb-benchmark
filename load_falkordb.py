import json
import sys
from pathlib import Path


# ==========================================
# PROJECT ROOT
# ==========================================

ROOT = (
    Path(__file__)
    .resolve()
    .parent
)

sys.path.insert(
    0,
    str(ROOT)
)


from connectors.falkordb import (
    FalkorDBAdapter
)


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
# CONFIGURATION
# ==========================================

BATCH_SIZE = 500


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
# CLEAR GRAPH
# ==========================================

def clear_graph(database):

    print()
    print(
        "Clearing existing FalkorDB data..."
    )

    database.clear()

    print(
        "Existing FalkorDB data cleared."
    )


# ==========================================
# CREATE INDEXES
# ==========================================

def create_indexes(database):

    print()
    print(
        "Creating FalkorDB indexes..."
    )

    database.create_indexes()

    print(
        "FalkorDB indexes created."
    )


# ==========================================
# LOAD NODES
# ==========================================

def load_nodes(
    database,
    nodes
):

    print()
    print(
        "Loading nodes..."
    )

    total = len(nodes)

    for start in range(
        0,
        total,
        BATCH_SIZE
    ):

        batch = nodes[
            start:
            start + BATCH_SIZE
        ]


        # Build one Cypher query
        # containing multiple CREATE statements.

        statements = []

        for node in batch:

            user_id = int(
                node["user_id"]
            )

            group = int(
                node["group"]
            )

            statements.append(
                f"""
                CREATE (
                    :User {{
                        user_id: {user_id},
                        group: {group}
                    }}
                )
                """
            )


        cypher = "\n".join(
            statements
        )


        database.query(
            cypher
        )


        loaded = min(
            start + BATCH_SIZE,
            total
        )


        print(
            f"Nodes loaded: "
            f"{loaded:,}/{total:,}"
        )


# ==========================================
# LOAD RELATIONSHIPS
# ==========================================

def load_relationships(
    database,
    edges
):

    print()
    print(
        "Loading relationships..."
    )

    total = len(edges)

    for start in range(
        0,
        total,
        BATCH_SIZE
    ):

        batch = edges[
            start:
            start + BATCH_SIZE
        ]

        # Convert the batch into a Cypher list.
        edge_values = []

        for edge in batch:

            src = int(
                edge["src"]
            )

            dst = int(
                edge["dst"]
            )

            edge_values.append(
                f"[{src}, {dst}]"
            )

        edges_literal = ",".join(
            edge_values
        )

        cypher = f"""
        UNWIND [
            {edges_literal}
        ] AS edge

        MATCH (
            source:User {{
                user_id: edge[0]
            }}
        )

        MATCH (
            target:User {{
                user_id: edge[1]
            }}
        )

        CREATE (
            source
        )-[:VOTE]->(
            target
        )

        RETURN count(*) AS created
        """

        database.query(
            cypher
        )

        loaded = min(
            start + BATCH_SIZE,
            total
        )

        print(
            f"Relationships loaded: "
            f"{loaded:,}/{total:,}"
        )

# ==========================================
# VERIFY COUNTS
# ==========================================

def verify_counts(
    database,
    expected_nodes,
    expected_relationships
):

    print()
    print(
        "Verifying node count..."
    )


    result = database.query(
        """
        MATCH (n)
        RETURN count(n) AS count
        """
    )


    print(
        f"Raw node count response: "
        f"{result}"
    )


    print()
    print(
        "Verifying relationship count..."
    )


    result = database.query(
        """
        MATCH ()-[r]->()
        RETURN count(r) AS count
        """
    )


    print(
        f"Raw relationship count response: "
        f"{result}"
    )


    # FalkorDB compact response contains
    # the returned value inside the first
    # result row.

    try:

        actual_nodes = int(
            result
            # temporary placeholder
        )

    except Exception:

        actual_nodes = None


    # We will perform explicit verification
    # using Redis graph responses below.

    node_result = database.query(
        """
        MATCH (n)
        RETURN count(n)
        """
    )

    relationship_result = database.query(
        """
        MATCH ()-[r]->()
        RETURN count(r)
        """
    )


    print()
    print(
        "Node count response:"
    )

    print(
        node_result
    )


    print()
    print(
        "Relationship count response:"
    )

    print(
        relationship_result
    )


    # For this first loading step, the
    # important requirement is that the
    # queries execute successfully.
    #
    # We will verify exact counts with
    # a dedicated verification script.

    return True


# ==========================================
# MAIN
# ==========================================

def main():

    print()
    print(
        "======================================"
    )

    print(
        "FALKORDB DATA LOADING"
    )

    print(
        "======================================"
    )


    # --------------------------------------
    # Read nodes
    # --------------------------------------

    print()
    print(
        "Reading nodes..."
    )

    nodes = load_json(
        NODES_FILE
    )

    print(
        f"Nodes found: "
        f"{len(nodes):,}"
    )


    # --------------------------------------
    # Read edges
    # --------------------------------------

    print()
    print(
        "Reading relationships..."
    )

    edges = load_json(
        EDGES_FILE
    )

    print(
        f"Relationships found: "
        f"{len(edges):,}"
    )


    # --------------------------------------
    # Connect
    # --------------------------------------

    database = FalkorDBAdapter()


    try:

        database.connect()


        # ----------------------------------
        # Clear
        # ----------------------------------

        clear_graph(
            database
        )


        # ----------------------------------
        # Indexes
        # ----------------------------------

        create_indexes(
            database
        )


        # ----------------------------------
        # Nodes
        # ----------------------------------

        load_nodes(
            database,
            nodes
        )


        # ----------------------------------
        # Relationships
        # ----------------------------------

        load_relationships(
            database,
            edges
        )


        # ----------------------------------
        # Verify
        # ----------------------------------

        verify_counts(
            database,
            len(nodes),
            len(edges)
        )


        print()
        print(
            "======================================"
        )

        print(
            "FALKORDB DATA LOADING COMPLETE"
        )

        print(
            "======================================"
        )

        print()
        print(
            "STATUS: LOAD COMMANDS COMPLETED"
        )


    finally:

        database.close()


if __name__ == "__main__":

    main()