import time

from connectors.cognodb import CognoDBAdapter


def main():

    database = CognoDBAdapter()

    try:

        database.connect()

        database.verify()

        print()
        print("Testing 3-hop traversal")
        print("========================")

        for i in range(5):

            start = time.perf_counter()

            result = database.run(
                "traversal_3",
                {
                    "start": 3
                }
            )

            elapsed = (
                time.perf_counter()
                - start
            ) * 1000

            print(
                f"Run {i + 1}: "
                f"{elapsed:.3f} ms | "
                f"result = {result}"
            )

    finally:

        database.close()


if __name__ == "__main__":

    main()