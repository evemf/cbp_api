# Catalonia Blackball Party API

La API de **Catalonia Blackball Party** está diseñada para gestionar las funcionalidades clave de un evento de forma eficiente, como la gestión de usuarios, pagos, y la integración con Firebase para el envío de notificaciones push.

## Tecnologías Utilizadas

- **Python**: Lenguaje de programación utilizado para desarrollar la API.
- **FastAPI**: Framework para la creación de APIs rápidas y eficientes.
- **PostgreSQL**: Sistema de gestión de bases de datos utilizado para almacenar la información del evento.
- **SQLAlchemy**: ORM para interactuar con la base de datos de manera sencilla.
- **Firebase**: Utilizado para la autenticación de usuarios y envío de notificaciones push.
- **SMTP (Gmail)**: Para el envío de correos electrónicos de confirmación y notificaciones a los usuarios.
- **Docker**: Contenedor utilizado para facilitar el desarrollo y despliegue de la API.
- **Heroku / IONOS**: Servicios utilizados para desplegar la API en producción.

## Funcionalidades

- **Gestión de Usuarios**: Registro, inicio de sesión y gestión de perfiles de los participantes.
- **Sistema de Pago**: Integración con plataformas de pago para gestionar los depósitos de pago como reserva al evento.
- **Notificaciones Push**: Envío de notificaciones en tiempo real utilizando **Firebase Cloud Messaging** (FCM).
- **Seguridad**: Autenticación mediante JWT utilizando el algoritmo **HS256**.
- **Correo Electrónico**: Envío automático de correos electrónicos (confirmaciones de registro).

## Instalación

Sigue estos pasos para instalar y configurar la API en tu entorno local o de producción:

1. Clona el repositorio en tu máquina local:

   git clone https://github.com/tu-usuario/catalonia-blackball-party-api.git
   cd catalonia-blackball-party-api

2. Crear un entorno virtual para el proyecto (opcional pero recomendado):

   python3 -m venv venv
   source venv/bin/activate  # Para sistemas Unix
   venv\Scripts\activate  # Para Windows

3. Instalar las dependencias del proyecto:

   pip install -r requirements.txt

4. Crear archivo `.env` y correctamente estos valores según tu entorno.


5. Ejecutar la API en entorno local:

   uvicorn main:app --reload

   Ahora puedes acceder a la API en http://127.0.0.1:8000.

## Autor

Este proyecto ha sido desarrollado por **Evelia Molina**.

## Licencia

Este proyecto está bajo la licencia MIT - consulta el archivo [LICENSE](./LICENSE) para más detalles.
