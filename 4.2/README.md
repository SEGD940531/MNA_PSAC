# Tec de Monterrey | Maestría en Inteligencia Artificial (MNA)
## Pruebas de software y aseguramiento de la calidad (Gpo 10)

David A. Serrano Garcia  
**Matrícula:** A01795935  
**Correo:** a01795935@tec.mx  

---

# Actividad 4.2 - Evidencia de ejecución (P1, P2, P3)

Este repositorio contiene tres programas (P1, P2, P3) ejecutados desde la raíz `4.2/` usando el `Makefile`.

## Estructura
- Raíz del proyecto: [`4.2/`](./)
- Makefile: [`4.2/Makefile`](./Makefile)

### P1 - Statistics
- Código: [`4.2/P1/source/computeStatistics.py`](./P1/source/computeStatistics.py)
- Datos de entrada: [`4.2/P1/data/`](./P1/data/)
- Resultados finales: [`4.2/P1/results/StatisticsResults.txt`](./P1/results/StatisticsResults.txt)
- Logs de ejecución (por TC): [`4.2/P1/logs/`](./P1/logs/)
  - Patrón: `TC*_YYYYMMDD_HHMMSS.stdout.log` y `TC*_YYYYMMDD_HHMMSS.stderr.log`
- Evidencia de tests: [`4.2/P1/test_logs/`](./P1/test_logs/)

### P2 - Converter
- Código: [`4.2/P2/source/convertNumbers.py`](./P2/source/convertNumbers.py)
- Datos de entrada: [`4.2/P2/data/`](./P2/data/)
- Resultados finales: [`4.2/P2/results/ConvertionResults.txt`](./P2/results/ConvertionResults.txt)
- Resultados por caso:
  - [`TC1.Results.txt`](./P2/results/TC1.Results.txt), [`TC2.Results.txt`](./P2/results/TC2.Results.txt), [`TC3.Results.txt`](./P2/results/TC3.Results.txt), [`TC4.Results.txt`](./P2/results/TC4.Results.txt)
- Logs de ejecución (por TC): [`4.2/P2/logs/`](./P2/logs/)
- Evidencia de tests: [`4.2/P2/test_logs/`](./P2/test_logs/)

### P3 - Word Count
- Código: [`4.2/P3/source/wordCount.py`](./P3/source/wordCount.py)
- Datos de entrada: [`4.2/P3/data/`](./P3/data/)
- Resultados finales: [`4.2/P3/results/WordCountResults.txt`](./P3/results/WordCountResults.txt)
- Resultados por caso:
  - [`TC1.Results.txt`](./P3/results/TC1.Results.txt), [`TC2.Results.txt`](./P3/results/TC2.Results.txt), [`TC3.Results.txt`](./P3/results/TC3.Results.txt), [`TC4.Results.txt`](./P3/results/TC4.Results.txt), [`TC5.Results.txt`](./P3/results/TC5.Results.txt)
- Logs de ejecución (por TC): [`4.2/P3/logs/`](./P3/logs/)
- Evidencia de tests: [`4.2/P3/test_logs/`](./P3/test_logs/)

---

## Resumen de ejecución

### P1 (Statistics)
- Ejecutar todos los casos (`TC1` a `TC7`) desde la raíz:
  - `make run-p1-all`
- Evidencia final:
  - [`4.2/P1/results/StatisticsResults.txt`](./P1/results/StatisticsResults.txt)
- Logs:
  - [`4.2/P1/logs/`](./P1/logs/)
- Tests con log:
  - `make test-p1-log`
  - Evidencia: [`4.2/P1/test_logs/`](./P1/test_logs/)

### P2 (Converter)
- Ejecutar todos los casos (`TC1` a `TC4`) desde la raíz:
  - `make run-p2-all`
- Evidencia final:
  - [`4.2/P2/results/ConvertionResults.txt`](./P2/results/ConvertionResults.txt)
- Evidencia por caso:
  - [`4.2/P2/results/`](./P2/results/)
- Logs:
  - [`4.2/P2/logs/`](./P2/logs/)
- Tests con log:
  - `make test-p2-log`
  - Evidencia: [`4.2/P2/test_logs/`](./P2/test_logs/)

### P3 (Word Count)
- Ejecutar todos los casos (`TC1` a `TC5`) desde la raíz:
  - `make run-p3-all`
- Evidencia final:
  - [`4.2/P3/results/WordCountResults.txt`](./P3/results/WordCountResults.txt)
- Evidencia por caso:
  - [`4.2/P3/results/`](./P3/results/)
- Logs:
  - [`4.2/P3/logs/`](./P3/logs/)
- Tests con log:
  - `make test-p3-log`
  - Evidencia: [`4.2/P3/test_logs/`](./P3/test_logs/)