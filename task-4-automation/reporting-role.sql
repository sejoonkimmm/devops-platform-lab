-- Read-only login for the weekly business report.
-- The password here is a placeholder; the real one comes from the secret manager.
CREATE ROLE reporting LOGIN PASSWORD 'set-via-secret-manager' CONNECTION LIMIT 2;
GRANT CONNECT ON DATABASE springboot_demo TO reporting;
GRANT USAGE ON SCHEMA public TO reporting;
GRANT SELECT ON products, prices, messages TO reporting;
-- No default privileges on purpose. A new table must be granted here explicitly,
-- so new data cannot leak into the reporting role by accident.
ALTER ROLE reporting SET statement_timeout = '30s';
