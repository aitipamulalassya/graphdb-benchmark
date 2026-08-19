import json
import sys
from pathlib import Path


# ======================================
# PROJECT ROOT
# ======================================

ROOT = (
    Path(__file__)
    .resolve()
    .parent
)

sys.path.insert(
    0,
    str(ROOT)
)


# ======================================
# IMPORT
# ======================================

from connectors.arangodb import ArangoDBAdapter


# ======================================
# FILES
# ======================================

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


# ======================================
# COLLECTION NAMES
# ======================================

VERTEX_COLLECTION = "users"
EDGE_COLLECTION = "votes"


# ======================================
# BATCH SIZE
# ======================================

BATCH_SIZE = 500


# ======================================
# LOAD JSON
# ======================================

def load_json(file_path):

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# ======================================
# CREATE COLLECTIONS
# ======================================

def create_collections(database):

    print()
    print("Creating ArangoDB collections...")

    db = database.db

    # ----------------------------------
    # Vertex collection
    # ----------------------------------

    if db.has_collection(
        VERTEX_COLLECTION
    ):

        print(
            f"Collection already exists: "
            f"{VERTEX_COLLECTION}"
        )

    else:

        db.create_collection(
            VERTEX_COLLECTION
        )

        print(
            f"Created collection: "
            f"{VERTEX_COLLECTION}"
        )


    # ----------------------------------
    # Edge collection
    # ----------------------------------

    if db.has_collection(
        EDGE_COLLECTION
    ):

        print(
            f"Collection already exists: "
            f"{EDGE_COLLECTION}"
        )

    else:

        db.create_collection(
            EDGE_COLLECTION,
            edge=True
        )

        print(
            f"Created edge collection: "
            f"{EDGE_COLLECTION}"
        )


# ======================================
# CLEAR COLLECTIONS
# ======================================

def clear_collections(database):

    print()
    print(
        "Clearing existing ArangoDB data..."
    )

    db = database.db


    # ----------------------------------
    # Clear vertices
    # ----------------------------------

    if db.has_collection(
        VERTEX_COLLECTION
    ):

        collection = db.collection(
            VERTEX_COLLECTION
        )

        collection.truncate()

        print(
            "Existing nodes cleared."
        )


    # ----------------------------------
    # Clear edges
    # ----------------------------------

    if db.has_collection(
        EDGE_COLLECTION
    ):

        collection = db.collection(
            EDGE_COLLECTION
        )

        collection.truncate()

        print(
            "Existing relationships cleared."
        )


# ======================================
# CREATE INDEXES
# ======================================

def create_indexes(database):

    print()
    print(
        "Creating ArangoDB indexes..."
    )

    collection = database.db.collection(
        VERTEX_COLLECTION
    )

    # ==================================
    # user_id index
    # ==================================

    collection.add_index(
        {
            "type": "persistent",
            "fields": [
                "user_id"
            ],
            "unique": True
        }
    )

    print(
        "Created index: user_id"
    )

    # ==================================
    # group index
    # ==================================

    collection.add_index(
        {
            "type": "persistent",
            "fields": [
                "group"
            ],
            "unique": False
        }
    )

    print(
        "Created index: group"
    )

# ======================================
# LOAD NODES
# ======================================

def load_nodes(
    database,
    nodes
):

    print()
    print(
        "Loading nodes..."
    )

    collection = database.db.collection(
        VERTEX_COLLECTION
    )


    total = len(nodes)

    loaded = 0


    for start in range(
        0,
        total,
        BATCH_SIZE
    ):

        batch = nodes[
            start:
            start + BATCH_SIZE
        ]


        documents = []


        for node in batch:

            user_id = int(
                node["user_id"]
            )

            group = int(
                node["group"]
            )


            documents.append(
                {
                    "_key": str(
                        user_id
                    ),

                    "user_id": user_id,

                    "group": group
                }
            )


        collection.insert_many(
            documents,
            overwrite=True
        )


        loaded += len(
            documents
        )


        print(
            f"Nodes loaded: "
            f"{loaded:,}/{total:,}"
        )


