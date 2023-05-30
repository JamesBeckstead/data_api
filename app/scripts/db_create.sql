CREATE DATABASE james_preston
    ENCODING 'UTF8'
    TABLESPACE pg_default
    LC_COLLATE ' en_US.UTF-8'
    LC_CTYPE 'en_US.UTF-8'
    CONNECTION LIMIT 2;

GRANT ALL ON DATABASE james_preston to temp;

CREATE SCHEMA homework;
