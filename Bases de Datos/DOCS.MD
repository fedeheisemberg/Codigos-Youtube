# Sistema de Registro de Datos de Opciones GGAL

## Descripción General

Sistema automatizado para capturar, almacenar y analizar datos en tiempo real de opciones financieras del activo GGAL (Grupo Financiero Galicia) desde HomeBroker. El sistema se conecta automáticamente durante el horario de trading y registra todas las cotizaciones en una base de datos SQLite.

## Características Principales

- **Conexión automática** durante horario de mercado (11:00 - 17:00, lunes a viernes)
- **Captura en tiempo real** de cotizaciones de opciones
- **Almacenamiento persistente** en base de datos SQLite
- **Generación de informes diarios** automáticos
- **Análisis de símbolos** para extraer vencimiento, strike y tipo de opción

## Requisitos

### Dependencias de Python

```python
pandas
sqlite3
datetime
schedule
pyhomebroker
sqlalchemy
json
```

### Archivo de Configuración

Crear un archivo `config.json` en el directorio raíz con el siguiente formato:

```json
{
  "broker": "123",
  "dni": "12345678",
  "usuario": "tu_usuario",
  "contrasena": "tu_contraseña"
}
```

## Estructura de la Base de Datos

### Tabla: `opciones_ggal`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | Integer | Clave primaria autoincremental |
| `simbolo` | String | Símbolo de la opción (ej: GFGC3500FE) |
| `vencimiento` | String | Mes de vencimiento (FE, AB, JU, AG, OC, DI) |
| `tipo_opcion` | String | Call o Put |
| `strike` | Float | Precio de ejercicio |
| `tamano_bid` | Integer | Tamaño de la oferta de compra |
| `bid` | Float | Precio de oferta de compra |
| `ask` | Float | Precio de oferta de venta |
| `tamano_ask` | Integer | Tamaño de la oferta de venta |
| `ultimo` | Float | Último precio operado |
| `cambio` | Float | Cambio porcentual |
| `apertura` | Float | Precio de apertura |
| `maximo` | Float | Precio máximo del día |
| `minimo` | Float | Precio mínimo del día |
| `cierre_previo` | Float | Precio de cierre anterior |
| `monto_operado` | Float | Monto total operado |
| `volumen` | Integer | Volumen de contratos |
| `operaciones` | Integer | Cantidad de operaciones |
| `fecha_hora` | DateTime | Fecha y hora de la cotización |
| `timestamp` | DateTime | Timestamp de inserción en BD |

## Funciones Principales

### `analizar_simbolo_opcion(simbolo)`

Extrae información del símbolo de la opción.

**Parámetros:**
- `simbolo` (str): Símbolo de la opción (formato: GFG[C/P]STRIKEXX)

**Retorna:**
- `vencimiento` (str): Código del mes de vencimiento
- `strike` (float): Precio de ejercicio
- `tipo_opcion` (str): "Call" o "Put"

**Ejemplo:**
```python
vencimiento, strike, tipo = analizar_simbolo_opcion('GFGC3500FE')
# Retorna: ('FE', 35.00, 'Call')
```

### `en_opciones(online, cotizaciones)`

Callback ejecutado al recibir datos de opciones desde HomeBroker.

**Funcionalidad:**
1. Filtra opciones de GGAL (prefijo GFG)
2. Calcula el cambio porcentual
3. Extrae vencimiento, strike y tipo de opción
4. Actualiza el DataFrame global
5. Guarda en la base de datos

### `guardar_en_base_datos(datos)`

Almacena las cotizaciones en la base de datos SQLite.

**Parámetros:**
- `datos` (DataFrame): DataFrame con las cotizaciones a guardar

**Manejo de errores:**
- Implementa rollback automático en caso de error
- Cierra la sesión siempre (finally)

### `conectar_homebroker()`

Establece conexión con HomeBroker y suscribe a datos de opciones.

**Proceso:**
1. Verifica si ya está conectado
2. Crea instancia de HomeBroker
3. Realiza autenticación con credenciales
4. Se conecta online
5. Suscribe a datos de opciones

### `desconectar_homebroker()`

Cierra la conexión con HomeBroker de forma segura.

### `es_horario_trading()`

Verifica si el momento actual está dentro del horario de trading.

**Retorna:**
- `True`: Si es día hábil (L-V) entre 11:00 y 17:00
- `False`: Fuera del horario de mercado

### `verificar_y_conectar()`

Gestiona automáticamente la conexión según el horario.

**Lógica:**
- Conecta si es horario de trading y no está conectado
- Desconecta si está fuera de horario y sigue conectado

