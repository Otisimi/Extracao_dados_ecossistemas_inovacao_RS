-- PROCEDURE: public.carrega_invest(text)

-- DROP PROCEDURE IF EXISTS public.carrega_invest(text);

CREATE OR REPLACE PROCEDURE public.carrega_invest(
	IN pi_arq text)
LANGUAGE 'plpgsql'
AS $BODY$
DECLARE
    i 		    int;
    wconteudo   text;
    wlin	    text;
	wlinhas     text[];
    wcols       text[];
	wcid_id	    int;
	wvlr_invest numeric(14,2);
BEGIN
    wconteudo := pg_read_file(PI_ARQ);
	wconteudo := replace(wconteudo, E'\r', '');
	wlinhas := string_to_array(wconteudo, E'\n');
	
	FOR i IN 2..array_upper(wlinhas, 1) LOOP
        wcols := string_to_array(trim(wlinhas[i]), ';');
		IF wcols IS NOT NULL 
			AND array_length(wcols, 1) > 0 THEN

			wvlr_invest := replace(replace(wcols[2], '.', ''), ',', '.')::numeric;
			
			BEGIN
				SELECT cid.id
				  INTO STRICT wcid_id
				  FROM cidades cid
				 WHERE UPPER(TRIM(cid.nome)) LIKE UPPER(TRIM(wcols[1]));
			 EXCEPTION WHEN NO_DATA_FOUND THEN
		           RAISE EXCEPTION 'Cidade não encontrada: %', wcols[1];
			END;
			
			BEGIN
				UPDATE cidades
				   SET vlr_invest = wvlr_invest
				 WHERE id = wcid_id;
			END;
		END IF;
    END LOOP;	
END 
$BODY$;
ALTER PROCEDURE public.carrega_invest(text)
    OWNER TO postgres;