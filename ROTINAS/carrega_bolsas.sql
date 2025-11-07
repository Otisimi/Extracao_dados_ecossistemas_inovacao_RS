-- PROCEDURE: public.carrega_bolsas(text)

-- DROP PROCEDURE IF EXISTS public.carrega_bolsas(text);

CREATE OR REPLACE PROCEDURE public.carrega_bolsas(
	IN pi_arq text)
LANGUAGE 'plpgsql'
AS $BODY$
DECLARE
    i 		    int;
    wconteudo   text;
    wlin	    text;
	wlinhas     text[];
    wcols       text[];
	wtip_inst   int;
	wcid_id	    int;
	winst_id    int;
	wnum_bolsas int;
	wsigla_inst text;
BEGIN
    wconteudo := pg_read_file(PI_ARQ);
	wconteudo := replace(wconteudo, E'\r', '');
	wlinhas := string_to_array(wconteudo, E'\n');
	
	FOR i IN 2..array_upper(wlinhas, 1) LOOP
        wcols := string_to_array(trim(wlinhas[i]), ';');
		IF wcols IS NOT NULL 
			AND array_length(wcols, 1) > 0 THEN

			IF wcols[3] <> '-' THEN
				wnum_bolsas := NULLIF(wcols[3], '')::int;
				wsigla_inst := TRIM(split_part(wcols[1], '-', 1));
	
				BEGIN
					UPDATE instituicoes
					   SET num_bolsas = COALESCE(num_bolsas, 0) + wnum_bolsas
					 WHERE UPPER(sigla) LIKE UPPER(wsigla_inst);
					
					IF NOT FOUND THEN
						RAISE EXCEPTION 'Instituição não encontrada: %', wcols[1];
					END IF;
				END;
			END IF;
		END IF;
    END LOOP;	
END 
$BODY$;
ALTER PROCEDURE public.carrega_bolsas(text)
    OWNER TO postgres;