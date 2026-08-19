from connectors.cognodb import CognoDBAdapter


db = CognoDBAdapter()

try:

    db.connect()

    db.verify()

    result = db.driver.execute_query(
        """
        RETURN 'CognoDB connection successful' AS message
        """,
        database_=db.database
    )

    for record in result.records:

        print(record["message"])

finally:

    db.close()