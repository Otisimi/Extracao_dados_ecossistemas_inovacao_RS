-- PROCEDURE: public.carrega_startups(text)

-- DROP PROCEDURE IF EXISTS public.carrega_startups(text);

CREATE OR REPLACE PROCEDURE carrega_startups(IN pi_arq text)
LANGUAGE 'plpgsql'
AS $BODY$
DECLARE
    i 		  int;
    wconteudo text;
    wlin	  text;
	wlinhas   text[];
    wcols     text[];
	wcid_id	  int;
	wamb_id	  int;
BEGIN
    wconteudo := pg_read_file(PI_ARQ);
	wconteudo := replace(wconteudo, E'\r', '');
	wlinhas := string_to_array(wconteudo, E'\n');
	
	FOR i IN 2..array_upper(wlinhas, 1) LOOP
	/*1 - Ecossistema
	  2 - Cidade
	  3 - Link
	  4 - Estágio de Maturidade
	  5 - Modelo de Negócio
	  6 - Segmento
	  7 - Vertical
	  8 - Público-alvo
	  9 - Startup
	  10 - Ambiente de Inovação*/
        wcols := string_to_array(trim(wlinhas[i]), ';');
		IF wcols IS NOT NULL 
			AND array_length(wcols, 1) > 0 THEN
			BEGIN
				SELECT cid.id
				  INTO STRICT wcid_id
				  FROM cidades cid
				 WHERE UPPER(TRIM(cid.nome)) LIKE UPPER(TRIM(wcols[2]));
			 EXCEPTION 
			 	WHEN NO_DATA_FOUND THEN
		           RAISE EXCEPTION 'Cidade não encontrada: %', wcols[2];
			 	WHEN OTHERS THEN
		           RAISE EXCEPTION 'ERRO Cidade: %; %', wcols[2], SQLERRM;
			END;

			IF UPPER(wcols[10]) LIKE 'NÃO INFORMADO' THEN
				wamb_id := NULL;
			ELSE
				BEGIN
					SELECT amb.id
					  INTO wamb_id
					  FROM ambientes_inov amb
					 WHERE UPPER(TRIM(amb.sigla)) LIKE '%' || REPLACE(UPPER(TRIM(wcols[10])), ' ', '%') || '%'
					   AND amb.cid_id = wcid_id;
				EXCEPTION 
					WHEN NO_DATA_FOUND THEN
						-- Insere ambiente como "Outro"
						INSERT INTO ambientes_inov (sigla, tip_amb, cid_id)
						VALUES (wcols[10], 4, wcid_id);
						-- Pega o ID novo do ambiente adicionado
						SELECT amb.id
						  INTO STRICT wamb_id
						  FROM ambientes_inov amb
						 WHERE UPPER(TRIM(amb.sigla)) LIKE UPPER(TRIM(wcols[10]));
			 	WHEN OTHERS THEN
		           RAISE EXCEPTION 'ERRO Ambiente: %; %', wcols[10], SQLERRM;
				END;
			END IF;

			BEGIN
			    INSERT INTO startups (nome, area, site, cid_id, amb_id)
			    VALUES (wcols[9], wcols[6], wcols[3], wcid_id, wamb_id);
			EXCEPTION
			    WHEN OTHERS THEN
			        RAISE EXCEPTION 'Erro ao inserir startup: %, Detalhe: %', wcols[9], SQLERRM;
			END;
				
		END IF;
    END LOOP;
END 
$BODY$;
ALTER PROCEDURE public.carrega_startups(text)
    OWNER TO postgres;
