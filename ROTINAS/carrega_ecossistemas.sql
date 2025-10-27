-- PROCEDURE: public.carrega_ecossistemas()

-- DROP PROCEDURE IF EXISTS public.carrega_ecossistemas();

CREATE OR REPLACE PROCEDURE public.carrega_ecossistemas(
	)
LANGUAGE 'plpgsql'
AS $BODY$
DECLARE
    wconteudo text;
    wlin	  text;
    wcols     text[];
    i 		  int;
BEGIN
    wconteudo := pg_read_file('dados_ecos/ecossistemas_rs.csv');
    -- Tira a quebra de linha 
	wconteudo := replace(wconteudo, E'\r', '');
    -- Quebra por linhas
    wlin := trim(wconteudo);
    -- Separa pelos ";"
    wcols := string_to_array(wlin, ';');

	-- Loop pra pegar os nomes
	FOR i IN array_lower(wcols, 1)..array_upper(wcols, 1) LOOP
		INSERT INTO ecossistemas_inovacao(NOME)
		VALUES(wcols[i]);
	END LOOP;
END 
$BODY$;
ALTER PROCEDURE public.carrega_ecossistemas()
    OWNER TO postgres;
