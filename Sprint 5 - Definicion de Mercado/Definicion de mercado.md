# Definición de mercado: TAM, SAM y SOM

**Proyecto:** CrediStep
**Asignatura:** Gestión de Innovación en TI, Pontificia Universidad Javeriana
**Sprint 5:** Análisis del mercado
**Integrantes:** Beike Romario Jaramillo Giraldo, Laura Sofía Ortiz Gómez, Sarahy Michelle Silva Pinto, Valentina Carrillo Peñuela, Miguel Ángel Gómez López
**Bogotá, D.C., octubre de 2026**

---

## 1. Introducción

CrediStep es una herramienta pensada para jóvenes colombianos de 18 a 25 años que apenas están empezando su vida crediticia. Lo que buscamos es explicarles de forma sencilla cómo se construye un historial crediticio, cómo funciona el puntaje y cómo usar bien el cupo y sus primeros productos de crédito.

En el Sprint anterior validamos el problema con una encuesta a 126 jóvenes. Los resultados que más nos sirven para este análisis fueron:

- El 54 % se sentiría inseguro al tomar su primer crédito sin recibir orientación.
- El 35,7 % ya evitó pedir un crédito por no saber cómo funcionaba.
- El 40,5 % se ubicó en los niveles más bajos de preparación para tomar decisiones de crédito.
- El 85,7 % dijo tener un interés alto o muy alto en una herramienta que le explique cómo iniciar y manejar su vida crediticia.

En este documento calculamos qué tan grande es la oportunidad de mercado de CrediStep usando el modelo TAM-SAM-SOM. Explicamos de dónde sale cada número y dejamos claro cuáles son datos con fuente y cuáles son supuestos nuestros. Este análisis nos sirve de base para el segundo pitch y para las proyecciones financieras.

## 2. Metodología

### 2.1. Qué es cada sigla

| Sigla | Nombre | Qué significa para CrediStep |
|---|---|---|
| **TAM** | Mercado total | Todos los jóvenes de 18 a 25 años en Colombia que podrían necesitar la herramienta. |
| **SAM** | Mercado atendible | La parte del TAM que sí podemos atender con nuestro modelo de negocio y los canales con los que vamos a empezar. |
| **SOM** | Mercado alcanzable | La parte del SAM que de forma realista podemos conseguir durante el primer año. |

### 2.2. Cómo lo calculamos

- **TAM y SAM:** usamos un enfoque *top-down*. Partimos de la población total de jóvenes de 18 a 25 años y le aplicamos filtros uno tras otro (ciudad, acceso a tecnología y necesidad).
- **SOM:** usamos un enfoque *bottom-up*. Partimos de un canal concreto, la Universidad Javeriana, y estimamos cuántos estudiantes se registrarían y cuántos pagarían.

### 2.3. Unidades

Trabajamos con **usuarios** y con **pesos colombianos (COP) por año**. Los ingresos anuales los calculamos así:

```
Ingresos anuales = Usuarios × ARPU anual
```

El ARPU es lo que paga en promedio cada usuario al año.

## 3. Supuestos generales

| Supuesto | Valor | Fuente o justificación |
|---|---|---|
| Edad del público objetivo | 18 a 25 años | Es el rango que definimos en el supuesto inicial y que validamos en la encuesta. |
| Población de 18 a 25 años en Colombia | 5,8 millones | DANE. Proyecciones de población a nivel nacional y departamental 2020-2050. |
| Precio mensual | $20.000 COP | Suscripción "1 - Plus" de nuestro modelo de negocio. Precio validado en el modelo financiero del simulador para el servicio principal que asegura nuestro punto de equilibrio. |
| ARPU anual | $240.000 COP | $20.000 × 12 meses. |
| Ciudad inicial | Bogotá | Es nuestro entorno inmediato, facilita el piloto logístico y concentra el mayor ecosistema de estudiantes universitarios del país. |
| Filtro de necesidad | 41,3 % | Encuesta CrediStep (n = 126), pregunta 2: jóvenes que nunca han tenido un producto de crédito. |

> **Algo que notamos en la encuesta:** el porcentaje de jóvenes que nunca ha tenido crédito aparece con tres valores distintos en nuestro documento de validación: 41,3 % (pregunta 2), 42,1 % (pregunta 8) y 43,7 % (pregunta 3, opción "Ninguno"). Para este análisis usamos 41,3 % porque viene directamente de la pregunta 2, y usamos ese mismo valor en el diagrama y en el Excel.

## 4. TAM: mercado total

**Qué incluye.** Todos los jóvenes de 18 a 25 años en Colombia.

**Cálculo.**

```
TAM (usuarios) = 5.800.000
TAM (COP/año)  = 5.800.000 × $240.000 = $1.392.000.000.000
```

