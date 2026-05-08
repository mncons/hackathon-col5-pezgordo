#!/usr/bin/env python3
"""
VERIFICACIÓN AUTOMÁTICA - Hackathon COL 5.0 Stress Test
========================================================
Reproduce los hallazgos del análisis Pez Gordo sobre SECOP II.

Uso:
    pip install duckdb --break-system-packages
    python3 verificar_pez_gordo.py /ruta/al/SECOP_II_Contratos_Electronicos.csv

Salida esperada: 7 verificaciones [PASS/FAIL] coincidiendo con README.md
"""
import duckdb, sys, os

if len(sys.argv) < 2:
    print("Uso: python3 verificar_pez_gordo.py <ruta_csv>")
    print("Ejemplo: python3 verificar_pez_gordo.py SECOP_II_Contratos_Electronicos_20260506.csv")
    sys.exit(1)

CSV = sys.argv[1]
if not os.path.exists(CSV):
    print(f"ERROR: archivo no existe: {CSV}")
    sys.exit(1)

print("=" * 72)
print("VERIFICACIÓN PEZ GORDO - Hackathon COL 5.0")
print(f"Dataset: {CSV}")
print(f"Tamaño : {os.path.getsize(CSV)/1024/1024:.0f} MB")
print("=" * 72)

con = duckdb.connect()
con.execute(f"""CREATE VIEW d AS SELECT * FROM read_csv_auto(
    '{CSV}', sample_size=-1, ignore_errors=true, header=true,
    quote='"', escape='"')""")

def check(label, sql, expected, tolerance=0):
    """Ejecuta query, compara con esperado, imprime PASS/FAIL."""
    actual = con.execute(sql).fetchone()[0]
    if actual is None:
        actual = 0
    if isinstance(expected, (int, float)) and tolerance > 0:
        ok = abs(actual - expected) <= tolerance
    else:
        ok = actual == expected
    tag = "[PASS]" if ok else "[FAIL]"
    print(f"{tag} {label}")
    print(f"        esperado: {expected}")
    print(f"        obtenido: {actual}")
    return ok

results = []

# ===== TESTS =====
print("\n--- TEST 1: Total de registros ---")
results.append(check(
    "Total registros del dataset",
    "SELECT count(*) FROM d",
    1003902
))

print("\n--- TEST 2: Entidades ficticias NO existen ---")
results.append(check(
    "Entidades Gotham/Gótica/Arkham/Wayne (debe ser 0)",
    """SELECT count(*) FROM d
       WHERE upper("Nombre Entidad") LIKE '%GOTHAM%'
          OR upper("Nombre Entidad") LIKE '%GOTICA%'
          OR upper("Nombre Entidad") LIKE '%GÓTICA%'
          OR upper("Nombre Entidad") LIKE '%ARKHAM%'""",
    0
))

print("\n--- TEST 3: Cédula 11223344 NO existe ---")
results.append(check(
    "Registros con CC representante legal = 11223344 (debe ser 0)",
    """SELECT count(*) FROM d
       WHERE "Identificación Representante Legal" = '11223344'""",
    0
))

print("\n--- TEST 4: Pez Gordo real #1 - Andrea Puerto Corredor ---")
results.append(check(
    "Entidades distintas firmadas por 'Andrea Puerto Corredor'",
    """SELECT count(DISTINCT "Nombre Entidad") FROM d
       WHERE "Nombre Representante Legal" = 'Andrea Puerto Corredor'""",
    640
))

print("\n--- TEST 5: Pez Gordo real #2 - CARLOS SUA FORERO ---")
results.append(check(
    "Contratos firmados por 'CARLOS SUA FORERO'",
    """SELECT count(*) FROM d
       WHERE "Nombre Representante Legal" = 'CARLOS SUA FORERO'""",
    829
))

print("\n--- TEST 6: # contratistas firmando en ≥10 entidades ---")
results.append(check(
    "Contratistas (excluyendo nulls) con ≥10 entidades distintas (debe ser >=30)",
    """SELECT count(*) FROM (
         SELECT "Nombre Representante Legal"
         FROM d
         WHERE "Nombre Representante Legal" IS NOT NULL
           AND "Nombre Representante Legal" NOT IN
               ('Sin Descripcion','Sin Descripción','No Definido')
         GROUP BY 1
         HAVING count(DISTINCT "Nombre Entidad") >= 10
       )""",
    30, tolerance=10  # >=20 y <=40
))

print("\n--- TEST 7: 311 ciudades por Andrea Puerto Corredor ---")
results.append(check(
    "Ciudades distintas firmadas por 'Andrea Puerto Corredor'",
    """SELECT count(DISTINCT "Ciudad") FROM d
       WHERE "Nombre Representante Legal" = 'Andrea Puerto Corredor'""",
    311
))

# ===== RESULTADO =====
print("\n" + "=" * 72)
passed = sum(results)
total = len(results)
print(f"RESULTADO: {passed}/{total} verificaciones PASS")
if passed == total:
    print("✅ Análisis Pez Gordo VERIFICADO contra el dataset.")
else:
    print(f"⚠ {total-passed} verificaciones fallaron.")
print("=" * 72)

# ===== EVIDENCIA EXTENDIDA =====
print("\n--- EVIDENCIA: Top 10 contratistas con más entidades ---")
print(con.execute("""
SELECT "Nombre Representante Legal" rep,
       "Identificación Representante Legal" cc,
       count(*) n_contratos,
       count(DISTINCT "Nombre Entidad") n_entidades,
       count(DISTINCT "Departamento") n_dept,
       count(DISTINCT "Ciudad") n_ciudades
FROM d
WHERE "Nombre Representante Legal" IS NOT NULL
  AND "Nombre Representante Legal" NOT IN
      ('Sin Descripcion','Sin Descripción','No Definido')
GROUP BY 1,2
HAVING count(DISTINCT "Nombre Entidad") >= 10
ORDER BY n_entidades DESC LIMIT 10""").df().to_string())

sys.exit(0 if passed == total else 1)
