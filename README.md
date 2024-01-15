# Ethereum Transactions Block Crawler

## Overview

This project includes two main components: `block_crawler` and `read_db`. The `block_crawler` script is used to fetch and store Ethereum Mainnet transactions within a specified block range into an SQLite database. The `read_db` script queries this database to find specific transaction details.

## Database Schema

The following is the schema for the `transactions` table in the SQLite database used by the Ethereum Transactions Block Crawler:

```sql
CREATE TABLE IF NOT EXISTS transactions (
    tx_hash TEXT PRIMARY KEY,
    block_number INTEGER,
    from_address TEXT,
    to_address TEXT,
    value TEXT,
    gas INTEGER,
    gas_price INTEGER,
    nonce INTEGER,
    timestamp DATETIME
);
```

This table stores information about each transaction within a specified block range on the Ethereum blockchain. The fields are as follows:

`tx_hash`: The hash of the transaction (Primary Key).\
`block_number`: The block number in which the transaction was included.\
`from_address`: The address of the sender in the transaction.\
`to_address`: The address of the receiver in the transaction.\
`value`: The value of ether transferred in the transaction.\
`gas`: The gas used for the transaction.\
`gas_price`: The gas price set for the transaction.
nonce: The nonce of the transaction.\
`timestamp`: The timestamp of the block containing the transaction.

This schema is designed to capture essential details about transactions on the Ethereum blockchain for further analysis and querying.

## block_crawler.py

The `block_crawler.py` script is responsible for fetching transaction data from the Ethereum Mainnet. It takes command-line arguments to specify the RPC endpoint, database file path, and block range.

### Usage
```bash
python block_crawler.py <RPC_ENDPOINT> <DB_PATH> <BLOCK_RANGE>
```

### Features
Connects to Ethereum Mainnet using a specified JSON-RPC endpoint.\
Retrieves transactions from the specified block range.\
Stores transaction data in an SQLite database.

## read_db.py
The `read_db.py` script queries the populated SQLite database to extract and display specific transaction information.

## Usage
```
python read_db.py <DB_PATH>
```

## Features
Connects to the specified SQLite database.\
Executes predefined queries to retrieve transaction details.\
Can be modified to perform various custom queries as per user requirements.
