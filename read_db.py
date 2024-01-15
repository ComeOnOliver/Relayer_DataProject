# Query for Largest Volume Block in Ethereum Transactions
# Author: Haoran Shu
# Project: Haoran Shu Technical Challenge
# Created: 2024-01-15
# Description: This script queries an SQLite database to find the block with the largest volume of ether transferred within a specific time frame.

import sqlite3
import sys

def query_largest_volume_block(db_path):
    """
    Queries the SQLite database to find the block with the largest volume of ether transferred.

    :param db_path: Path to the SQLite database file.
    """
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    try:
        # SQL query to find the block with the largest volume of ether transferred between 2024-01-01 00:00:00 and 2024-01-01 00:30:00
        query = """
        SELECT block_number, SUM(value) AS total_volume
        FROM transactions
        WHERE timestamp BETWEEN strftime('%s', '2024-01-01 00:00:00') AND strftime('%s', '2024-01-01 00:30:00')
        GROUP BY block_number
        ORDER BY total_volume DESC
        LIMIT 1;
        """

        c.execute(query)
        result = c.fetchone()

        # Process and display the query result
        if result:
            block_number, total_volume = result
            print(f"Block with Largest Volume: {block_number}, Total Volume Transferred: {total_volume} Ether")
        else:
            print("No transactions found in the specified time frame.")
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    # Command line argument handling
    if len(sys.argv) != 2:
        print("Usage: python3 read_db.py <DB_PATH>")
        sys.exit(1)

    db_path = sys.argv[1]
    query_largest_volume_block(db_path)
