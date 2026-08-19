import os

from dotenv import load_dotenv
from neo4j import GraphDatabase


load_dotenv()


URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")
DATABASE = os.getenv("NEO4J_DATABASE")


print()
print("======================================")
print("NEO4J DIRECT CONNECTION TEST")
print("======================================")

print()
print("URI:")
print(URI)

print()
print("USERNAME:")
print(USERNAME)

print()
print("DATABASE:")
print(DATABASE)

print()
print(
    "PASSWORD PRESENT:",
    bool(PASSWORD)
)


driver = None


try:

    print()
    print("Creating Neo4j driver...")

    driver = GraphDatabase.driver(
        URI,
        auth=(
            USERNAME,
            PASSWORD
        )
    )

    print(
        "Driver created."
    )

    # ----------------------------------
    # Connectivity test
    # ----------------------------------

    print()
    print(
        "Testing connectivity..."
    )

    driver.verify_connectivity()

    print(
        "Connectivity successful."
    )


    # ----------------------------------
    # Direct query WITHOUT specifying
    # a database
    # ----------------------------------

    print()
    print(
        "Running RETURN 1..."
    )

    with driver.session() as session:

        result = session.run(
            "RETURN 1 AS value"
        )

        record = result.single()

        print(
            "Query result:",
            record["value"]
        )


    # ----------------------------------
    # Database-specific query
    # ----------------------------------

    print()
    print(
        "Testing configured database..."
    )

    with driver.session(
        database=DATABASE
    ) as session:

        result = session.run(
            "RETURN 1 AS value"
        )

        record = result.single()

        print(
            "Database query result:",
            record["value"]
        )


    print()
    print(
        "======================================"
    )

    print(
        "ALL NEO4J TESTS PASSED"
    )

    print(
        "======================================"
    )


except Exception as error:

    print()
    print(
        "======================================"
    )

    print(
        "NEO4J TEST FAILED"
    )

    print(
        "======================================"
    )

    print()
    print(
        "Error type:"
    )

    print(
        type(error).__name__
    )

    print()
    print(
        "Error:"
    )

    print(
        str(error)
    )


finally:

    if driver:

        driver.close()