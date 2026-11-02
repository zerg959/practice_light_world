CREATE DATABASE myproject_db;
CREATE USER myproject_user WITH PASSWORD 'secure_password_123';
ALTER ROLE myproject_user SET client_encoding TO 'utf8';
ALTER ROLE myproject_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE myproject_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE myproject_db TO myproject_user;
GRANT ALL ON SCHEMA public TO myproject_user;