import gzip
import json
import random
from pathlib import Path


# -----------------------------------------
# Paths
# -----------------------------------------

DATA_DIR = Path(__file__).resolve().parent

RAW_FILE = DATA_DIR / "raw" / "wiki-Vote.txt.gz"

PREPARED_DIR = DATA_DIR / "prepared"

NODES_FILE = PREPARED_DIR / "nodes.json"

EDGES_FILE = PREPARED_DIR / "edges.json"

START_NODES_FILE = PREPARED_DIR / "start_nodes.json"


# -----------------------------------------
# Create prepared directory
# -----------------------------------------

PREPARED_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# -----------------------------------------
# Prepare dataset
# -----------------------------------------

def prepare_dataset():

    if not RAW_FILE.exists():

        raise FileNotFoundError(
            f"Dataset not found: {RAW_FILE}\n"
            "Run download_dataset.py first."
        )

    print("Reading Wiki-Vote dataset...")

    edges = []

    node_ids = set()

    # -------------------------------------
    # Read compressed dataset
    # -------------------------------------

    with gzip.open(
        RAW_FILE,
        "rt",
        encoding="utf-8"
    ) as file:

        for line in file:

            line = line.strip()

            # Ignore empty lines
            if not line:
                continue

            # Ignore comments
            if line.startswith("#"):
                continue

            # Each line:
            # source destination

            parts = line.split()

            if len(parts) != 2:
                continue

            source = int(parts[0])

            destination = int(parts[1])

            # Save relationship

            edges.append(
                {
                    "src": source,
                    "dst": destination
                }
            )

            # Save nodes

            node_ids.add(source)

            node_ids.add(destination)


    # -------------------------------------
    # Create nodes
    # -------------------------------------

    nodes = []

    for node_id in sorted(node_ids):

        nodes.append(
            {
                "user_id": node_id,

                # Deterministic property
                # used for indexed lookup
                # and aggregation

                "group": node_id % 10
            }
        )


    # -------------------------------------
    # Select benchmark start nodes
    # -------------------------------------

    random_generator = random.Random(20260819)

    start_nodes = random_generator.sample(
        sorted(node_ids),
        min(100, len(node_ids))
    )


    # -------------------------------------
    # Save nodes
    # -------------------------------------

    with open(
        NODES_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            nodes,
            file,
            indent=2
        )


    # -------------------------------------
    # Save relationships
    # -------------------------------------

    with open(
        EDGES_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            edges,
            file,
            indent=2
        )


    # -------------------------------------
    # Save start nodes
    # -------------------------------------

    with open(
        START_NODES_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            start_nodes,
            file,
            indent=2
        )


    # -------------------------------------
    # Print statistics
    # -------------------------------------

    print()
    print("======================================")
    print("DATASET PREPARATION COMPLETE")
    print("======================================")

    print(f"Nodes:          {len(nodes):,}")

    print(f"Relationships:  {len(edges):,}")

    print(f"Start nodes:    {len(start_nodes):,}")

    print()
    print("Files created:")

    print(NODES_FILE)

    print(EDGES_FILE)

    print(START_NODES_FILE)

    print("======================================")


# -----------------------------------------
# Main
# -----------------------------------------

if __name__ == "__main__":

    prepare_dataset()