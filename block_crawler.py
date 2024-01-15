# Block Crawler for Ethereum Transactions
# Author: Haoran Shu
# Project: Haoran Shu Technical Challenge
# Created: 2024-01-15
# Description: This script retrieves Ethereum Mainnet transactions within a specified block range
# and saves them to an SQLite database. It utilizes the Web3.py library to interact with the Ethereum blockchain.

import sqlite3
import sys
import os
import re
from web3 import Web3

def create_database(db_path, schema_file='create_db.sql'):
    """
    Creates an SQLite database based on the provided schema file.
    
    :param db_path: Path to the SQLite database file.
    :param schema_file: Path to the SQL file containing the database schema.
    """
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    with open(schema_file, 'r') as file:
        schema = file.read()
        c.executescript(schema)

    conn.commit()
    conn.close()
    
def fetch_transactions(start_block, end_block, db_path, alchemy_url):
    """
    Fetches transactions from the Ethereum Mainnet within a given block range
    and stores them in the SQLite database.

    :param start_block: The starting block number.
    :param end_block: The ending block number.
    :param db_path: Path to the SQLite database file.
    :param alchemy_url: URL for the Ethereum JSON-RPC endpoint.
    """
    w3 = Web3(Web3.HTTPProvider(alchemy_url))
    if not w3.is_connected():
        print("Failed to connect to Ethereum network")
        return

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    try:
        for block_num in range(start_block, end_block + 1):
            print(f"Fetching block {block_num}...")
            block = w3.eth.get_block(block_num, full_transactions=True)
            for tx in block.transactions:
                # Insert transaction data into the database
                c.execute('INSERT OR IGNORE INTO transactions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                          (tx.hash.hex(), tx.blockNumber, tx['from'], tx['to'], str(w3.from_wei(tx['value'], 'ether')),
                           tx['gas'], tx['gasPrice'], tx['nonce'], block.timestamp))
            conn.commit()
            print(f"Block {block_num}: {len(block.transactions)} transactions processed.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

def validate_ethereum_rpc_endpoint(url):
    """
    Validates the Ethereum RPC endpoint URL.
    
    :param url: The URL to validate.
    :return: Boolean indicating if the URL is valid.
    """
    pattern = re.compile(r'https?://[^\s/$.?#].[^\s]*')
    return pattern.match(url) is not None

def validate_database_path(db_path):
    """
    Validates the database path to ensure it is writable.
    
    :param db_path: The path to the database file.
    :return: Boolean indicating if the path is valid.
    """
    try:
        with open(db_path, 'a'):
            pass
        return True
    except IOError:
        return False

def parse_block_range(block_range):

    """
    Parses and validates the block range.
    
    :param block_range: The block range string.
    :return: Tuple of start and end blocks, or None if invalid.
    """
    try:
        start_block, end_block = map(int, block_range.split('-'))
        if start_block <= end_block:
            return start_block, end_block
    except ValueError:
        pass
    return None

if __name__ == "__main__":
    # Command line argument handling
    if len(sys.argv) != 4:
        print("Usage: python block-crawler.py <RPC_ENDPOINT> <DB_PATH> <BLOCK_RANGE>")
        sys.exit(1)

    rpc_endpoint, db_path, block_range = sys.argv[1], sys.argv[2], sys.argv[3]

    #Run the Input Validation
    if not validate_ethereum_rpc_endpoint(rpc_endpoint):
        print("Invalid Ethereum RPC endpoint.")
        sys.exit(1)

    if not validate_database_path(db_path):
        print("Invalid or inaccessible database path.")
        sys.exit(1)

    block_range_parsed = parse_block_range(block_range)
    if block_range_parsed is None:
        print("Invalid block range format or range. Format should be start-end (e.g., 200-300).")
        sys.exit(1)

    start_block, end_block = block_range_parsed
    
    create_database(db_path)
    fetch_transactions(start_block, end_block, db_path, rpc_endpoint)