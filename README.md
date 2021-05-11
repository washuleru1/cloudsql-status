# cloudsql-status

cloudsql-status es un proyecto base Python, para actualizar el estado de una bd cloudsql en GCP

## Pre requisitos

Crear una cloud function con trigger de pub/sub [documentación](https://cloud.google.com/functions/docs/calling/pubsub) para que se gatille al recibir un evento de un tópico "x". Debe tener también creada una cuenta de servicio con rol "CloudSql Editor", asignada al scope en donde desea ejecutar la solución, al Folder, por ejemplo.


## Uso

Al despegar en cloud function, esta se gatilla automáticamente al recibir un evento. Setear el Entrypoint a la función pubsub_subscriber del main.py

## Contribuir
Bienvenidas dean los pull request. Para cambios mayores, favor primero crear un issue para exponer lo que se desea cambiar


## License
[MIT](https://choosealicense.com/licenses/mit/)