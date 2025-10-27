-- PROCEDURE: public.carrega_instituicoes()

-- DROP PROCEDURE IF EXISTS public.carrega_instituicoes();

CREATE OR REPLACE PROCEDURE public.carrega_instituicoes(
	)
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
    wconteudo := pg_read_file('dados_ecos/univs.csv');
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
				 WHERE UPPER(TRIM(cid.nome)) LIKE UPPER(TRIM(wcols[3]));
			 EXCEPTION WHEN NO_DATA_FOUND THEN
		           RAISE EXCEPTION 'Cidade não encontrada: %', wcols[3];
			END;

			BEGIN
			    INSERT INTO instituicoes (sigla, nome, tip_inst, cid_id)
			    VALUES (wcols[1], wcols[2], 1, wcid_id);
			EXCEPTION
			    WHEN OTHERS THEN
			        RAISE EXCEPTION 'Erro ao inserir instituição: %, Detalhe: %', wcols[2], SQLERRM;
			END;
				
		END IF;
    END LOOP;
	
	/* === Ler arquivo com as matriculas (e outras instituicoes) === */
    wconteudo := pg_read_file('dados_ecos/instituicoes_ep.csv');
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

					RAISE NOTICE 'Inst %, tipo %', wcols[4], wtip_inst;

					BEGIN
						INSERT INTO instituicoes (SIGLA, NOME, TIP_INST, NUM_MATRICULAS, SITE, CID_ID)
						VALUES(wcols[2], wcols[4], wtip_inst, wnum_mats, wcols[6], wcid_id);
					EXCEPTION WHEN OTHERS THEN
						RAISE EXCEPTION 'Erro ao inserir instituição: %, Detalhe: %', wcols[4], SQLERRM;
					END;
    			END IF;
			END;
		END IF;
    END LOOP;
END 
$BODY$;
ALTER PROCEDURE public.carrega_instituicoes()
    OWNER TO postgres;
