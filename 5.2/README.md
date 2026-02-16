# Tec de Monterrey | Maestría en Inteligencia Artificial (MNA)
## Pruebas de software y aseguramiento de la calidad (Gpo 10)

David A. Serrano Garcia  
**Matrícula:** A01795935  
**Correo:** a01795935@tec.mx  

---

# Actividad 5.2 - Compute Sales (Evidencia de ejecución)

Este repositorio contiene el programa **computeSales.py** para calcular el total de ventas a partir de:
1) Un catálogo de precios (JSON)  
2) Un registro de ventas (JSON)

La ejecución se realiza desde la raíz del proyecto `5.2/` usando el `Makefile`.

---

## Estructura del proyecto
- Raíz del proyecto: [`5.2/`](./)
- Makefile: [`5.2/Makefile`](./Makefile)

### Código fuente
- CLI (requerido por la actividad): [`5.2/src/computeSales.py`](./src/computeSales.py)
- Paquete con lógica pura: [`5.2/src/compute_sales/`](./src/compute_sales/)
  - Lógica de cálculo: [`5.2/src/compute_sales/main.py`](./src/compute_sales/main.py)
  - Export público: [`5.2/src/compute_sales/__init__.py`](./src/compute_sales/__init__.py)

### Datos de entrada (incluidos para la evidencia)
- Catálogo de precios: [`5.2/data/priceCatalogue.json`](./data/priceCatalogue.json)
- Registro de ventas: [`5.2/data/salesRecord.json`](./data/salesRecord.json)

### Evidencia de resultados
- Archivo generado (Req 2): [`5.2/output/SalesResults.txt`](./output/SalesResults.txt)

### Evidencia de ejecución (logs)
- Logs de ejecución del programa: [`5.2/logs/run/`](./logs/run/)
  - Patrón: `run_YYYYMMDD_HHMMSS.stdout.log` y `run_YYYYMMDD_HHMMSS.stderr.log`
- Logs de pruebas unitarias: [`5.2/logs/test/`](./logs/test/)
  - Patrón: `test_YYYYMMDD_HHMMSS.stdout.log` y `test_YYYYMMDD_HHMMSS.stderr.log`

### Pruebas
- Suite de pruebas: [`5.2/tests/test_compute_sales.py`](./tests/test_compute_sales.py)
- Entradas de casos de prueba:
  - [`5.2/tests/fixtures/valid/TC1/`](./tests/fixtures/valid/TC1/)
  - [`5.2/tests/fixtures/valid/TC2/`](./tests/fixtures/valid/TC2/)
  - [`5.2/tests/fixtures/valid/TC3/`](./tests/fixtures/valid/TC3/)
- Totales esperados (oracle): [`5.2/tests/expected/Results.txt`](./tests/expected/Results.txt)

---

## Requisitos cubiertos

### Req 1. Invocación por línea de comandos con dos archivos
El programa se ejecuta con:
```bash
python src/computeSales.py data/priceCatalogue.json data/salesRecord.json

Req 2. Cálculo total y salida a consola y archivo SalesResults.txt
	•	Imprime en consola un reporte legible para el usuario.
	•	Genera el archivo:
	•	output/SalesResults.txt￼

Req 3. Manejo de datos inválidos sin detener ejecución
	•	Errores y advertencias se imprimen en stderr con prefijos:
	•	[ERROR] ...
	•	[WARN] ...
	•	La ejecución continúa y el programa genera salida con lo que sea posible procesar.

Req 4. Nombre del programa
	•	El entrypoint requerido es: src/computeSales.py￼

Req 5. Formato mínimo de invocación

python computeSales.py priceCatalogue.json salesRecord.json

En este repositorio:

python src/computeSales.py data/priceCatalogue.json data/salesRecord.json

Req 6. Escalabilidad (cientos a miles de items)
	•	La lógica de cálculo usa un mapa title -> price para búsqueda O(1) por producto.
	•	El cálculo es lineal respecto al número de registros de ventas.

Req 7. Tiempo transcurrido
	•	El reporte incluye el tiempo de ejecución:
	•	En consola
	•	En output/SalesResults.txt

Req 8. PEP8
	•	Se incluye flake8 y black en el flujo del repositorio.
	•	El Makefile contiene targets para lint y format (si están habilitados en tu versión final).

⸻

Cómo ejecutar

1) Instalar dependencias

make install

Esto crea .venv/ e instala:
	•	pytest
	•	flake8
	•	black

2) Ejecutar el programa (genera logs)

make run

Evidencia:
	•	Resultado final: output/SalesResults.txt￼
	•	Logs:
	•	logs/run/￼

3) Ejecutar tests (genera logs)

make test

Evidencia:
	•	Logs:
	•	logs/test/￼

⸻

Evidencia de ejecución incluida

Ejecución del programa
	•	Logs exitosos:
	•	logs/run/run_20260215_175723.stdout.log￼
	•	logs/run/run_20260215_175723.stderr.log￼
	•	Ejemplo de ejecución con errores (archivos no encontrados):
	•	logs/run/run_20260215_175504.stdout.log￼
	•	logs/run/run_20260215_175504.stderr.log￼

Ejecución de pruebas
	•	Ejecución exitosa:
	•	logs/test/test_20260215_175119.stdout.log￼
	•	logs/test/test_20260215_175119.stderr.log￼

⸻

Notas de diseño
	•	Separación de responsabilidades:
	•	compute_sales contiene solo lógica de negocio (probada por unit tests).
	•	computeSales.py implementa el CLI: lectura de archivos, validación defensiva, cronometraje, reporte y escritura del archivo.
	•	Formato legible:
	•	Se imprime un reporte con encabezado, rutas de archivos, total, tiempo y sección de warnings cuando aplica.

⸻


