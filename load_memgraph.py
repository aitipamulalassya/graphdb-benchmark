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


# ==========================================
# IMPORT CONNECTOR
# ==========================================

sys.path.insert(
    0,
    str(ROOT)
)

from connectors.memgraph import MemgraphAdapter


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
# CLEAR DATABASE
# ==========================================

def clear_database(database):

    print()
    print(
        "Clearing existing Memgraph data..."
    )

    database.run(
        """
        MATCH (n)
        DETACH DELETE n
        """
    )

    print(
        "Existing Memgraph data cleared."
    )


# ==========================================
# CREATE INDEXES
# ==========================================

def create_indexes(database):

    print()
    print(
        "Creating Memgraph indexes..."
    )

    # user_id index

    try:

        database.run(
            """
            CREATE INDEX ON :User(user_id)
            """
        )

        print(
            "User user_id index created."
        )

    except Exception as error:

        message = str(error).lower()

        if (
            "already exists" in message
            or
            "exists" in message
        ):

            print(
                "User user_id index already exists."
            )

        else:

            raise


    # group index

    try:

        database.run(
            """
            CREATE INDEX ON :User(group)
            """
        )

        print(
            "User group index created."
        )

    except Exception as error:

        message = str(error).lower()

        if (
            "already exists" in message
            or
            "exists" in message
        ):

            print(
                "User group index already exists."
            )

        else:

            raise


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


        database.run(
            """
            UNWIND $rows AS row

            CREATE (
                u:User
            )

            SET
                u.user_id = row.user_id,
                u.group = row.group
            """,
            {
                "rows": batch
            }
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


        database.run(
            """
            UNWIND $rows AS row

            MATCH (
                source:User {
                    user_id: row.src
                }
            )

            MATCH (
                target:User {
                    user_id: row.dst
                }
            )

            CREATE (
                source
            )-[:VOTE]->(
                target
            )
            """,
            {
                "rows": batch
            }
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


    result = database.run(
        """
        MATCH (n)
        RETURN count(n) AS count
        """
    )


    actual_nodes = (
        result[0]["count"]
    )


    print(
        f"Memgraph nodes: "
        f"{actual_nodes:,}"
    )


    print()
    print(
        "Verifying relationship count..."
    )


    result = database.run(
        """
        MATCH ()-[r]->()
        RETURN count(r) AS count
        """
    )


    actual_relationships = (
        result[0]["count"]
    )


    print(
        f"Memgraph relationships: "
        f"{actual_relationships:,}"
    )


    print()


    if actual_nodes == expected_nodes:

        print(
            "Node count verification: PASS"
        )

    else:

        print(
            "Node count verification: FAIL"
        )


    if (
        actual_relationships
        ==
        expected_relationships
    ):

        print(
            "Relationship count verification: PASS"
        )

    else:

        print(
            "Relationship count verification: FAIL"
        )


    return (
        actual_nodes == expected_nodes
        and
        actual_relationships
        == expected_relationships
    )


# ==========================================
# MAIN
# ==========================================

def main():

    print()
    print(
        "======================================"
    )

    print(
        "MEMGRAPH DATA LOADING"
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

    database = MemgraphAdapter()


    try:

        database.connect()


        # ----------------------------------
        # Clear
        # ----------------------------------

        clear_database(
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

        success = verify_counts(
            database,
            len(nodes),
            len(edges)
        )


        # ----------------------------------
        # Final status
        # ----------------------------------

        print()
        print(
            "======================================"
        )

        print(
            "MEMGRAPH DATA LOADING COMPLETE"
        )

        print(
            "======================================"
        )


        print()


        if success:

            print(
                "STATUS: SUCCESS"
            )

            print()

            print(
                "All Wiki-Vote data was loaded "
                "successfully into Memgraph."
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