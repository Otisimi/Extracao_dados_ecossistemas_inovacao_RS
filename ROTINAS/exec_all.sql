-- PROCEDURE: public.exec_all()

-- DROP PROCEDURE IF EXISTS public.exec_all();

CREATE OR REPLACE PROCEDURE public.exec_all(
	)
LANGUAGE 'plpgsql'
AS $BODY$
BEGIN
	CALL reset_tables();
	CALL cria_tabelas();						  
	-- Ecos
	CALL carrega_ecossistemas('dados_ecos/ecossistemas_rs.csv');
	-- Cidades
	CALL carrega_cidades('dados_ecos/cidades.csv');
	-- Investimento em P&D
	CALL carrega_invest('dados_ecos/invest.csv');
	-- Instituições
	CALL carrega_instituicoes('dados_ecos/univs.csv');
	-- Matrículas
	CALL carrega_matriculas('dados_ecos/matriculas.csv');
	-- Bolsas
	CALL carrega_bolsas('dados_ecos/bolsas.csv');
	-- Aceleradoras
	CALL carrega_ambientes('dados_ecos/aceleradoras.csv', 1);
	-- Incubadoras
	CALL carrega_ambientes('dados_ecos/incubadoras.csv', 2);
	-- Parques
	CALL carrega_ambientes('dados_ecos/parques.csv', 3);
	-- Startups
	CALL carrega_startups('dados_ecos/startups.csv');
	-- Pessoas
	CALL carrega_pessoas('dados_ecos/pessoas.csv');
	-- Patentes
	CALL carrega_producoes('dados_ecos/patentes_instituicoes.csv', 1);
	-- Projetos
	CALL carrega_producoes('dados_ecos/projetos_instituicoes.csv', 2);
	-- Publicacoes
	CALL carrega_producoes('dados_ecos/publicacoes_instituicoes.csv', 3);
	-- Alto crescimento
	CALL carrega_alto_cresc('dados_ecos/alto_cresc.csv');
	-- SEBRAE
	CALL carrega_gov('dados_ecos/ent_gov.csv');
END;
$BODY$;
ALTER PROCEDURE public.exec_all()
    OWNER TO postgres;
