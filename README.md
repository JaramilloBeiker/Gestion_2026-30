# CrediStep

> *Construye hoy el historial que necesitarás mañana.*

CrediStep es un GPS financiero para personas de 18 a 49 años en Colombia que empiezan o fortalecen su historial de crédito: les hace un diagnóstico, les traza una ruta de pasos, les enseña con lecciones cortas y simuladores, y les muestra su progreso antes de pedir su primer crédito. No recomienda bancos ni productos: enseña cómo avanzar.

Proyecto de la asignatura **Gestión de Innovación en TI**, Pontificia Universidad Javeriana, 2026-30. Se trabajó con Scrum en 10 sprints, del 16/07/2026 al 25/11/2026.

Este repositorio reúne todos los entregables del proyecto (documentos, pitches, hojas financieras) y el código del MVP.

## Contenido

- [Equipo](#equipo)
- [Estructura del repositorio](#estructura-del-repositorio)
- [Cómo leer los archivos de cada carpeta](#cómo-leer-los-archivos-de-cada-carpeta)
- [Cifras clave](#cifras-clave)
- [Ejecutar el MVP](#ejecutar-el-mvp)
- [Próximos pasos](#próximos-pasos)

## Equipo

| Integrante | Rol |
|---|---|
| Beiker Romario Jaramillo Giraldo | Scrum Master |
| Laura Sofía Ortiz Gómez | Desarrolladora full-stack |
| Sarahy Michelle Silva Pinto | Diseñadora UX/UI |
| Valentina Carrillo Peñuela | Ingeniera de QA |
| Miguel Ángel Gómez López | Investigación y validación |

Product Owner: Víctor Hugo Vela Pinzón (profesor).

## Estructura del repositorio

```
Gestion_2026-30/
├── README.md                          Este archivo
├── Plan de Negocios/                  Plan de negocios (V1, V2 y final)
├── Informacion Adicional/             Documento Scrum del proyecto completo (sprints 1 a 10)
├── Sprint 1 - Contextualizacion del problema/
├── Sprint 2 - Primer Pitch/
├── Sprint 3 - Artefactos de Validacion/
├── Sprint 4 - Lienzo Canvas/
├── Sprint 5 - Definicion de Mercado/
├── Sprint 6 - Prototipado a Mano/
├── Sprint 7 - Contexto Financiero/
├── Sprint 8 - Segundo Pitch/
├── Sprint 9 - Mockups/
├── Sprint 10 - Pitch_Final/
└── CrediStep-App/                     Código del MVP (FastAPI + Vue)
```

### Sprints

| # | Carpeta | Fechas | Entregable principal |
|---|---|---|---|
| 1 | `Sprint 1 - Contextualizacion del problema/` | 16/07 – 30/07 | Contextualización del problema con fuentes oficiales |
| 2 | `Sprint 2 - Primer Pitch/` | 03/08 – 31/08 | Diapositivas y guion del primer pitch |
| 3 | `Sprint 3 - Artefactos de Validacion/` | 01/09 – 21/09 | Encuesta a 126 jóvenes y análisis de resultados |
| 4 | `Sprint 4 - Lienzo Canvas/` | 22/09 – 05/10 | Lienzo Canvas del modelo de negocio |
| 5 | `Sprint 5 - Definicion de Mercado/` | 06/10 – 12/10 | Definición de mercado (TAM, SAM, SOM): versión 1 y versión 2.0 (18 a 49 años, la vigente) |
| 6 | `Sprint 6 - Prototipado a Mano/` | 13/10 – 19/10 | Prototipos a mano, wireframes y taller práctico |
| 7 | `Sprint 7 - Contexto Financiero/` | 20/10 – 26/10 | Contexto financiero, diagrama TAM-SAM-SOM y proyección financiera (Excel) |
| 8 | `Sprint 8 - Segundo Pitch/` | 27/10 – 02/11 | Deck y guion del segundo pitch |
| 9 | `Sprint 9 - Mockups/` | 03/11 – 16/11 | Documento "Cómo funciona la aplicación" (MVP y mockups) |
| 10 | `Sprint 10 - Pitch_Final/` | 17/11 – 25/11 | Deck del pitch final y guion en inglés |

Cada carpeta de sprint incluye su `Documento_Scrum_Sprint_N` (`.tex` y `.pdf`) con objetivo, historias de usuario, tareas, métricas, revisión y retrospectiva. El documento que consolida los diez sprints está en `Informacion Adicional/`.

### Otras carpetas

| Carpeta | Contenido |
|---|---|
| `Plan de Negocios/` | Plan de negocios (`Plan_de_Negocios_CrediStep`, `V2Plan_de_Negocios_CrediStep` y `Final_Plan_de_Negocios_CrediStep`), con las cifras referenciadas |
| `Informacion Adicional/` | `Documento_Scrum_Proyecto` (consolidado de los 10 sprints) en versión inicial, V2 y final |
| `CrediStep-App/` | Backend (`backend/`), frontend (`frontend/`), scripts de arranque y la guía técnica de la app, [`DOCUMENTACION_APP.md`](CrediStep-App/DOCUMENTACION_APP.md) |

## Cómo leer los archivos de cada carpeta

Los documentos se guardaron por versiones:

| Nombre | Significado |
|---|---|
| `Nombre.pdf` / `Nombre.tex` | Primera versión del documento |
| `V2Nombre.pdf` | Segunda versión, después de la revisión |
| `Final_Nombre.pdf` | Versión final entregada (la que debe leerse) |
| `Nombre (1).pdf`, `Nombre (3).xlsx` | Copias descargadas. Pueden ser versiones distintas: en el Sprint 5, `Definicion_de_mercado_V2 (1).pdf` es la versión 2.0 vigente |

Los `.tex` son el código fuente en LaTeX de los PDF.

## Cifras clave

| Indicador | Valor |
|---|---|
| Jóvenes de 18 a 25 años con crédito formal | 19,4 % (Reporte de Inclusión Financiera 2025) |
| Encuesta de validación | 126 jóvenes; 54 % se sentiría inseguro sin orientación; 85,7 % quiere una herramienta de orientación |
| Mercado total (TAM) | 25.607.240 personas de 18 a 49 años (6,15 billones de COP al año) |
| Mercado atendible (SAM) | 8.482.872 usuarios urbanos, con acceso digital, con capacidad de pago y sin crédito formal (2,04 billones de COP al año) |
| Registrados en el año 1 | 44.196 (42.414 por canal digital y 1.782 de la Javeriana) |
| Suscriptores de pago en el año 1 (SOM) | 891, unos $213,8 millones |
| Supuestos del SOM | Alcance digital de 0,5 % del SAM y conversión a pago de 2,1 % |
| Precio de CrediStep Plus | $20.000 al mes ($240.000 al año por suscriptor) |
| Inversión inicial | $5 millones, aportados por el equipo |
| Punto de equilibrio del año 1 | 440 suscriptores ($105,6 millones de costos entre $240.000) |

La fuente de las cifras de mercado es `Definicion_de_mercado_V2 (1).pdf` en la carpeta del [Sprint 5](Sprint%205%20-%20Definicion%20de%20Mercado/), versión 2.0 de noviembre de 2026. El alcance digital de 0,5 % es un supuesto del equipo que debe validarse en el piloto. La inversión inicial y el punto de equilibrio vienen de la hoja financiera del [Sprint 7](Sprint%207%20-%20Contexto%20Financiero/).

**Documentos con cifras anteriores.** El plan de negocios final, el contexto financiero final y la hoja de proyección del Sprint 7 todavía usan la versión anterior del mercado (11.580.726 personas de 18 a 30 años de TAM, 4.182.110 de SAM y 439 suscriptores). La versión 2.0 pide actualizar la hoja financiera con 891 suscriptores. Además, el Sprint 1 cita un dato más antiguo de acceso a crédito (22 %); el valor vigente es 19,4 %.

## Ejecutar el MVP

Requisito: Python 3.11 o superior.

- **Windows:** doble clic en `CrediStep-App/iniciar.bat`
- **macOS o Linux:** `bash CrediStep-App/iniciar.sh`

Luego abre <http://localhost:8000>. Las cuentas de demostración, las funcionalidades y la arquitectura están en [`CrediStep-App/DOCUMENTACION_APP.md`](CrediStep-App/DOCUMENTACION_APP.md).

Límites actuales del MVP: corre en un computador local, el plan Plus se activa en modo demostración (sin pasarela de pagos) y todavía no se ha probado con usuarios reales.

## Próximos pasos

Piloto con la Javeriana, pruebas con usuarios reales, definición del precio de la licencia institucional, pasarela de pagos, despliegue en la nube y versión móvil.

---
Gestión de Innovación en TI · Pontificia Universidad Javeriana · 2026
