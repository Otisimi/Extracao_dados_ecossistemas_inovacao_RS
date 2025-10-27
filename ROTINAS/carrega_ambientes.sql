-- PROCEDURE: public.carrega_ambientes(text, integer)

-- DROP PROCEDURE IF EXISTS public.carrega_ambientes(text, integer);

CREATE OR REPLACE PROCEDURE public.carrega_ambientes(
	IN pi_arq text,
	IN pi_tip_amb integer)
LANGUAGE 'plpgsql'
AS $BODY$
DECLARE
    wconteudo text;
    wlin	  text;
	wlinhas   text[];
    wcols     text[];
	wcid_id	  int;
    i 		  int;
BEGIN
    wconteudo := pg_read_file(PI_ARQ);
	wconteudo := replace(wconteudo, E'\r', '');
	wlinhas := string_to_array(wconteudo, E'\n');
	
	FOR i IN 2..array_upper(wlinhas, 1) LOOP
        wcols := string_to_array(trim(wlinhas[i]), ';');
		IF wcols IS NOT NULL 
			AND array_length(wcols, 1) > 0 THEN
			BEGIN
				SELECT cid.id
				  INTO STRICT wcid_id
				  FROM cidades cid
				 WHERE UPPER(TRIM(cid.nome)) LIKE UPPER(TRIM(wcols[4]));
			 EXCEPTION WHEN NO_DATA_FOUND THEN
		           RAISE EXCEPTION 'Cidade não encontrada: %', wcols[4];
			END;

			BEGIN
			    INSERT INTO ambientes_inov (sigla, nome, tip_amb, site, cid_id)
			    VALUES (wcols[2], wcols[3], pi_tip_amb, wcols[5], wcid_id);
			EXCEPTION
			    WHEN OTHERS THEN
			        RAISE EXCEPTION 'Erro ao inserir ambiente: %, Detalhe: %', wcols[3], SQLERRM;
			END;
				
		END IF;
    END LOOP;
END 
$BODY$;
ALTER PROCEDURE public.carrega_ambientes(text, integer)
    OWNER TO postgres;
