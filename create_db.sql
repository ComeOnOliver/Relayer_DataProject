-- create_db.sql
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
