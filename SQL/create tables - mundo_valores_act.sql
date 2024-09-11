-- CREATE SCHEMA mundo_valores_act
-- DROP SCHEMA mundo_valores_act CASCADE;

/*

REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA mundo_valores_act FROM readuser1;
REVOKE USAGE ON SCHEMA mundo_valores_act FROM readUser1;

GRANT USAGE ON SCHEMA mundo_valores_act TO readuser1;
GRANT SELECT ON ALL TABLES IN SCHEMA mundo_valores_act TO readuser1;

*/

/*************************************************************************************************/
/*************************************************************************************************/

create table mundo_valores_act.sdim_valores
(
	tipo_valor				VARCHAR(100) not null,
	tick					VARCHAR(100) not null,
	fec_carga 				TIMESTAMP not null,
	primary key (tick)
);

create table mundo_valores_act.sdim_mercados
(
	tipo_mercado			VARCHAR(100) ,
	tipo_bolsa				VARCHAR(100) ,
	cod_bolsa	 			VARCHAR(100) not null,
	fec_carga 				TIMESTAMP not null, 
	primary key (cod_bolsa)
);

/*************************************************************************************************/
/*************************************************************************************************/

CREATE TABLE IF NOT EXISTS mundo_valores_act.tdc_pais
(
	cod_pais 					VARCHAR(100),
	pais						VARCHAR(100),
	country						VARCHAR(100),
	continente					VARCHAR(100),
	cod_moneda 					VARCHAR(100),
	moneda						VARCHAR(100),
	cod_region					VARCHAR(100) not null,
	region						VARCHAR(100) not null,
	fec_carga 					TIMESTAMP not null,
	primary key (cod_region)

);

create table mundo_valores_act.dim_bolsa_valores 
(
	bolsa 					VARCHAR(100),
	bolsa_integrada			VARCHAR(100) not null,
	cod_bolsa_integrada		VARCHAR(100) not null,
	cod_region				VARCHAR(100),
	fec_carga 				TIMESTAMP not null,
	primary key (cod_bolsa_integrada)
);

create table mundo_valores_act.dim_exchange_cripto 
(
	exchange 					VARCHAR(100) not null,
	cod_exchange				VARCHAR(100) not null,
	year_fundacion				int,
	regulacion					VARCHAR(100),
	comision_media				DOUBLE PRECISION,
	metodos_pago				VARCHAR(100),
	variedad_catalogo 			VARCHAR(100),
	seguridad					VARCHAR(100),
	tipo_servicios				VARCHAR(100),
	soporte_cliente				VARCHAR(100),
	fec_carga 					TIMESTAMP not null,
	primary key (cod_exchange)
);

/*************************************************************************************************/
/*************************************************************************************************/

-- Tabla que contiene los históricos de cotizacion de los valores
 create table mundo_valores_act.hh_historico_cotizacion
(
	par				VARCHAR(100) not null,
	tick			VARCHAR(100) not null,
	cod_bolsa	    VARCHAR(100) not null,
	fec_dato 		DATE not null,
	dia_semana 		VARCHAR(100) not null,
	cierre 			DOUBLE PRECISION,
	apertura		DOUBLE PRECISION,
	maximo			DOUBLE PRECISION,
	minimo			DOUBLE PRECISION,
	vol_negociado	DOUBLE PRECISION,
	var_porcentual 	DOUBLE PRECISION,
	fec_carga 		TIMESTAMP not null,
	primary key (tick,cod_bolsa,fec_dato)
);

/*************************************************************************************************/
/*************************************************************************************************/

create table mundo_valores_act.dim_divisas
(
	tick				VARCHAR(100) not null,
	divisa				VARCHAR(100) not null,		
	fec_carga 			TIMESTAMP not null,
	primary key (tick)
);

create table mundo_valores_act.dim_FIs
(
	tick					VARCHAR(100) not null,
	FI						VARCHAR(100) not null,
	ISIN					VARCHAR(100),
	emisor					VARCHAR(100) not null,
	cod_pais_emisor			VARCHAR(100) not null,
	tipo_valor_subyacente   VARCHAR(100) not null,
	categoria				VARCHAR(100) not null,
	rating_morningstar	 	VARCHAR(100) not null,
	fec_carga 				TIMESTAMP not null,
	primary key (tick)
);

/*************************************************************************************************/
/*************************************************************************************************/

