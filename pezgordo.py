import duckdb
con = duckdb.connect()
CSV = "/home/thinkpad/Documentos/hackaton/SECOP_II_-_Contratos_Electrónicos_20260506.csv"
con.execute(f"""CREATE VIEW d AS SELECT * FROM read_csv_auto(
    '{CSV}', sample_size=-1, ignore_errors=true, header=true, quote='"', escape='"')""")

# Convertir 'Valor del Contrato' (formato colombiano: 1.234.567,89 o solo dígitos)
# Estrategia robusta: si tiene coma decimal -> formato CO; si no -> directo
con.execute("""CREATE OR REPLACE VIEW v AS
SELECT *,
  CASE
    WHEN "Valor del Contrato" LIKE '%,%'
      THEN try_cast(replace(replace("Valor del Contrato", '.', ''), ',', '.') AS DOUBLE)
    ELSE try_cast("Valor del Contrato" AS DOUBLE)
  END AS valor_num
FROM d""")

print("=== PEZ GORDO: top reps con 10+ entidades, ordenado por monto total ===")
print(con.execute("""
SELECT "Nombre Representante Legal" rep,
       "Identificación Representante Legal" cc,
       count(*) n_contratos,
       count(DISTINCT "Nombre Entidad") n_entidades,
       count(DISTINCT "Departamento") n_dept,
       count(DISTINCT "Ciudad") n_ciudades,
       round(sum(valor_num),0) monto_total
FROM v
WHERE "Nombre Representante Legal" IS NOT NULL
  AND "Nombre Representante Legal" NOT IN ('Sin Descripcion','Sin Descripción','No Definido')
GROUP BY 1,2
HAVING count(DISTINCT "Nombre Entidad") >= 10
ORDER BY monto_total DESC NULLS LAST
LIMIT 15""").df().to_string())

print("\n=== Mismo top pero ordenado por # entidades ===")
print(con.execute("""
SELECT "Nombre Representante Legal" rep,
       "Identificación Representante Legal" cc,
       "Domicilio Representante Legal" dir,
       count(*) n_contratos,
       count(DISTINCT "Nombre Entidad") n_entidades,
       count(DISTINCT "Departamento") n_dept,
       count(DISTINCT "Ciudad") n_ciudades,
       round(sum(valor_num),0) monto_total
FROM v
WHERE "Nombre Representante Legal" IS NOT NULL
  AND "Nombre Representante Legal" NOT IN ('Sin Descripcion','Sin Descripción','No Definido')
GROUP BY 1,2,3
HAVING count(DISTINCT "Nombre Entidad") >= 10
ORDER BY n_entidades DESC
LIMIT 15""").df().to_string())
