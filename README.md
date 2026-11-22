# CrediStep

> *Construye hoy el historial que necesitarás mañana.*

CrediStep es un GPS financiero para jóvenes colombianos de 18 a 30 años. Les hace un diagnóstico, les traza una ruta de pasos, les enseña con lecciones cortas y simuladores, y les muestra su progreso antes de pedir su primer crédito. No recomienda bancos ni productos: enseña cómo avanzar.

Proyecto de la asignatura **Gestión de Innovación en TI**, Pontificia Universidad Javeriana, 2026-30. Se trabajó con Scrum en 10 sprints, del 16/07/2026 al 25/11/2026.

## Objetivo del proyecto

Validar el problema, definir el modelo de negocio, calcular el mercado y construir un MVP funcional de CrediStep, y sustentar el proyecto en un pitch final ante los jurados.

## Equipo

| Integrante | Rol |
|---|---|
| Beiker Romario Jaramillo Giraldo | Scrum Master |
| Laura Sofía Ortiz Gómez | Desarrolladora full-stack |
| Sarahy Michelle Silva Pinto | Diseñadora UX/UI |
| Valentina Carrillo Peñuela | Ingeniera de QA |
| Miguel Ángel Gómez López | Investigación y validación |

Product Owner: Víctor Hugo Vela Pinzón (profesor).

## Cifras clave

| Indicador | Valor |
|---|---|
| Jóvenes de 18 a 25 años con crédito formal | 19,4 % |
| Encuesta de validación | 126 jóvenes; 54 % se sentiría inseguro sin orientación; 85,7 % quiere una herramienta de orientación |
| Mercado total (TAM) | 11.580.726 jóvenes de 18 a 30 años |
| Mercado atendible (SAM) | 4.182.110 |
| Suscriptores de pago en el año 1 (SOM) | 439, unos $105,4 millones |
| Inversión inicial | $5 millones |
| Punto de equilibrio del año 1 | 440 suscriptores |

Detalle y fuentes en el [plan de negocios](Plan%20de%20Negocios/) y en el [contexto financiero](Sprint%207%20-%20Contexto%20Financiero/).

## Estructura del repositorio

| Carpeta | Contenido |
|---|---|
| `Plan de Negocios/` | Plan de negocios inicial (`.tex` y `.pdf`), con todas las cifras referenciadas |
| `Informacion Adicional/` | Documento Scrum del proyecto completo, sprints 1 a 10 |
| `Sprint 1 - Contextualizacion del problema/` | Contextualización del problema con fuentes oficiales |
| `Sprint 2 - Primer Pitch/` | Diapositivas y guion del primer pitch |
| `Sprint 3 - Artefactos de Validacion/` | Encuesta a 126 jóvenes y análisis de resultados |
| `Sprint 4 - Lienzo Canvas/` | Lienzo Canvas del modelo de negocio |
| `Sprint 5 - Definicion de Mercado/` | Definición de mercado, versiones 1 y 2 (TAM, SAM, SOM) |
| `Sprint 6 - Prototipado a Mano/` | Prototipo a mano de cinco pantallas |
| `Sprint 7 - Contexto Financiero/` | Contexto financiero y hojas de proyección, versiones 1 y 2 |
| `Sprint 8 - Segundo Pitch/` | Diapositivas y guion del segundo pitch |
| `Sprint 9 - Mockups/` | Documentación de cómo funciona la aplicación |
| `Sprint 10 - Pitch_Final/` | Diapositivas y guion del pitch final |
| `CrediStep-App/` | Código del MVP web (FastAPI y Vue) |

Cada carpeta de sprint incluye su `Documento_Scrum_Sprint_N` (`.tex` y `.pdf`) con objetivo, historias de usuario, tareas, métricas, revisión y retrospectiva.

## Ejecutar el MVP

Requisito: Python 3.11 o superior.

- **Windows:** doble clic en `CrediStep-App/iniciar.bat`
- **macOS o Linux:** `bash CrediStep-App/iniciar.sh`

Luego abre <http://localhost:8000>. Las cuentas de demostración y la arquitectura están en [`CrediStep-App/README.md`](CrediStep-App/README.md).

Límites actuales del MVP: corre en un computador local, el plan Plus se activa en modo demostración (sin pasarela de pagos) y todavía no se ha probado con usuarios reales.

## Próximos pasos

Piloto con la Javeriana, pruebas con usuarios reales, definición del precio de la licencia institucional, pasarela de pagos, despliegue en la nube y versión móvil.

---
Gestión de Innovación en TI · Pontificia Universidad Javeriana · 2026
