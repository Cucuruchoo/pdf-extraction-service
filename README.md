
# PDF Extraction Service

## Descripción

Microservicio desarrollado en Python y FastAPI
para extraer texto de documentos PDF.

Forma parte del proyecto Desarrollo de Software 2026.

## Responsabilidad

Recibir documentos PDF desde Request Service,
extraer su contenido textual y devolverlo
mediante una API REST interna.

## Tecnologías

- Python 3.12
- FastAPI
- pypdf
- uv
- Docker
- pytest
- Ruff

## Arquitectura

El servicio separa las responsabilidades en:

- API: endpoints y validaciones HTTP.
- Aplicación: coordinación de la extracción.
- Dominio: abstracción de extracción de texto.
- Infraestructura: implementación mediante pypdf.

## Endpoints

### GET /health

Permite comprobar el estado del servicio.

### POST /internal/v1/extract

Recibe un PDF y devuelve su texto extraído.

Encabezados requeridos:

- Content-Type: application/pdf
- X-Filename: documento.pdf

El PDF se envía como cuerpo de la solicitud.

## Validaciones

- Content-Type application/pdf.
- Nombre con extensión .pdf.
- Tamaño máximo configurable, por defecto 10 MiB.
- Manejo de errores durante la extracción.

El procesamiento se realiza en memoria,
sin guardar temporalmente el PDF en disco
mediante la aplicación.

## Logging y trazabilidad

- Registros estructurados en JSON.
- Identificador X-Request-ID.
- Registro de duración y estado HTTP.
- Logs accesibles desde Docker.
- No se registra el contenido completo del PDF.

## Ejecución con Docker

Los repositorios deben encontrarse en
una misma carpeta:

Proyecto/
  pdf-request-service/
  pdf-extraction-service/
  pdf-storage-service/

Desde pdf-request-service ejecutar:

docker compose up --build -d

## Pruebas automatizadas

Desde pdf-extraction-service:

uv sync

uv run pytest -q

uv run ruff check app tests

## Consideraciones

- No realiza persistencia de documentos.
- No administra MongoDB.
- Es utilizado internamente por Request Service.
- Extrae texto disponible en el PDF; no incorpora OCR.
