import os

from dotenv import load_dotenv
from neo4j import GraphDatabase


load_dotenv()


URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")
DATABASE = os.getenv("NEO4J_DATABASE")


# Change only the connection scheme.
# neo4j+s://  ->  bolt+s://
BOLT_URI = URI.replace(
    "neo4j+s://",
    "bolt+s://"
)


print()
print("======================================")
print("NEO4J DIRECT BOLT TEST")
print("======================================")

print()
print("Original URI:")
print(URI)

print()
print("Direct Bolt URI:")
print(BOLT_URI)

print()
print("Username:")
print(USERNAME)

print()
print("Database:")
print(DATABASE)

print()
print(
    "Password present:",
    bool(PASSWORD)
)


driver = None


try:

    print()
    print("Creating driver...")

    driver = GraphDatabase.driver(
        BOLT_URI,
        auth=(
            USERNAME,
            PASSWORD
        )
    )

    print(
        "Driver created."
    )


    print()
    print(
        "Testing direct Bolt connectivity..."
    )

    driver.verify_connectivity()

    print(
        "Direct Bolt connectivity successful."
    )


    print()
    print(
        "Running test query..."
    )

    with driver.session(
        database=DATABASE
    ) as session:

        result = session.run(
            "RETURN 1 AS value"
        )

        record = result.single()

        print(
            "Query result:",
            record["value"]
        )


    print()
    print("======================================")
    print("DIRECT BOLT TEST PASSED")
    print("======================================")


except Exception as error:

    print()
    print("======================================")
    print("DIRECT BOLT TEST FAILED")
    print("======================================")

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