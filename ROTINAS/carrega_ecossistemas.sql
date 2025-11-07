-- PROCEDURE: public.carrega_ecossistemas(text)

-- DROP PROCEDURE IF EXISTS public.carrega_ecossistemas(text);

CREATE OR REPLACE PROCEDURE public.carrega_ecossistemas(
	IN pi_arq text)
LANGUAGE 'plpgsql'
AS $BODY$
DECLARE
    wconteudo text;
    wlin	  text;
    wcols     text[];
    i 		  int;
BEGIN
    wconteudo := pg_read_file(PI_ARQ);
    -- Tira a quebra de linha 
	wconteudo := replace(wconteudo, E'\r', '');
    -- Quebra por linhas
    wlin := trim(wconteudo);
    -- Separa pelos ";"
    wcols := string_to_array(wlin, ';');

	-- Loop pra pegar os nomes
	FOR i IN array_lower(wcols, 1)..array_upper(wcols, 1) LOOP
		INSERT INTO ecossistemas_inovacao(NOME, PAIS, ESTADO)
		VALUES(wcols[i], 'Brasil', 'Rio Grande do Sul');
	END LOOP;
END 
$BODY$;
ALTER PROCEDURE public.carrega_ecossistemas(text)
    OWNER TO postgres;
