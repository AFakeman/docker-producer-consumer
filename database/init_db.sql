CREATE USER consumer;
CREATE DATABASE queue;
\c queue;
CREATE TABLE IF NOT EXISTS queue (
    id serial PRIMARY KEY,
    data varchar(140)
);
GRANT INSERT ON queue TO consumer;
GRANT USAGE, SELECT ON queue_id_seq to consumer;
