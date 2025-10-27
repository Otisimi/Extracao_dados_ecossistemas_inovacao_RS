-- PROCEDURE: public.exec_all()

-- DROP PROCEDURE IF EXISTS public.exec_all();

CREATE OR REPLACE PROCEDURE public.exec_all(
	)
LANGUAGE 'plpgsql'
AS $BODY$
BEGIN
	CALL reset_tables();
	CALL cria_tabelas();						  
	CALL carrega_ecossistemas();
	CALL carrega_cidades();
	CALL carrega_instituicoes();
END;
$BODY$;
ALTER PROCEDURE public.exec_all()
    OWNER TO postgres;
