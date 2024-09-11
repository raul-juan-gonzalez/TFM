-- ****************************************
-- 1) CATALOGOS (super-dimensionales)
-- ****************************************

with inserciones as (
	SELECT DISTINCT
		tipo_valor,tick,fec_carga  
	FROM mundo_valores_act.sdim_valores
	-- primary key (tick)
	where tick not in ( select distinct tick from mundo_valores_v.sdim_valores )
)
INSERT INTO mundo_valores_v.sdim_valores (tipo_valor,tick,fec_carga)  
SELECT *
FROM inserciones;  

-- --------------------------------------------------------------------

with inserciones as (
	SELECT DISTINCT 
		tipo_mercado,tipo_bolsa,cod_bolsa,fec_carga  
	FROM mundo_valores_act.sdim_mercados
	-- primary key (cod_bolsa)
	where cod_bolsa not in ( select distinct cod_bolsa from mundo_valores_v.sdim_mercados )
)
INSERT INTO mundo_valores_v.sdim_mercados (tipo_mercado,tipo_bolsa,cod_bolsa,fec_carga)  
SELECT *
FROM inserciones;   

-- ****************************************
-- 2) primeras TDCs
-- ****************************************

with inserciones as (
	SELECT DISTINCT 
		cod_pais,pais,country,continente,cod_moneda,moneda,cod_region,region,fec_carga
	from mundo_valores_act.tdc_pais
	--primary key (cod_region)	
	where cod_region not in (select distinct cod_region from mundo_valores_v.tdc_pais )
)
INSERT INTO mundo_valores_v.tdc_pais (cod_pais,pais,country,continente,cod_moneda,moneda,cod_region,region,fec_carga)
SELECT *
FROM inserciones;   

-- --------------------------------------------------------------------

with inserciones as (
	SELECT DISTINCT
		bolsa,bolsa_integrada,cod_bolsa_integrada,cod_region,fec_carga
	FROM mundo_valores_act.dim_bolsa_valores
	WHERE cod_bolsa_integrada not in (select distinct cod_bolsa_integrada from mundo_valores_v.dim_bolsa_valores)
)
INSERT INTO mundo_valores_v.dim_bolsa_valores (bolsa,bolsa_integrada,cod_bolsa_integrada,cod_region,fec_carga)
SELECT *
FROM inserciones;   

-- --------------------------------------------------------------------

with inserciones as (
	SELECT DISTINCT 
		exchange,cod_exchange,year_fundacion,regulacion,comision_media,
		metodos_pago,variedad_catalogo,seguridad,tipo_servicios,soporte_cliente,fec_carga
	FROM mundo_valores_act.dim_exchange_cripto
	-- primary key (cod_exchange)
	WHERE cod_exchange not in ( select distinct cod_exchange from mundo_valores_v.dim_exchange_cripto )

)
INSERT INTO mundo_valores_v.dim_exchange_cripto (exchange,cod_exchange,year_fundacion,regulacion,comision_media,
										  metodos_pago,variedad_catalogo,seguridad,tipo_servicios,soporte_cliente,fec_carga)
SELECT *
FROM inserciones;   

-- ****************************************
-- 3) hh_historico_cotizacion
-- ****************************************

with ya_insertadas as (
	
	SELECT DISTINCT 
		tick,
		cod_bolsa,
		max(fec_dato) as max_fec_dato
	-- primary key (tick,cod_bolsa,fec_dato)
	from mundo_valores_v.hh_historico_cotizacion
	group by 1,2
	
), inserciones as (
	
	SELECT DISTINCT 
		h.*,
		case 
			when h.tick||h.cod_bolsa not in ( select distinct tick||cod_bolsa from ya_insertadas ) then 'S'
			when h.tick||h.cod_bolsa in ( select distinct tick||cod_bolsa from ya_insertadas ) 
				 and h.fec_dato > ya.max_fec_dato then 'S'
			else 'N'
		end as a_insertar		
	FROM mundo_valores_act.hh_historico_cotizacion h
	left join ya_insertadas ya 
		on (ya.tick = h.tick and ya.cod_bolsa = h.cod_bolsa)
)
INSERT INTO mundo_valores_v.hh_historico_cotizacion (par,tick,cod_bolsa,fec_dato,dia_semana,
													cierre,apertura,maximo,minimo,vol_negociado,var_porcentual,fec_carga)
