# CrediStep — Documentación de la aplicación (MVP)

> *Construye hoy el historial que necesitarás mañana.*

CrediStep es un **GPS financiero para personas de 18 a 49 años**: hace un diagnóstico de su situación, propone una
ruta personalizada, los acompaña con educación aplicada, metas y recordatorios, y les muestra su progreso.
**No les decimos qué comprar; les enseñamos cómo avanzar.**

Esta guía es la documentación técnica de la carpeta `CrediStep-App/`. La visión general del repositorio está en el
[README de la raíz](../README.md).

## Cómo ejecutarla

Requisito: **Python 3.11 o superior** (no hace falta Node.js ni internet después de instalar).

- **Windows:** doble clic en `iniciar.bat`
- **macOS / Linux:** `bash iniciar.sh`

Abre <http://localhost:8000>. La documentación interactiva de la API está en <http://localhost:8000/docs>.

| Cuenta demo | Correo | Contraseña |
|---|---|---|
| Estudiante (con progreso) | `demo@credistep.co` | `CrediStep2026` |
| Universidad (panel B2B) | `admin@javeriana.edu.co` | `CrediStep2026` |
| Código institucional para registrarse | `JAVERIANA2026` | — |

Para reiniciar los datos, borra `backend/credistep.db` y vuelve a iniciar.

## El MVP en cifras

| Elemento | Cantidad |
|---|---|
| Preguntas del diagnóstico | 7 |
| Pasos de la ruta personalizada | 5 |
| Módulos educativos | 4 |
| Lecciones | 12 |
| Preguntas de quiz | 17 |
| Simuladores | 4 (uso de cupo, costo de crédito, pagos atrasados, puntaje) |
| Términos del glosario | 18 |
| Preguntas frecuentes | 12 |
| Pruebas automáticas (pytest) | 22 |
| Plan gratuito: metas de ahorro | hasta 2 |
| CrediStep Plus | $20.000 al mes o $200.000 al año |

## Funcionalidades y de dónde salen

| Funcionalidad | Origen en el proyecto |
|---|---|
| Inicio de sesión / registro | Prototipo, Pantalla 1 |
| Diagnóstico de 7 preguntas con puntaje, nivel, fortalezas y mejoras | Prototipo, Pantallas 2 y 3 · Encuesta de validación |
| Ruta de 5 pasos personalizada (cambia si el usuario ya tiene crédito), próximo objetivo y tareas que se completan solas | Pitch 1 (“Paso 1…5”) · Prototipo, Pantalla 4 |
| Acción recomendada con checklist “antes de hacerlo” (sin marcas ni productos específicos) | Prototipo, Pantalla 5 · “No te decimos qué comprar” |
| 4 módulos educativos con 12 lecciones y quiz | Artefacto de validación, Cuadro 2 (módulos del MVP) |
| Simuladores: uso de cupo, costo de crédito, pagos atrasados, puntaje | Dudas más frecuentes de la encuesta (puntaje, cupo, atrasos) |
| Metas de ahorro y recordatorios recurrentes | Canvas: fidelización con recordatorios |
| Índice de preparación crediticia, XP, niveles y racha | Canvas: “indicador de progreso” |
| Asistente **Step** y glosario | Canvas: asistencia personal y autoservicio |
| **CrediStep Plus** con funciones bloqueadas en el plan gratuito | Modelo de negocio · Definición de mercado |
| Licencias institucionales y **panel de la universidad** solo con datos agregados | Canvas: licencias · Pitch 2: piloto en la Javeriana |

## Arquitectura

```
CrediStep-App/
├── iniciar.bat / iniciar.sh   Crean el entorno, instalan dependencias y arrancan el servidor
├── backend/                   FastAPI + SQLModel + SQLite + JWT
│   ├── app/
│   │   ├── main.py            API (/api) y servidor del frontend
│   │   ├── config.py          Configuración (precios, límites, token)
│   │   ├── models.py          Tablas
│   │   ├── content.py         Módulos, lecciones, ruta, glosario y FAQ
│   │   ├── seed.py            Datos de demostración
│   │   ├── services/          Diagnóstico, progreso, simuladores, asistente
│   │   └── routers/           auth, diagnostic, plan, learning, goals, reminders, tools, dashboard
│   └── tests/                 22 pruebas (pytest)
└── frontend/                  Vue 3 + Vue Router (módulos ES, sin paso de compilación)
    ├── css/styles.css         Sistema de diseño verde (claro / oscuro)
    ├── js/views/              Una vista por pantalla (15)
    └── vendor/ fonts/         Librerías y tipografía incluidas localmente
```

- **Seguridad:** contraseñas con PBKDF2-SHA256 y sesiones con tokens JWT (duran 72 horas por defecto).
- **Pruebas:** desde `backend/`, `.venv\Scripts\python -m pytest` (Windows) o `.venv/bin/python -m pytest` (macOS / Linux).
- **Pagos:** Plus se activa en **modo demostración** (no se cobra ni se piden datos de pago).
- Los simuladores son **educativos y aproximados**. El contenido legal se basa en la Ley 1266 de 2008 y la Ley 2157 de 2021.

## Próximos pasos sugeridos

Pasarela de pagos real, notificaciones push o por correo para los recordatorios, un asistente con modelo de lenguaje,
app móvil (el frontend ya es responsive) y migrar la base de datos a PostgreSQL al salir del entorno local.

---
Proyecto de Gestión de Innovación en TI · Pontificia Universidad Javeriana · 2026
