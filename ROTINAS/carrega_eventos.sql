-- PROCEDURE: public.carrega_eventos(text)

-- DROP PROCEDURE IF EXISTS public.carrega_eventos(text);

CREATE OR REPLACE PROCEDURE public.carrega_eventos(
	IN pi_arq text)
LANGUAGE 'plpgsql'
AS $BODY$
DECLARE
    wconteudo text;
    wlin	  text;
	wlinhas   text[];
    wcols     text[];
	weco_id	  int;
    i 		  int;
BEGIN
    wconteudo := pg_read_file(PI_ARQ);
    -- Tira a quebra de linha 
	wconteudo := replace(wconteudo, E'\r', '');
    -- Quebra por linhas
	wlinhas := string_to_array(wconteudo, E'\n');
	
	-- Itera pelas linhas
	FOR i IN 2..array_upper(wlinhas, 1) LOOP
		-- Pega linha atual (sem espaços antes ou depois)
        wlin := trim(wlinhas[i]);
		-- Reseta só pra evitar duplicados
		wcols := NULL;
        IF wlin IS NOT NULL AND wlin <> '' THEN
			-- Separa as colunas em Ecossistema e Nome
            wcols := string_to_array(wlin, ';');
			IF wcols IS NOT NULL THEN
				BEGIN
					SELECT ecoi.id
					  INTO STRICT weco_id
					  FROM ecossistemas_inovacao ecoi
					 WHERE UPPER(ecoi.nome) LIKE UPPER(wcols[1]);
				EXCEPTION WHEN NO_DATA_FOUND THEN
		            RAISE EXCEPTION 'Ecossistema não encontrado: %', wcols[1];
				END;

				BEGIN
					INSERT INTO eventos (NOME
						, DTA_INI
						, DTA_FIM
						, ECO_ID)
					VALUES(wcols[2]
						, TO_DATE(wcols[3], 'DD/MM/YYYY')
						, TO_DATE(wcols[4], 'DD/MM/YYYY')
						, weco_id);
				EXCEPTION WHEN OTHERS THEN
					RAISE EXCEPTION 'Não foi possível incluir evento: %', wcols[2];
				END;
				
			END IF;
        END IF;
    END LOOP;
END 
$BODY$;
ALTER PROCEDURE public.carrega_eventos(text)
    OWNER TO postgres;
