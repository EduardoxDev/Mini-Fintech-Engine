
CREATE TABLE account (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    balance DECIMAL(19,4) NOT NULL,
    version BIGINT NOT NULL
);

CREATE TABLE transaction_record (
    id VARCHAR(36) PRIMARY KEY,
    source_account_id VARCHAR(36) NOT NULL,
    target_account_id VARCHAR(36) NOT NULL,
    amount DECIMAL(19,4) NOT NULL,
    idempotency_key VARCHAR(255) UNIQUE,
    timestamp TIMESTAMP NOT NULL,
    status VARCHAR(50) NOT NULL
);

CREATE TABLE outbox_event (
    id VARCHAR(36) PRIMARY KEY,
    aggregate_type VARCHAR(255) NOT NULL,
    aggregate_id VARCHAR(36) NOT NULL,
    type VARCHAR(255) NOT NULL,
    payload TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    processed BOOLEAN DEFAULT FALSE
);

CREATE TABLE idempotency_key_entity (
    key_name VARCHAR(255) PRIMARY KEY,
    created_at TIMESTAMP NOT NULL
);
