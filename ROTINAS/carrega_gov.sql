-- PROCEDURE: public.carrega_gov(text)

-- DROP PROCEDURE IF EXISTS public.carrega_gov(text);

CREATE OR REPLACE PROCEDURE public.carrega_gov(
	IN pi_arq text)
LANGUAGE 'plpgsql'
AS $BODY$
DECLARE
    wconteudo text;
    wlin	  text;
	wlinhas   text[];
    wcols     text[];
	wcid_id	  int;
	wnome_cid text;
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
				wnome_cid := unaccent(replace(UPPER(TRIM(wcols[3])), '''', ''));
			
				SELECT cid.id
				  INTO STRICT wcid_id
				  FROM cidades cid
				 WHERE unaccent(UPPER(TRIM(cid.nome))) LIKE wnome_cid;
			 EXCEPTION WHEN NO_DATA_FOUND THEN
		           RAISE EXCEPTION 'Cidade não encontrada: %', wcols[3];
			END;

			BEGIN
			    INSERT INTO entidades_gov (entidade, nome_uni, cid_id)
			    VALUES (wcols[1], wcols[2], wcid_id);
			EXCEPTION
			    WHEN OTHERS THEN
			        RAISE EXCEPTION 'Erro ao inserir unidade: %, Detalhe: %', wcols[2], SQLERRM;
			END;
				
		END IF;
    END LOOP;
END 
$BODY$;
ALTER PROCEDURE public.carrega_gov(text)
    OWNER TO postgres;
