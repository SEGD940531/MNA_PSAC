# Actividad 6.2 - Ejercicio de programación 3

**Tec de Monterrey | Maestría en Inteligencia Artificial (MNA)**  
Pruebas de software y aseguramiento de la calidad (Gpo 10)  

David A. Serrano Garcia  
Matrícula: A01795935  
Correo: [a01795935@tec.mx](mailto:a01795935@tec.mx)

---

## Estrategia de desarrollo

> A continuación describo de forma breve la estrategia de desarrollo que seguí, la cual resume el flujo de trabajo aplicado en este proyecto.

El desarrollo se realizó de forma incremental:

1. **Estructura base del proyecto**  
   Primero se definió la estructura del proyecto ([`src/`](./src), [`tests/`](./tests), [`logs/`](./logs), [`data/`](./data), [`output/`](./output)) junto con el [`Makefile`](./Makefile) para poder ejecutar todo de forma consistente.

2. **Pruebas antes de la implementación**  
   Se crearon los tests en [`tests/test_compute_sales.py`](./tests/test_compute_sales.py) utilizando los resultados esperados en [`tests/expected/Results.txt`](./tests/expected/Results.txt), aun sin tener la lógica completa, para definir el comportamiento esperado.  
   En los logs de pruebas ([`logs/test/`](./logs/test/)) se pueden ver ejecuciones iniciales con tests fallidos y posteriormente ejecuciones exitosas conforme se fue implementando la lógica.

3. **Lógica desacoplada en paquete**  
   La lógica se implementó en el paquete [`src/compute_sales/`](./src/compute_sales/) (principalmente en [`main.py`](./src/compute_sales/main.py)) como función independiente.  
   La idea de esta separación fue aislar la lógica core del programa del manejo de CLI y de archivos, de modo que la lógica sea reutilizable, fácil de probar y no dependa de la entrada/salida.

4. **Implementación del CLI**  
   Se creó el entrypoint [`src/computeSales.py`](./src/computeSales.py), encargado de la lectura de archivos, validación de datos, medición de tiempo y generación del archivo de resultados [`output/SalesResults.txt`](./output/SalesResults.txt).

5. **Calidad de código (PEP8)**  
   Se utilizaron herramientas como `flake8`, registrando resultados en [`logs/lint/`](./logs/lint/) y ajustando el código con base en sus reportes.

6. **Registro de ejecución**  
   Todas las ejecuciones generan evidencia en logs:
   - Ejecución del programa: [`logs/run/`](./logs/run/)  
   - Pruebas: [`logs/test/`](./logs/test/)  
   - Análisis estático: [`logs/lint/`](./logs/lint/)

---

## Descripción

Programa CLI en Python que calcula el total de ventas a partir de:

- Catálogo de precios (JSON)
- Registro de ventas (JSON)

Genera salida en consola y en archivo.

---

## Estructura

```
5.2/
├── Makefile
├── src/
│   ├── computeSales.py
│   └── compute_sales/
│       ├── __init__.py
│       └── main.py
├── data/
│   ├── priceCatalogue.json
│   └── salesRecord.json
├── output/
│   └── SalesResults.txt
├── logs/
│   ├── run/
│   ├── test/
│   └── lint/
└── tests/
    ├── test_compute_sales.py
    ├── fixtures/
    └── expected/
```

---

## Uso

```
python src/computeSales.py data/priceCatalogue.json data/salesRecord.json
```

---

## Makefile

Instalar dependencias:

```
make install
```

Ejecutar programa:

```
make run
```

Ejecutar pruebas:

```
make test
```

Análisis estático:

```
make lint
```

---

## Requisitos cubiertos

1. CLI con dos archivos  
2. Salida en consola y archivo  
3. Manejo de errores sin detener ejecución  
4. Entry point: `computeSales.py`  
5. Formato de ejecución estándar  
6. Escalabilidad O(n) con búsqueda O(1)  
7. Medición de tiempo de ejecución  
8. Cumplimiento PEP8  

---

## Logs

- Ejecución: `logs/run/`
- Tests: `logs/test/`
- Lint: `logs/lint/`

Formato:

```
*_YYYYMMDD_HHMMSS.stdout.log
*_YYYYMMDD_HHMMSS.stderr.log
```

---

## Pruebas

- Tests unitarios en `tests/`
- Datos en `tests/fixtures/`
- Resultados esperados en `tests/expected/`

---

## Calidad de código

Herramientas:

- flake8
- pylint
- black

Resultado:

- Score pylint: ~9+
- Sin errores críticos

---

## Diseño

- `compute_sales`: lógica pura (testable)
- `computeSales.py`: CLI, IO, validación, logging
- Manejo defensivo de errores
- Reporte claro y legible

---
