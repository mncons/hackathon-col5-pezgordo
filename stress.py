import duckdb, os
con = duckdb.connect()
CSV = "/home/thinkpad/Documentos/hackaton/SECOP_II_-_Contratos_Electrónicos_20260506.csv"
con.execute(f"""CREATE VIEW d AS SELECT * FROM read_csv_auto(
    '{CSV}', sample_size=-1, ignore_errors=true, header=true, quote='"', escape='"')""")

print("=== 1. Entidades Gotham/Gótica/Arkham/Wayne ===")
print(con.execute("""
SELECT "Nombre Entidad", count(*) n FROM d
WHERE upper("Nombre Entidad") LIKE '%GOTHAM%'
   OR upper("Nombre Entidad") LIKE '%GOTICA%'
   OR upper("Nombre Entidad") LIKE '%GÓTICA%'
   OR upper("Nombre Entidad") LIKE '%ARKHAM%'
   OR upper("Nombre Entidad") LIKE '%WAYNE%'
GROUP BY 1 ORDER BY n DESC LIMIT 20""").df().to_string())

print("\n=== 2. Bruce Wayne como representante ===")
print(con.execute("""
SELECT "Nombre Representante Legal" rep,
       "Identificación Representante Legal" cc,
       "Domicilio Representante Legal" dir,
       count(*) n_contratos,
       count(DISTINCT "Nombre Entidad") n_entidades,
       count(DISTINCT "Departamento") n_dept,
       count(DISTINCT "Ciudad") n_ciudades
FROM d
WHERE upper("Nombre Representante Legal") LIKE '%WAYNE%'
   OR upper("Nombre Representante Legal") LIKE '%BRUCE%'
   OR "Identificación Representante Legal" = '11223344'
GROUP BY 1,2,3 ORDER BY n_contratos DESC LIMIT 20""").df().to_string())

print("\n=== 3. Top reps con 10+ entidades distintas ===")
print(con.execute("""
SELECT "Nombre Representante Legal" rep,
       "Identificación Representante Legal" cc,
       count(*) n_contratos,
       count(DISTINCT "Nombre Entidad") n_entidades,
       count(DISTINCT "Departamento") n_dept,
       count(DISTINCT "Ciudad") n_ciudades
FROM d
WHERE "Nombre Representante Legal" IS NOT NULL
GROUP BY 1,2
HAVING count(DISTINCT "Nombre Entidad") >= 10
ORDER BY n_entidades DESC, n_contratos DESC LIMIT 30""").df().to_string())

print("\n=== 4. Buscar supervisores Alfred/Lucius/Gordon ===")
print(con.execute("""
SELECT DISTINCT "Nombre supervisor", "Número de documento supervisor"
FROM d
WHERE upper("Nombre supervisor") LIKE '%ALFRED%'
   OR upper("Nombre supervisor") LIKE '%LUCIUS%'
   OR upper("Nombre supervisor") LIKE '%PENNYWORTH%'
   OR upper("Nombre supervisor") LIKE '%GORDON%'
   OR "Número de documento supervisor" IN ('55667788','99887766','44332211')
LIMIT 20""").df().to_string())

print("\n=== 5. CC 11223344 directo ===")
print(con.execute("""
SELECT * FROM d
WHERE "Identificación Representante Legal" = '11223344' LIMIT 5""").df().to_string())
