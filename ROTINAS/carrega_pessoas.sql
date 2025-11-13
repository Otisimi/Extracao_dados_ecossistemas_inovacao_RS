-- PROCEDURE: public.carrega_pessoas(text)

-- DROP PROCEDURE IF EXISTS public.carrega_pessoas(text);

CREATE OR REPLACE PROCEDURE public.carrega_pessoas(
	IN pi_arq text)
LANGUAGE 'plpgsql'
AS $BODY$
DECLARE
    wconteudo text;
    wlin	  text;
	wlinhas   text[];
    wcols     text[];
	weco_id	  int;
	winst_id  int;
	wtitulo	  int;
	wpesq	  int;
	wprojs	  text[];
    i 		  int;
	j		  int;
	wproj_salvo int;
	wproj_grava text;
BEGIN
    wconteudo := pg_read_file(PI_ARQ);
	wconteudo := replace(wconteudo, E'\r', '');
	wlinhas := string_to_array(wconteudo, E'\n');
	
	BEGIN
		SELECT inst.id
		  INTO STRICT winst_id
		  FROM instituicoes inst
		 WHERE UPPER(TRIM(inst.sigla)) LIKE 'UCS'
		   AND inst.ind_principal = 1;
	 EXCEPTION WHEN NO_DATA_FOUND THEN
		   RAISE EXCEPTION 'Instituição UCS não encontrada';
	END;
	
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
							  WHEN TRIM(wcols[3]) = 'Especialização' THEN 1
							  WHEN TRIM(wcols[3]) = 'Mestrado' THEN 2
							  WHEN TRIM(wcols[3]) = 'Doutorado' THEN 3
							  ELSE 4
						   END;

				wpesq := CASE  
							WHEN UPPER(TRIM(wcols[4])) LIKE 'SIM' THEN 1
							ELSE 0
						   END;

				INSERT INTO pessoas(nome, ind_pesq, tip_titulo, eco_id)
				VALUES (wcols[2], wpesq, wtitulo, weco_id);

				IF wcols[5] <> '' THEN
					wprojs := string_to_array(trim(replace(wcols[5], '"', '')), '\');
					-- Loop para inserir projetos
					FOR j IN 1 .. array_upper(wprojs, 1)  LOOP
						wproj_grava := TRIM(wprojs[j]);
						BEGIN
							INSERT INTO producoes (nome, tip_prod, autor, inst_id)
							VALUES (wproj_grava, 2, wcols[2], winst_id);
						EXCEPTION
							WHEN UNIQUE_VIOLATION THEN
								wproj_salvo := 1;
							WHEN OTHERS THEN
								RAISE EXCEPTION 'Erro ao inserir produção: % - %, Detalhe: %', wproj_grava, wcols[2], SQLERRM;
						END;
					END LOOP;
				END IF;
			END IF;
        END IF;
    END LOOP;
END 
$BODY$;
ALTER PROCEDURE public.carrega_pessoas(text)
    OWNER TO postgres;
