# Hackathon COL 5.0 - Stress Test Pez Gordo

Análisis de exposición de datos personales en SECOP II (1,003,902 contratos, 1.7GB CSV).

## Perfil ficticio del slide

- Nombre: Bruce Wayne
- CC: 11223344
- Dirección: Calle Gotham #100-01, Mansión Wayne
- 45 contratos / 12 entidades / $50,000,000,000 COP / 4 dept / 7 ciudades
- Supervisores: Alfred Pennyworth (55667788), Lucius Fox (99887766), James Gordon (44332211)
- Entidades: Hospital Central de Gotham, Alcaldía Ciudad Gótica, Subred Servicios Salud Arkham

## Verificación en dataset real

Búsqueda directa en SECOP II:
- Entidades Gotham/Gótica/Arkham/Wayne: 0 resultados
- CC 11223344: 0 resultados
- Supervisores Pennyworth/Fox/Gordon: 0 coincidencias

**El perfil es narrativo. El reto verdadero: identificar contratistas con concentración anómala.**

## Pez Gordo real - Top contratistas con >=10 entidades

| # | Representante | CC | Contratos | Entidades | Dept | Ciudades |
|---|---|---|---:|---:|---:|---:|
| 1 | Andrea Puerto Corredor | Sin Desc | 812 | 640 | 27 | 311 |
| 2 | CARLOS SUA FORERO | Sin Desc | 829 | 611 | 33 | 257 |
| 3 | Doris Martinez Corredor | 51740316 | 350 | 277 | 26 | 95 |
| 4 | Angela Maria Alvarez Patiño | 30402563 | 298 | 226 | 23 | 73 |
| 5 | SEGUROS DEL ESTADO S.A | 860009578-6 | 185 | 147 | 20 | 73 |

**30+ contratistas firmando en >=10 entidades distintas.** Andrea Puerto Corredor: 640 entidades en 311 ciudades = humanamente imposible.

## Hallazgos de exposición

1. Direcciones residenciales visibles sin enmascarar
2. Cédulas de personas naturales sin enmascarar
3. Concentración anómala de contratos por persona

**Marco vulnerado:** Ley 1581/2012 (Habeas Data), Decreto 1377/2013, Ley 1712/2014.

## Reproducibilidad

Scripts DuckDB en este repo: `stress.py`, `pezgordo.py`, `diag.py`, `final.py`. Resultados en `*_result.txt`.

```
pip install duckdb --break-system-packages
python3 stress.py
```