# ======================================
# LOAD RELATIONSHIPS
# ======================================

def load_relationships(
    database,
    edges
):

    print()
    print(
        "Loading relationships..."
    )

    collection = database.db.collection(
        EDGE_COLLECTION
    )


    total = len(edges)

    loaded = 0


    for start in range(
        0,
        total,
        BATCH_SIZE
    ):

        batch = edges[
            start:
            start + BATCH_SIZE
        ]


        documents = []


        for index, edge in enumerate(
            batch
        ):

            src = int(
                edge["src"]
            )

            dst = int(
                edge["dst"]
            )


            documents.append(
                {
                    "_key": (
                        f"{src}_{dst}_"
                        f"{start + index}"
                    ),

                    "_from": (
                        f"{VERTEX_COLLECTION}/"
                        f"{src}"
                    ),

                    "_to": (
                        f"{VERTEX_COLLECTION}/"
                        f"{dst}"
                    )
                }
            )


        collection.insert_many(
            documents,
            overwrite=True
        )


        loaded += len(
            documents
        )


        print(
            f"Relationships loaded: "
            f"{loaded:,}/{total:,}"
        )


# ======================================
# VERIFY NODE COUNT
# ======================================

def verify_node_count(
    database,
    expected
):

    print()
    print(
        "Verifying node count..."
    )


    collection = database.db.collection(
        VERTEX_COLLECTION
    )


    actual = collection.count()


    print(
        f"ArangoDB nodes: "
        f"{actual:,}"
    )


    if actual != expected:

        raise RuntimeError(
            "Node count verification failed: "
            f"expected {expected}, "
            f"got {actual}"
        )


    print(
        "Node count verification: PASS"
    )


# ======================================
# VERIFY RELATIONSHIP COUNT
# ======================================

def verify_relationship_count(
    database,
    expected
):

    print()
    print(
        "Verifying relationship count..."
    )


    collection = database.db.collection(
        EDGE_COLLECTION
    )


    actual = collection.count()


    print(
        f"ArangoDB relationships: "
        f"{actual:,}"
    )


    if actual != expected:

        raise RuntimeError(
            "Relationship count verification "
            f"failed: expected {expected}, "
            f"got {actual}"
        )


    print(
        "Relationship count verification: PASS"
    )


# ======================================
# MAIN
# ======================================

def main():

    print()
    print(
        "======================================"
    )

    print(
        "ARANGODB DATA LOADING"
    )

    print(
        "======================================"
    )


    # ----------------------------------
    # Read nodes
    # ----------------------------------

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


    # ----------------------------------
    # Read edges
    # ----------------------------------

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


    # ----------------------------------
    # Connect
    # ----------------------------------

    database = ArangoDBAdapter()


    try:

        database.connect()


        # ----------------------------------
        # Collections
        # ----------------------------------

        create_collections(
            database
        )


        # ----------------------------------
        # Clear existing data
        # ----------------------------------

        clear_collections(
            database
        )


        # ----------------------------------
        # Indexes
        # ----------------------------------

        create_indexes(
            database
        )


        # ----------------------------------
        # Load nodes
        # ----------------------------------

        load_nodes(
            database,
            nodes
        )


        # ----------------------------------
        # Load relationships
        # ----------------------------------

        load_relationships(
            database,
            edges
        )


        # ----------------------------------
        # Verify
        # ----------------------------------

        verify_node_count(
            database,
            len(nodes)
        )


        verify_relationship_count(
            database,
            len(edges)
        )


        # ----------------------------------
        # Complete
        # ----------------------------------

        print()
        print(
            "======================================"
        )

        print(
            "ARANGODB DATA LOADING COMPLETE"
        )

        print(
            "======================================"
        )

        print()
        print(
            "STATUS: SUCCESS"
        )

        print()
        print(
            "All Wiki-Vote data was loaded "
            "successfully into ArangoDB."
        )


    finally:

        database.close()


# ======================================
# ENTRY POINT
# ======================================

if __name__ == "__main__":

    main()