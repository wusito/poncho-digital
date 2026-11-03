DO $$
DECLARE
    r RECORD;
BEGIN
    FOR r IN 
        SELECT 
            tc.table_schema, 
            tc.table_name, 
            tc.column_name, 
            pg_get_serial_sequence(quote_ident(tc.table_schema) || '.' || quote_ident(tc.table_name), tc.column_name) AS seq_name
        FROM information_schema.columns tc
        WHERE pg_get_serial_sequence(quote_ident(tc.table_schema) || '.' || quote_ident(tc.table_name), tc.column_name) IS NOT NULL
    LOOP
        EXECUTE format(
            'SELECT setval(%L, COALESCE(MAX(%I), 1), MAX(%I) IS NOT NULL) FROM %I.%I',
            r.seq_name,
            r.column_name,
            r.column_name,
            r.table_schema,
            r.table_name
        );
    END LOOP;
END $$;
