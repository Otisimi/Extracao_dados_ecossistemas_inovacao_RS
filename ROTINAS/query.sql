call exec_all();

select * from eventos;

select * from cidades c  where vlr_invest is not null;

select * From instituicoes where ind_principal = 1 and num_bolsas is not null;

select * from pessoas where eco_id = 6 order by nome desc;

select c.nome, e.* from ENTIDADES_GOV e join cidades c on c.id = e.cid_id;

SELECT
	E.NOME,
	C.NOME,
	AI.SIGLA,
	AI.NOME,
	AI.TIP_AMB,
	AI.SITE
FROM
	AMBIENTES_INOV AI
	INNER JOIN CIDADES C ON AI.CID_ID = C.ID
	INNER JOIN ECOSSISTEMAS_INOVACAO E ON C.ECO_ID = E.ID
ORDER BY
	AI.SIGLA;


select c.id, c.nome, s.* from startups s join cidades c on c.id = s.cid_id order by c.id desc;

select * from startups where cid_id is null;

select i.sigla, p.* from producoes p join instituicoes i on i.id = p.inst_id where i.sigla = 'UCS';

select c.nome, e.* from empresas_alto_cresc e join cidades c on c.id = e.cid_id;