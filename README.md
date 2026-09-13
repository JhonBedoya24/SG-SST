# Gestión Documental SG-SST

Aplicación web desarrollada para apoyar la gestión y administración de documentos relacionados con el Sistema de Gestión de Seguridad y Salud en el Trabajo (SG-SST).

## Descripción del proyecto

El proyecto consiste en una aplicación web sencilla que permite registrar y administrar información básica de los documentos utilizados dentro del SG-SST.

La aplicación está orientada principalmente a pequeñas empresas que requieren una herramienta básica para organizar la información documental.

## Funcionalidades

El sistema cuenta con las siguientes funcionalidades:

- Registro de documentos.
- Consulta de documentos registrados.
- Edición de documentos.
- Eliminación de documentos.
- Validación de campos obligatorios.
- Validación del número de versión.
- Almacenamiento de información mediante SQLite.

## Información administrada

Cada documento puede contener:

- Nombre del documento.
- Tipo de documento.
- Responsable.
- Fecha.
- Versión.
- Descripción.

## Tecnologías utilizadas

- Python
- Flask
- SQLite
- HTML5
- CSS3
- Git
- GitHub
- PyCharm

## Estructura del proyecto

```text
SG-SST/
│
├── static/
│   └── style.css
│
├── templates/
│   ├── index.html
│   ├── registrar.html
│   └── editar.html
│
├── .gitignore
├── app.py
├── main.py
├── sgsst.db
└── README.md