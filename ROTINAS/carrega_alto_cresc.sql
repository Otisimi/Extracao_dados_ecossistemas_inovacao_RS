-- PROCEDURE: public.carrega_alto_cresc(text)

-- DROP PROCEDURE IF EXISTS public.carrega_alto_cresc(text);

CREATE OR REPLACE PROCEDURE public.carrega_alto_cresc(IN pi_arq text
	)
LANGUAGE 'plpgsql'
AS $BODY$
DECLARE
    wconteudo text;
    wlin	  text;
	wlinhas   text[];
    wcols     text[];
	wcid_id	  int;
    i 		  int;
	r_alto_cresc empresas_alto_cresc%ROWTYPE;
BEGIN
    wconteudo := pg_read_file(PI_ARQ);
	wconteudo := replace(wconteudo, E'\r', '');
	wlinhas := string_to_array(wconteudo, E'\n');
	
	FOR i IN 2..array_upper(wlinhas, 1) LOOP
        wlin := trim(wlinhas[i]);
		wcols := NULL;
        IF wlin IS NOT NULL AND wlin <> '' THEN
			/* 1 - Posição
			   2 - Empresa
			   3 - Sede
			   4 - Fundação
			   5 - Setor
			   6 - Receita 2024
			   7 - Receita 2023
			   8 - Expansão
			   9 - O que faz
			*/
            wcols := string_to_array(wlin, ';');
			IF wcols IS NOT NULL THEN
				BEGIN
					SELECT cid.id
					  INTO wcid_id
					  FROM cidades cid
					 WHERE UPPER(cid.nome) LIKE UPPER(TRIM(wcols[3]));
				EXCEPTION WHEN NO_DATA_FOUND THEN
		            RAISE EXCEPTION 'Cidade não encontrada: %', wcols[3];
				END;

				r_alto_cresc := NULL;

				SELECT nextval('empresas_alto_cresc_id_seq') INTO r_alto_cresc.id;
				
				r_alto_cresc.nome := TRIM(wcols[2]);
				r_alto_cresc.area := TRIM(wcols[5]);
				r_alto_cresc.receita_24 := replace(TRIM(wcols[6]), '.', '')::numeric;
				r_alto_cresc.receita_23 := replace(TRIM(wcols[7]), '.', '')::numeric;
				r_alto_cresc.cid_id := wcid_id;

				INSERT INTO empresas_alto_cresc
				VALUES (r_alto_cresc.*)
				RETURNING * INTO r_alto_cresc;
				
			END IF;
        END IF;
    END LOOP;
END 
$BODY$;
ALTER PROCEDURE public.carrega_alto_cresc(text)
    OWNER TO postgres;
