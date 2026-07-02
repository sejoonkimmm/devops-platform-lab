CREATE ROLE reporting LOGIN PASSWORD 'set-via-secret-manager';
GRANT CONNECT ON DATABASE springboot_demo TO reporting;
GRANT USAGE ON SCHEMA public TO reporting;
GRANT SELECT ON products, prices, messages TO reporting;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO reporting;