| Concepto | Valor |
|---|---|
| Usuarios | 5,8 millones |
| Ingresos potenciales por año | $1,392 billones COP |

**Por qué este segmento.** Los datos del contexto muestran que es un grupo con poco acceso al crédito. Según el reporte de inclusión financiera 2023 de la Banca de las Oportunidades, solo el 22,3 % de los adultos entre 18 y 25 años accedió a algún producto de crédito. Además, cerca del 32 % de los adultos en Colombia no tenía historial crediticio tradicional al cierre del segundo trimestre de 2026 (TransUnion), y los menores de 28 años concentran el 51 % de las primeras operaciones de crédito (DataCrédito Experian, 2024). Es decir, el momento en que se necesita orientación llega temprano.

**Limitación.** El TAM en pesos es un techo teórico, porque supone que todos los jóvenes del país pagarían la suscripción completa, y eso no va a pasar. Lo usamos para dimensionar la oportunidad, no para proyectar ingresos.

## 5. SAM: mercado atendible

**Qué incluye.** Los jóvenes de 18 a 25 años que sí podemos atender con lo que tenemos planeado: que vivan en la ciudad donde vamos a empezar, que tengan smartphone e internet (porque CrediStep es digital) y que de verdad necesiten orientación.

**Cálculo.**

| Paso | Filtro | Porcentaje | Usuarios que quedan | Fuente |
|---|---|---|---|---|
| 0 | TAM | 100 % | 5.800.000 | DANE |
| 1 | Viven en Bogotá | ~18,9 % | 1.100.000 | Proyecciones de población DANE. |
| 2 | Tienen smartphone e internet | 84,1 % | 925.100 | MinTIC / Encuesta TIC DANE. |
| 3 | Tienen la necesidad (nunca han tenido crédito) | 41,3 % | **381.667** | Encuesta CrediStep (n = 126) |

```
SAM (usuarios) = 5.800.000 × %Bogotá × %conectividad × 41,3 % = 381.667
SAM (COP/año)  = 381.667 × $240.000 = $91.600.080.000
```
| Concepto | Valor |
|---|---|
| Usuarios | 381.667 |
| Ingresos potenciales por año | $91.600 millones COP |

**Por qué cada filtro.**

- **Ciudad inicial:** Elegimos Bogotá por viabilidad operativa del equipo. Si el piloto es exitoso, planeamos expandirnos a ciudades principales como Medellín y Cali.
- **Smartphone e internet:** sin acceso a la tecnología, una persona no puede usar CrediStep.
- **Necesidad:** aplicamos el porcentaje de quienes nunca han tenido un producto de crédito, porque son los que más necesitan aprender cómo empezar un historial.

**Limitación.** Sacamos el filtro de necesidad de una muestra de solo 126 personas, concentrada en jóvenes de 18 a 20 años y seguramente en estudiantes universitarios. Por eso lo tomamos como una aproximación y no como un dato exacto de todo el país.

## 6. SOM: mercado alcanzable

**Qué incluye.** Los usuarios que realmente podemos conseguir y convertir en clientes de pago durante el primer año, con los recursos que tenemos.

**Canal.** Elegimos la Universidad Javeriana como piloto del año 1. Al ser estudiantes de la Pontificia Universidad Javeriana, tenemos acceso directo a los canales de comunicación institucionales y orgánicos, reduciendo los costos de adquisición de clientes.

**Cálculo (bottom-up).**

| Paso | Variable | Valor | Fuente |
|---|---|---|---|
| 1 | Estudiantes de pregrado de la Javeriana | 21.900 | Cifras institucionales oficiales de la Pontificia Universidad Javeriana, Sede Bogotá. |
| 2 | Estudiantes que se registran | 10 % | Supuesto nuestro. Supuesto base optimista alineado a los estándares de adopción inicial para modelos de startups tecnológicas en entornos universitarios. |
| 3 | Registrados que pagan | 20 % | Supuesto nuestro. Tasa de conversión de freemium a pago estándar en la industria SaaS, la cual requerimos para alcanzar el punto de equilibrio según nuestro simulador financiero. |

```
SOM (usuarios) = 21.900 × 10 % × 20 % = 438
SOM (COP/año)  = 438 × $240.000 = $105.120.000
```

| Concepto | Valor |
|---|---|
| Usuarios de pago | 438 |
| Ingresos por año | $105 millones COP |

**Por qué estos números.** En la encuesta, el 85,7 % mostró un interés alto o muy alto, lo que nos dice que hay demanda. Sin embargo, que alguien diga que le interesa no es lo mismo que alguien que paga, así que las tasas de registro y de pago son **supuestos** que tenemos que comprobar con el piloto.

### 6.1. Qué pasa si las tasas son más bajas

