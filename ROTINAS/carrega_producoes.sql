-- PROCEDURE: public.carrega_producoes(text, integer)

-- DROP PROCEDURE IF EXISTS public.carrega_producoes(text, integer);

CREATE OR REPLACE PROCEDURE public.carrega_producoes(
	IN pi_arq text,
	IN pi_tip_prod integer)
LANGUAGE 'plpgsql'
AS $BODY$
DECLARE
    wconteudo text;
    wlin	  text;
	wlinhas   text[];
    wcols     text[];
	wautores  text[];
	weco_id   int;
	winst_id  int;
	wtip_prod int;
    i 		  int;
	j		  int;
	wexiste	  boolean;
	waut_grava text;
	registro_duplicado_na_api int;
BEGIN
    wconteudo := pg_read_file(PI_ARQ);
	wconteudo := replace(wconteudo, E'\r', '');
	wlinhas := string_to_array(wconteudo, E'\n');
	
	FOR i IN 2..array_upper(wlinhas, 1) LOOP
        wcols := string_to_array(trim(wlinhas[i]), ';');
		IF wcols IS NOT NULL 
			AND array_length(wcols, 1) > 0 THEN
			-- Pega id da instiuição principal
			BEGIN
				SELECT inst.id
				  INTO STRICT winst_id
				  FROM instituicoes inst
				 WHERE UPPER(TRIM(inst.sigla)) LIKE UPPER(TRIM(wcols[1]))
				   AND inst.ind_principal = 1;
			 EXCEPTION WHEN NO_DATA_FOUND THEN
		           RAISE EXCEPTION 'Instituição não encontrada: %', wcols[1];
			END;

			-- Se for publicação, tem campo extra indicando se é tese ou dissertação
			IF pi_tip_prod = 3 THEN
				wtip_prod := CASE WHEN wcols[4] = 'TESE' THEN 3 ELSE 4 END;
				-- Tira os colchetes e separa pela vírgula
				wautores := string_to_array(trim(replace(replace(wcols[5], '[', ''), ']', '')), ',');
			ELSE
				wtip_prod = pi_tip_prod;
				wautores := string_to_array(trim(replace(replace(wcols[4], '[', ''), ']', '')), ',');
			END IF;
			
			-- Loop para inserir autores separadamente
			FOR j IN 1 .. array_upper(wautores, 1)  LOOP
				waut_grava := TRIM(replace(wautores[j],'''', ''));
				BEGIN
					INSERT INTO producoes (nome, tip_prod, autor, inst_id)
					VALUES (wcols[3], wtip_prod, waut_grava, winst_id);
				EXCEPTION
					WHEN UNIQUE_VIOLATION THEN
						registro_duplicado_na_api := 1;
					WHEN OTHERS THEN
						RAISE EXCEPTION 'Erro ao inserir produção: % - %, Detalhe: %', wtip_prod, wcols[3], SQLERRM;
				END;

				IF pi_tip_prod = 2 THEN
					SELECT EXISTS (
							    SELECT 1
							      FROM pessoas
							     WHERE unaccent(UPPER(nome)) LIKE unaccent(UPPER(waut_grava))
							) INTO wexiste;
					IF NOT wexiste  THEN
						BEGIN
							SELECT eco.id
							  INTO weco_id
							  FROM instituicoes inst
							  JOIN cidades c 
							    ON c.id = inst.cid_id
							  JOIN ecossistemas_inovacao eco
							    ON eco.id = c.eco_id
							 WHERE inst.id = winst_id;
						EXCEPTION WHEN NO_DATA_FOUND THEN
							RAISE EXCEPTION 'Ecossistema não encontrado para pesquisador: %', waut_grava;
						END;

						INSERT INTO PESSOAS(nome, ind_pesq, tip_titulo, eco_id)
						  	 VALUES (waut_grava, 1, 4, weco_id);
					END IF;
				END IF;

			END LOOP;
				
		END IF;
    END LOOP;
END 
$BODY$;
ALTER PROCEDURE public.carrega_producoes(text, integer)
    OWNER TO postgres;
