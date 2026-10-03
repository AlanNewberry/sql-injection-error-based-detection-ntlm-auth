# Deteccion de SQL Injection Error-Based con Autenticacion NTLM

## Descripcion

Hice este script para automatizar la deteccion de inyeccion SQL basada en errores en aplicaciones web .NET que usan autenticacion NTLM. Envia una lista de payloads clasicos de SQLi contra un parametro de busqueda y analiza las respuestas buscando keywords de error de base de datos (SQL Server, Oracle, MySQL, SQLite, PostgreSQL, ODBC).

## Como funciona

1. **Autenticacion NTLM**: Se autentica contra la aplicacion con credenciales de dominio
2. **Envio de payloads**: Prueba cada payload de SQLi contra el parametro configurado
3. **Deteccion de errores**: Busca keywords de error de base de datos en la respuesta
4. **Reporte**: Muestra el status code, tamanio de respuesta, payload usado y el snippet de error encontrado

## Payloads incluidos

```
test, ', '', test'--, test", 1) OR (1=1, test' OR '1'='1, %, *, test;--, test`
```

## Keywords de deteccion

```
sql, syntax, exception, stack, ora-, sqlite, postgres, mysql, odbc, invalid
```

## Requisitos

```bash
pip install requests requests-ntlm
```

## Uso

Configura las variables al inicio del script:

```python
TARGET = "https://TARGET_HOST"
DOMAIN = "DOMAIN"
USERNAME = "USERNAME"
PASSWORD = "PASSWORD"
ENDPOINT = "/Package"
PARAM = "search"
```

```bash
python3 sql-injection-error-based-detection-ntlm-auth.py
```

## Ejemplo de salida

```
[200] len= 15234 search='test'
[500] len=  3421 search="'"  ...SqlException: Unclosed quotation mark after the character string...
[200] len= 15234 search="''"
[500] len=  3518 search="test'--"  ...syntax error near 'test'...
```

## Interpretacion de resultados

- **500 con keyword SQL**: Confirmacion de SQLi — el payload llego a la query sin sanitizar
- **200 con tamanio diferente**: Posible SQLi boolean-based
- **200 con mismo tamanio**: El payload fue sanitizado o no afecta la query
- **403**: WAF o filtro de seguridad bloqueando el request

## Aviso legal

Este script es unicamente para pruebas de seguridad autorizadas y fines educativos. Siempre obtene la autorizacion correspondiente antes de testear contra cualquier sistema.

## Autor

**Alan Newberry**
