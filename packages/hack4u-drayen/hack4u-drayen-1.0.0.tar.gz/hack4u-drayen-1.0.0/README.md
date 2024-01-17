# Hack4U Python Library

[![PyPI version](https://badge.fury.io/py/hack4u.svg)](https://badge.fury.io/py/hack4u)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## Descripción

La biblioteca `hack4u` es una herramienta sencilla que te permite obtener información detallada sobre los cursos de hacking ético ofrecidos por la Academia Hack4u. Esta librería facilita el acceso a datos esenciales sobre los cursos, como el nombre del curso, el instructor y la URL de la página del curso en Hack4u.

## Instalación

Puedes instalar la librería `hack4u` utilizando pip. Abre tu terminal y ejecuta el siguiente comando:

```bash
pip install hack4u
```

## Uso básico

```python
from hack4u import Hack4u

# Crear una instancia del cliente
hack4u_client = Hack4u()

# Obtener la lista de cursos
courses = hack4u_client.get_courses()

# Imprimir información sobre cada curso
for course in courses:
    print(f"Nombre del curso: {course['name']}")
    print(f"Instructor: {course['instructor']}")
    print(f"URL del curso: {course['url']}")
    print("-" * 50)
```

## Contribuir

¡Las contribuciones son bienvenidas! Si deseas mejorar la biblioteca, realiza un fork del repositorio, crea una rama con tus cambios y presenta una solicitud de extracción. Asegúrate de seguir las pautas de contribución en el archivo [CONTRIBUTING.md](CONTRIBUTING.md).

## Licencia

Esta librería está distribuida bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para obtener más detalles.

## Contacto

Si tienes alguna pregunta o problema con la librería, no dudes en abrir un [issue](https://github.com/tuusuario/hack4u/issues) en el repositorio de GitHub.

¡Gracias por usar `hack4u`! Esperamos que sea útil para tu exploración en el mundo del hacking ético en la Academia Hack4u.