### `generar_informe_diario()`

Genera un informe resumido de la actividad del día.

**Contenido del informe:**
- Total de símbolos registrados
- Total de puntos de datos capturados
- Período de tiempo cubierto
- Top 5 opciones más activas con:
  - Cantidad de registros
  - Rango de precios (mín-máx)
  - Precio de cierre

**Salida:**
- Imprime en consola
- Guarda archivo `informe_opciones_YYYY-MM-DD.txt`

## Programación de Tareas

El sistema utiliza la librería `schedule` para automatizar tareas:

```python
# Verifica conexión cada 2 segundos
schedule.every(2).seconds.do(verificar_y_conectar)

# Genera informe diario a las 17:05
schedule.every().day.at("17:05").do(generar_informe_diario)
```

## Uso

### Inicio del Sistema

```bash
python nombre_del_script.py
```

### Salida de Ejemplo

```
Iniciando Sistema de Registro de Base de Datos para Opciones GGAL
Archivo de base de datos: /ruta/completa/opciones_ggal.db
Base de datos existente encontrada con 15420 registros
Conectando a HomeBroker...
Conexión exitosa a HomeBroker
2025-10-29 11:15:30 - Guardados 45 registros de opciones GGAL
```

### Detener el Sistema

Presionar `Ctrl+C` para detener el sistema de forma segura. El sistema desconectará automáticamente de HomeBroker.

## Análisis de Símbolos

El sistema reconoce el siguiente formato de símbolos:

**Estructura:** `GFG[C/P][STRIKE][VENCIMIENTO]`

- `GFG`: Prefijo para opciones de GGAL
- `C/P`: Call o Put
- `STRIKE`: Precio de ejercicio en centavos (ej: 3500 = $35.00)
- `VENCIMIENTO`: Código de dos letras (FE=Febrero, AB=Abril, etc.)

**Ejemplos:**
- `GFGC3500FE`: Call strike $35.00 vencimiento Febrero
- `GFGP4000JU`: Put strike $40.00 vencimiento Junio

## Manejo de Errores

El sistema implementa múltiples niveles de manejo de errores:

1. **Carga de configuración**: Verifica existencia y validez de `config.json`
2. **Conexión a HomeBroker**: Captura excepciones y reporta errores
3. **Base de datos**: Implementa rollback en transacciones fallidas
4. **Callback de error**: Función `en_error()` para errores del broker

## Consultas SQL Útiles

### Obtener todos los registros de un símbolo específico

```sql
SELECT * FROM opciones_ggal 
WHERE simbolo = 'GFGC3500FE' 
ORDER BY fecha_hora DESC;
```

### Resumen diario por tipo de opción

```sql
SELECT 
    tipo_opcion,
    COUNT(*) as total_registros,
    AVG(ultimo) as precio_promedio
FROM opciones_ggal 
WHERE date(fecha_hora) = '2025-10-29'
GROUP BY tipo_opcion;
```

### Opciones más volátiles del día

```sql
SELECT 
    simbolo,
    MAX(ultimo) - MIN(ultimo) as rango,
    COUNT(*) as registros
FROM opciones_ggal 
WHERE date(fecha_hora) = date('now')
GROUP BY simbolo
ORDER BY rango DESC
LIMIT 10;
```

## Consideraciones Importantes

1. **Horario de Trading**: El sistema solo opera de 11:00 a 17:00, lunes a viernes
2. **Credenciales**: Nunca compartir el archivo `config.json`
3. **Espacio en disco**: La base de datos crece continuamente, monitorear espacio
4. **Red**: Requiere conexión estable a internet
5. **Performance**: Verifica cada 2 segundos, puede ajustarse según necesidad

## Troubleshooting

### Error: "No se pudo cargar el archivo config.json"
**Solución:** Crear archivo `config.json` con las credenciales correctas

### Error: "Error al conectar a HomeBroker"
**Solución:** Verificar credenciales y conexión a internet

### Base de datos bloqueada
**Solución:** Asegurarse de que solo una instancia del script esté corriendo

### No se guardan datos
**Solución:** Verificar que sea horario de trading y que la conexión esté activa

## Mejoras Futuras Sugeridas

- Implementar respaldo automático de la base de datos
- Agregar notificaciones por email/SMS en eventos importantes
- Dashboard web para visualización en tiempo real
- Análisis de volatilidad implícita
- Exportación a CSV/Excel
- Integración con sistemas de trading algorítmico

## Licencia y Disclaimer

Este sistema es para uso educativo y análisis personal. El trading de opciones implica riesgos significativos. Siempre consultar con un asesor financiero antes de tomar decisiones de inversión.