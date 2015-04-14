//CREATE KEYSPACE ks WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };

use ks;

CREATE TABLE things (
  uuid varchar PRIMARY KEY,
  timestamp int,
  name varchar
);
