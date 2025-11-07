-- PROCEDURE: public.carrega_matriculas(text)

-- DROP PROCEDURE IF EXISTS public.carrega_matriculas(text);

CREATE OR REPLACE PROCEDURE public.carrega_matriculas(
	IN pi_arq text)
LANGUAGE 'plpgsql'
AS $BODY$
DECLARE
    wconteudo text;
    wlin	  text;
	wlinhas   text[];
    wcols     text[];
	wtip_inst int;
	wcid_id	  int;
	wnum_mats int;
    i 		  int;
BEGIN
    wconteudo := pg_read_file(PI_ARQ);
	wconteudo := replace(wconteudo, E'\r', '');
	wlinhas := string_to_array(wconteudo, E'\n');
	
	FOR i IN 2..array_upper(wlinhas, 1) LOOP
        wcols := string_to_array(trim(wlinhas[i]), ';');
		IF wcols IS NOT NULL 
			AND array_length(wcols, 1) > 0 THEN

			wnum_mats := NULLIF(wcols[3], '')::int;
			
			BEGIN
				SELECT cid.id
				  INTO STRICT wcid_id
				  FROM cidades cid
				 WHERE UPPER(TRIM(cid.nome)) LIKE UPPER(TRIM(wcols[5]));
		    EXCEPTION WHEN NO_DATA_FOUND THEN
		         RAISE EXCEPTION 'Ecossistema não encontrado: %', wcols[1];
			END;

			BEGIN
				UPDATE instituicoes
				   SET num_matriculas = wnum_mats
				      ,site = wcols[6]
				 WHERE UPPER(nome) LIKE UPPER(TRIM(wcols[4]))
				   AND cid_id = wcid_id;
				
				IF NOT FOUND THEN
					-- Faz update nas matrículas 
					-- pela sigla só pra evitar registros 
					-- com valor nulo onde não deveria ser
					UPDATE instituicoes
					   SET num_matriculas = wnum_mats
					 WHERE UPPER(sigla) LIKE UPPER(TRIM(wcols[2]));
					-- Mesmo assim insere um novo registro
					-- com o campus novo
					BEGIN
						SELECT i.tip_inst
						  INTO STRICT wtip_inst
						  FROM instituicoes i
						 WHERE UPPER(TRIM(i.sigla)) LIKE UPPER(TRIM(wcols[2]))
						 LIMIT 1;
					 EXCEPTION 
					 	WHEN NO_DATA_FOUND THEN
				           wtip_inst := 2;
					END;

					BEGIN
						INSERT INTO instituicoes (SIGLA, NOME, TIP_INST, IND_PRINCIPAL, NUM_MATRICULAS, SITE, CID_ID)
						VALUES(wcols[2], wcols[4], wtip_inst, 0, wnum_mats, wcols[6], wcid_id);
					EXCEPTION WHEN OTHERS THEN
						RAISE EXCEPTION 'Erro ao inserir instituição: %, Detalhe: %', wcols[4], SQLERRM;
					END;
    			END IF;
			END;
		END IF;
    END LOOP;
	
	
END 
$BODY$;
ALTER PROCEDURE public.carrega_matriculas(text)
    OWNER TO postgres;