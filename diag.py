import duckdb
con = duckdb.connect()
con.execute("""CREATE VIEW d AS SELECT * FROM read_csv_auto(
    '/home/thinkpad/Documentos/hackaton/SECOP_II_-_Contratos_Electrónicos_20260506.csv',
    sample_size=-1, ignore_errors=true, header=true, quote='"', escape='"')""")

print("Muestra de 'Valor del Contrato' (10 valores):")
print(con.execute("""SELECT "Valor del Contrato" FROM d
WHERE "Valor del Contrato" IS NOT NULL AND "Valor del Contrato" <> ''
LIMIT 10""").df().to_string())

print("\n¿Cuántos parsean como DOUBLE directo?")
print(con.execute("""SELECT
  count(*) total,
  count("Valor del Contrato") no_null,
  count(try_cast("Valor del Contrato" AS DOUBLE)) plain,
  count(try_cast(replace("Valor del Contrato", ',', '.') AS DOUBLE)) coma_punto,
  count(try_cast(replace(replace("Valor del Contrato",'.',''),',','.') AS DOUBLE)) co_format,
  count(try_cast(regexp_replace("Valor del Contrato",'[^0-9.-]','','g') AS DOUBLE)) limpio
FROM d""").df().to_string())