-- DELETE FROM mundo_valores_act.dim_criptomonedas;
create table mundo_valores_act.dim_criptomonedas
(
	tick					VARCHAR(100) not null,
	cripto					VARCHAR(100) not null,
	fec_carga 				TIMESTAMP not null,
	primary key (tick)
	
);

create table mundo_valores_act.h_cripto_emisiones
(
	fec_dato 				DATE not null,
	dia_semana 				VARCHAR(100) not null,
	tick					VARCHAR(100) not null,
	oferta_actual			DOUBLE PRECISION,
	oferta_maxima			DOUBLE PRECISION,
	fec_carga 				TIMESTAMP not null,
	primary key (fec_dato,tick)
	
);

/*************************************************************************************************/
/*************************************************************************************************/

create table mundo_valores_act.tdc_industria (
	cod_industria			VARCHAR(100) not null,
	industria				VARCHAR(100) not null,
	fec_carga 				TIMESTAMP not null, 
	primary key (cod_industria)
);

create table mundo_valores_act.tdc_sector (
	cod_sector				VARCHAR(100) not null,
	sector					VARCHAR(100) not null,
	fec_carga 				TIMESTAMP not null,
	primary key (cod_sector)
);

create table mundo_valores_act.tdc_estados (
	cod_sector				VARCHAR(100) not null,
	estado_contable			VARCHAR(100) not null,
	cod_magnitud			VARCHAR(100) not null,
	magnitud				VARCHAR(500) not null,
	fec_carga 				TIMESTAMP not null,
	primary key (cod_sector,cod_magnitud)
);

-- DROP TABLE mundo_valores_act.dim_acciones CASCADE
create table mundo_valores_act.dim_acciones
(
	tick					VARCHAR(100) not null,
	empresa					VARCHAR(100) not null,
	sede					VARCHAR(100) not null,
	cod_pais_sede			VARCHAR(100) not null,
	cod_industria			VARCHAR(100) not null,
	cod_sector				VARCHAR(100) not null,
	fec_carga 				TIMESTAMP not null,
	primary key (tick)
);

-- DROP TABLE mundo_valores_act.h_acc_dividendos 
create table mundo_valores_act.h_acc_dividendos
(
	tick					VARCHAR(100) not null,
	fec_dividendo			VARCHAR(100) not null,
	dividendo				DOUBLE PRECISION not null,
	fec_carga 				TIMESTAMP not null,
	primary key (tick,fec_dividendo)
);

-- DROP TABLE mundo_valores_act.h_estados_contables 
create table mundo_valores_act.h_estados_contables
(
	tick					VARCHAR(100) not null,
	cod_sector				VARCHAR(100) not null,
	anio					INT not null,
	periodo					VARCHAR(100) not null,
	cod_magnitud			VARCHAR(100) not null,
	valor_magnitud			DOUBLE PRECISION,
	fec_carga 				TIMESTAMP not null,
	primary key (tick,cod_sector,anio,periodo,cod_magnitud)
);

/*************************************************************************************************/
/*************************************************************************************************/

create table mundo_valores_act.dim_indices
(
	tick					VARCHAR(100) not null,
	indice					VARCHAR(100) not null,
	cod_bolsa				VARCHAR(100) not null,
	cod_pais_referencia	 	VARCHAR(100) not null,
	fec_carga 				TIMESTAMP,
	primary key (tick)
);

create table mundo_valores_act.dim_ETFs
(
	tick					VARCHAR(100) not null,
	ETF						VARCHAR(100) not null,
	ISIN					VARCHAR(100),
	emisor					VARCHAR(100),
	tipo_valor_subyacente   VARCHAR(100),
	subyacente   	 		VARCHAR(100),
	fec_carga 				TIMESTAMP,
	primary key (tick)
);

/*************************************************************************************************/
/*************************************************************************************************/

/*
DO $$
DECLARE
    tabla_actual text;
    dep record;
BEGIN
    -- Obtener el nombre de todas las tablas en el esquema 'mundo_valores_act'
    FOR tabla_actual IN 
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'mundo_valores_act' AND table_type = 'BASE TABLE'
    LOOP
    	EXECUTE 'DROP TABLE IF EXISTS mundo_valores_act.' || tabla_actual || ' CASCADE';
    END LOOP;
END $$;

*/

/*************************************************************************************************/
/*************************************************************************************************/

/*
-- recuento de registros por tabla
SELECT DISTINCT
	schemaname as schema, 
	relname as tabla, 
	n_live_tup as num_filas
FROM pg_stat_user_tables
where schemaname = 'mundo_valores_v'
ORDER BY n_live_tup DESC;
*/
