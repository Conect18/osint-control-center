# OSINT Control Center

**Versión 1.3.0**

Laboratorio OSINT local desarrollado en Python para organizar investigaciones, ejecutar herramientas de reconocimiento, conservar evidencias y generar reportes por caso.

## Características

* Gestión de investigaciones mediante casos independientes.
* Organización de resultados y evidencias.
* Ejecución centralizada de herramientas OSINT.
* Visualización de resultados desde una interfaz de consola.
* Generación de reportes en Markdown y JSON.
* Registro de actividad y resultados de ejecución.
* Pruebas automatizadas.

## Herramientas integradas

| Herramienta | Función                                                      |
| ----------- | ------------------------------------------------------------ |
| Nmap        | Reconocimiento de redes y servicios.                         |
| Sublist3r   | Enumeración de subdominios.                                  |
| Sherlock    | Búsqueda de nombres de usuario en plataformas.               |
| Maigret     | Búsqueda de perfiles asociados a nombres de usuario.         |
| Holehe      | Comprobación de servicios asociados a direcciones de correo. |

Las herramientas externas deben estar instaladas y disponibles en el PATH del sistema.

Los resultados son indicios técnicos y no constituyen por sí solos una confirmación de identidad, titularidad o actividad.

## Requisitos

* Ubuntu 22.04 o posterior.
* Python 3.11 o posterior.
* Git.
* Herramientas externas que se deseen utilizar.

## Instalación

Clonar el repositorio:

```bash
git clone <URL_DEL_REPOSITORIO>
cd osint-lab
```

Crear y activar el entorno virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instalar el proyecto:

```bash
python -m pip install --upgrade pip
pip install -e .
```

Para instalar también las dependencias de desarrollo:

```bash
pip install -e ".[dev]"
```

## Ejecución

```bash
osint-lab
```

## Pruebas y análisis de código

Ejecutar las pruebas:

```bash
python -m pytest
```

Comprobar el código de la aplicación:

```bash
ruff check app
```

Comprobar los tests:

```bash
ruff check tests --ignore S101
```

## Estructura del proyecto

```text
osint-lab/
├── app/
│   ├── config/
│   ├── core/
│   ├── services/
│   ├── ui/
│   ├── utils/
│   ├── application.py
│   ├── main.py
│   └── tool_registry.py
├── scripts/
├── tests/
├── .gitignore
├── LICENSE
├── pyproject.toml
├── requirements.txt
└── requirements-dev.txt
```

## Seguridad y privacidad

* Los datos de investigaciones deben permanecer fuera del repositorio público.
* No almacenar contraseñas, tokens, claves API ni credenciales en el código.
* Mantener los archivos `.env` y los resultados locales fuera de Git.
* Proteger los directorios de evidencias y reportes.
* Verificar los resultados antes de incorporarlos a un informe.

## Uso responsable

Este proyecto está destinado a investigación, auditoría y aprendizaje en sistemas propios o con autorización expresa.

El usuario es responsable de cumplir la legislación aplicable, las condiciones de servicio de las plataformas y las normas de privacidad.

No utilizar estas herramientas para acoso, vigilancia no autorizada, suplantación, acceso indebido o vulneración de la privacidad de terceros.

## Licencia

Este proyecto se distribuye bajo la licencia MIT. Consultar el archivo `LICENSE`.