SELECT DISTINCT 
	par,tick,cod_bolsa,fec_dato,dia_semana,
	cierre,apertura,maximo,minimo,vol_negociado,var_porcentual,fec_carga
FROM inserciones
WHERE a_insertar = 'S';

-- ****************************************
-- 4) dim_divisas, dim_fis
-- ****************************************

with inserciones as (
	SELECT DISTINCT
		tick,divisa,fec_carga
	FROM mundo_valores_act.dim_divisas
	-- primary key (tick)
	WHERE tick not in (select distinct tick from mundo_valores_v.dim_divisas)
)
INSERT INTO mundo_valores_V.dim_divisas (tick,divisa,fec_carga)
SELECT *
FROM inserciones;

-- --------------------------------------------------------------------

with inserciones as (
	SELECT DISTINCT 
		tick,FI,ISIN,emisor,cod_pais_emisor,tipo_valor_subyacente,
		categoria,rating_morningstar,fec_carga
	FROM mundo_valores_act.dim_FIs
	-- primary key (tick)
	where tick not in ( select distinct tick from mundo_valores_v.dim_FIs )
)
INSERT INTO mundo_valores_v.dim_FIs (tick,FI,ISIN,emisor,cod_pais_emisor,tipo_valor_subyacente,
									 categoria,rating_morningstar,fec_carga)
SELECT *
FROM inserciones;

-- ****************************************
-- 5) dim_criptomonedas, h_cripto_emisiones
-- ****************************************

with inserciones as (
	SELECT DISTINCT
		tick,cripto,fec_carga
	FROM mundo_valores_act.dim_criptomonedas
	-- primary key (tick)
	WHERE tick not in (select distinct tick from mundo_valores_v.dim_criptomonedas )
)
INSERT INTO mundo_valores_v.dim_criptomonedas (tick,cripto,fec_carga)
SELECT *
FROM inserciones;

-- --------------------------------------------------------------------

with ya_insertadas as (
	
	SELECT DISTINCT
		tick,
		max(fec_dato) as max_fec_dato
	from mundo_valores_v.h_cripto_emisiones
	group by 1 

), inserciones as (
	
	SELECT DISTINCT
		h.*,
		case
			when h.tick not in (select distinct tick from mundo_valores_v.h_cripto_emisiones) then 'S'
			when h.tick in (select distinct tick from mundo_valores_v.h_cripto_emisiones) and
				 h.fec_dato > ya.max_fec_dato then 'S'
			else 'N'
		end as a_insertar
	FROM mundo_valores_act.h_cripto_emisiones h
	left join ya_insertadas ya on ya.tick = h.tick
)
INSERT INTO mundo_valores_v.h_cripto_emisiones (fec_dato,dia_semana,tick,oferta_actual,oferta_maxima,fec_carga)
SELECT 
	fec_dato,dia_semana,tick,oferta_actual,oferta_maxima,fec_carga
FROM inserciones
where a_insertar = 'S';

-- ****************************************
-- 6) Resto de TDCs
-- ****************************************

WITH inserciones as (
	SELECT DISTINCT
		cod_industria,industria,fec_carga
	FROM mundo_valores_act.tdc_industria
	-- primary key (cod_industria)
	WHERE cod_industria not in ( select distinct cod_industria from mundo_valores_v.tdc_industria )
)
INSERT INTO mundo_valores_v.tdc_industria (cod_industria,industria,fec_carga)
SELECT *
FROM inserciones;

-- --------------------------------------------------------------------

with inserciones as (
	SELECT DISTINCT
		cod_sector,sector,fec_carga
	FROM mundo_valores_act.tdc_sector
	-- primary key (cod_sector)
	WHERE cod_sector not in ( select distinct cod_sector from mundo_valores_v.tdc_sector )
)
INSERT INTO mundo_valores_v.tdc_sector (cod_sector,sector,fec_carga)
SELECT *
FROM inserciones;

-- --------------------------------------------------------------------

with inserciones as (
	SELECT DISTINCT *
	FROM mundo_valores_act.tdc_estados
	-- primary key (cod_sector,cod_magnitud)
	WHERE cod_sector||cod_magnitud not in ( select distinct cod_sector||cod_magnitud from mundo_valores_v.tdc_estados )
)
INSERT INTO mundo_valores_v.tdc_estados (cod_sector,estado_contable,cod_magnitud,magnitud,fec_carga)
SELECT *
FROM inserciones;
										 
