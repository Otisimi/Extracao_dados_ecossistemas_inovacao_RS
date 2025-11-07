-- PROCEDURE: public.carrega_pessoas(text)

-- DROP PROCEDURE IF EXISTS public.carrega_pessoas(text);

CREATE OR REPLACE PROCEDURE public.carrega_pessoas(IN pi_arq text
	)
LANGUAGE 'plpgsql'
AS $BODY$
DECLARE
    wconteudo text;
    wlin	  text;
	wlinhas   text[];
    wcols     text[];
	weco_id	  int;
	wtitulo	  int;
	wpesq	  int;
    i 		  int;
BEGIN
    wconteudo := pg_read_file(PI_ARQ);
	wconteudo := replace(wconteudo, E'\r', '');
	wlinhas := string_to_array(wconteudo, E'\n');
	
	FOR i IN 2..array_upper(wlinhas, 1) LOOP
        wlin := trim(wlinhas[i]);
		wcols := NULL;
        IF wlin IS NOT NULL AND wlin <> '' THEN
            wcols := string_to_array(wlin, ';');
			IF wcols IS NOT NULL THEN
				BEGIN
					SELECT eco.id
					  INTO weco_id
					  FROM ecossistemas_inovacao eco
					 WHERE UPPER(eco.nome) LIKE UPPER(TRIM(wcols[1]));
				EXCEPTION WHEN NO_DATA_FOUND THEN
		            RAISE EXCEPTION 'Ecossistema não encontrado: %', wcols[1];
				END;

				wtitulo := CASE  
							  WHEN UPPER(TRIM(wcols[3])) = 'Especialização' THEN 1
							  WHEN UPPER(TRIM(wcols[3])) = 'Mestrado' THEN 2
							  WHEN UPPER(TRIM(wcols[3])) = 'Doutorado' THEN 3
							  ELSE 4
						   END;

				wpesq := CASE  
							WHEN UPPER(TRIM(wcols[4])) LIKE 'SIM' THEN 1
							ELSE 0
						   END;

				INSERT INTO pessoas(nome, ind_pesq, tip_titulo, eco_id)
				VALUES (wcols[2], wpesq, wtitulo, weco_id);
				
			END IF;
        END IF;
    END LOOP;
END 
$BODY$;
ALTER PROCEDURE public.carrega_pessoas(text)
    OWNER TO postgres;
