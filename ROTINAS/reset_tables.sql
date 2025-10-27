-- PROCEDURE: public.reset_tables()

-- DROP PROCEDURE IF EXISTS public.reset_tables();

CREATE OR REPLACE PROCEDURE public.reset_tables(
	)
LANGUAGE 'plpgsql'
AS $BODY$
DECLARE
    r RECORD;
BEGIN
    FOR r IN (
        SELECT tablename
        FROM pg_tables
        WHERE schemaname = 'public'
    )
    LOOP
        EXECUTE 'DROP TABLE IF EXISTS public.' || quote_ident(r.tablename) || ' CASCADE';
    END LOOP;
END;
$BODY$;
ALTER PROCEDURE public.reset_tables()
    OWNER TO postgres;