-- ****************************************
-- 7) dim_acciones y sus Hs
-- ****************************************
										 
with inserciones as (
	SELECT DISTINCT *
	FROM mundo_valores_act.dim_acciones
	-- primary key (tick)
	WHERE tick not in ( select distinct tick from  mundo_valores_v.dim_acciones )
) 
INSERT INTO mundo_valores_v.dim_acciones (tick,empresa,sede,cod_pais_sede,cod_industria,cod_sector,fec_carga)
SELECT *
FROM inserciones;
										 
-- --------------------------------------------------------------------

with ya_insertadas as (
	
	SELECT DISTINCT 
		tick,
		max(fec_dividendo) as max_fec_dividendo
	-- primary key (tick,fec_dividendo)
	FROM mundo_valores_v.h_acc_dividendos
	GROUP BY 1
	
), inserciones as (
	
	SELECT DISTINCT
		h.*,
		case
			when h.tick not in (select distinct tick from ya_insertadas) then 'S'
			when h.tick in (select distinct tick from ya_insertadas) 
		         and h.fec_dividendo > ya.max_fec_dividendo then 'S'
			else 'N'
		end as a_insertar
	FROM mundo_valores_act.h_acc_dividendos h
	LEFT JOIN ya_insertadas ya on ya.tick = h.tick
)
										 
INSERT INTO mundo_valores_v.h_acc_dividendos (tick,fec_dividendo,dividendo,fec_carga)
SELECT 
	tick,fec_dividendo,dividendo,fec_carga
FROM inserciones
WHERE a_insertar = 'S';
					
-- --------------------------------------------------------------------
										 
with ya_insertadas as (

	SELECT DISTINCT
		tick,
		cod_sector,
		anio,
		periodo,
		cod_magnitud,
		'S' as ya_existe
	FROM mundo_valores_v.h_estados_contables
										 
), inserciones as (
	
	SELECT DISTINCT
		h.*,
		case
			when coalesce(ya_existe,'N') = 'N' then 'S'
			else 'N'
		end as a_insertar
	FROM mundo_valores_act.h_estados_contables h
	LEFT JOIN ya_insertadas ya ON ( ya.tick = h.tick and 
								   	ya.cod_sector = h.cod_sector and
								    ya.periodo = h.periodo and
								    ya.anio = h.anio and
								    ya.cod_magnitud = h.cod_magnitud )
)				
INSERT INTO mundo_valores_v.h_estados_contables (tick,cod_sector,anio,periodo,cod_magnitud,valor_magnitud,fec_carga)
SELECT 
	tick,cod_sector,anio,periodo,cod_magnitud,valor_magnitud,fec_carga
FROM inserciones
WHERE a_insertar = 'S';

-- ****************************************
-- 7) dim_indices y dim_ETFs
-- ****************************************
										 
with inserciones as (
	SELECT DISTINCT
		tick,indice,cod_bolsa,cod_pais_referencia,fec_carga
	FROM mundo_valores_act.dim_indices
	-- primary key (tick)
	WHERE tick not in ( select distinct tick from mundo_valores_v.dim_indices )
)
INSERT INTO mundo_valores_v.dim_indices (tick,indice,cod_bolsa,cod_pais_referencia,fec_carga)
SELECT *
FROM inserciones;

-- --------------------------------------------------------------------

with inserciones as (
	SELECT DISTINCT
		tick,ETF,ISIN,emisor,tipo_valor_subyacente,subyacente,fec_carga
	FROM mundo_valores_act.dim_ETFs
	-- primary key (tick)
	WHERE tick not in ( select distinct tick from mundo_valores_v.dim_ETFs)
)										 
INSERT INTO mundo_valores_act.dim_ETFs (tick,ETF,ISIN,emisor,tipo_valor_subyacente,subyacente,fec_carga)
SELECT *
FROM inserciones;

/*
-- recuento de registros por tabla
SELECT DISTINCT
	schemaname as schema, 
	relname as tabla, 
	n_live_tup as num_filas
FROM pg_stat_user_tables
ORDER BY n_live_tup DESC;
*/