Como el 10 % y el 20 % son supuestos, armamos otros escenarios para ver cómo cambia el resultado. Los escenarios intermedio y conservador son propuestas nuestras, no datos de una fuente.

| Escenario | Registro | Pago | Usuarios de pago | Ingresos por año (COP) |
|---|---|---|---|---|
| Base (el del diagrama) | 10 % | 20 % | 438 | $105.120.000 |
| Intermedio | 10 % | 10 % | 219 | $52.560.000 |
| Conservador | 5 % | 5 % | 55 (54,75) | ≈ $13.140.000 |

Nos quedamos con el Escenario Base (10% y 20%) porque ya está alineado con el diagrama y es el que sustenta los $105 millones COP requeridos en nuestra evaluación financiera.

## 7. Diagrama TAM-SAM-SOM


<img width="1599" height="899" alt="image" src="https://github.com/user-attachments/assets/380635ca-6cf7-4625-82bb-be1064b0caee" />


*Figura 1. Mercado de CrediStep: TAM, SAM y SOM. Fuentes: DANE, encuesta CrediStep (n = 126) y cifras institucionales de la Universidad Javeriana.*

En el diagrama se ve cómo cada nivel está dentro del anterior: el SOM es una parte del SAM, y el SAM es una parte del TAM. Los valores de cada nivel son:

| Nivel | Usuarios | Ingresos potenciales por año (COP) |
|---|---|---|
| TAM | 5.800.000 | $1,392 billones |
| SAM | 381.667 | $91.600.080.000 |
| SOM | 438 | $105.120.000 |

## 8. Limitaciones y riesgos

- **No hemos validado el precio con usuarios.** El ARPU de $240.000 al año sale de nuestro modelo de negocio, pero en la encuesta preguntamos por interés, no por cuánto estarían dispuestos a pagar.
- **Las tasas de registro y de pago no tienen fuente externa.** Un 20 % de pago entre los registrados es alto comparado con lo que suele pasar en modelos freemium, así que conviene contrastarlo con referencias o con los resultados del piloto.
- **Sesgo de la muestra.** La encuesta se concentró en jóvenes de 18 a 20 años, probablemente estudiantes universitarios. Representa bien al canal de la universidad (SOM), pero hay que tener cuidado al extrapolarla al SAM.
- **El filtro de necesidad cambia según la pregunta.** El porcentaje de jóvenes sin crédito varía entre 41,3 % y 43,7 %. Usamos 41,3 % y dejamos documentada la decisión.
- **El SOM depende de una sola universidad.** Si el piloto funciona, el siguiente paso sería sumar otras universidades, lo que ampliaría el SOM con la misma lógica de cálculo.

## 9. Conclusiones

1. El mercado total de jóvenes de 18 a 25 años en Colombia es de 5,8 millones de personas, lo que equivale a un potencial teórico de $1,392 billones COP al año.
2. Si tenemos en cuenta la ciudad inicial, el acceso a tecnología y la necesidad real de orientación, el mercado que podemos atender es de 381.667 usuarios, equivalente a $91.600 millones COP al año.
3. En el primer año, con la Universidad Javeriana como canal piloto, estimamos 438 usuarios de pago y $105 millones COP, bajo el escenario base.
4. Lo más incierto de nuestro análisis son las tasas de registro y de pago. El piloto en la Javeriana nos va a servir para medirlas y ajustar las proyecciones.
5. Estos resultados los vamos a usar en el segundo pitch y en el análisis financiero.

## 10. Referencias

1. Llanes, M. C. (2024, 17 de junio). *Colombia: inclusión financiera casi universal, pero con retos en inclusión crediticia.* BBVA Research.
2. Alguero, M. O. (2024, 9 de agosto). *Jóvenes: ¿cómo sacar su primer crédito y no morir en el intento?* El Colombiano.
3. La República. (2026, 8 de septiembre). *Informe de TransUnión reveló que 32 % de las personas no cuentan con historial crediticio.*
4. La República. (2025, 12 de noviembre). *Jóvenes entre 18 y 30 años representan 20 % de los préstamos tradicionales en la banca.*
5. DANE. Proyecciones de población a nivel nacional, departamental y municipal 2020-2050. Proyecciones de población (18 a 25 años y por ciudad).
6. MinTIC / DANE. Indicadores básicos de tenencia y uso de tecnologías de la información y comunicación – TIC. Fuente de conectividad: DANE o MinTIC.
7. Pontificia Universidad Javeriana. Cifras institucionales - Estudiantes matriculados en pregrado Sede Bogotá. Cifras institucionales de estudiantes de pregrado.
8. Equipo CrediStep. (2026, 5 de octubre). *Artefactos de validación: Proyecto CrediStep.* Pontificia Universidad Javeriana.
