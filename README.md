# FastInventory por Enmanuel Brett 28.501.636

FastInventory es una API REST diseñada para la gestión eficiente de productos mediante operaciones CRUD (Crear, Leer, Actualizar y Eliminar).

## Requisitos Previos

- Python 3.8 o superior
- [Visual Studio Code](https://code.visualstudio.com/) (opcional, pero recomendado)

## Configuración del Entorno Virtual

Para aislar las dependencias del proyecto, se recomienda utilizar un entorno virtual. Siga los siguientes pasos:

1. Abra una terminal en la raíz del proyecto.
2. Cree el entorno virtual ejecutando:

   ```powershell
   python -m venv venv
   ```

3. Active el entorno virtual con el siguiente comando:

   ```powershell
   .\venv\Scripts\Activate
   ```

   > **Nota:** Si utiliza una terminal diferente, el comando de activación puede variar.

## Instalación de Dependencias

Con el entorno virtual activado, instale las dependencias necesarias ejecutando:

```powershell
pip install -r requirements.txt
```

## Ejecución del Proyecto

Para iniciar el servidor de desarrollo, utilice el siguiente comando:

```powershell
uvicorn app:app --host=localhost --port=8000 --reload
```

Una vez iniciado, la documentación interactiva estará disponible en: [http://localhost:8000/docs](http://localhost:8000/docs)

## Recursos Adicionales

- [Documentación de FastAPI](https://fastapi.tiangolo.com/es/)
- [Documentación de Uvicorn](https://www.uvicorn.org/)

---

## Tareas Pendientes

A continuación se detallan las tareas para la ampliación de la API:

1. **Gestión de Categorías de Productos**

   - Implementar endpoints para:
     - Obtener todas las categorías.
     - Crear una nueva categoría.
     - Actualizar una categoría existente.
     - Eliminar una categoría.

2. **Relación Producto-Categoría**

   - Cada producto debe estar asociado a una categoría mediante el campo `category_id`.
   - Al crear un producto, validar que la categoría especificada exista en la base de datos (`db.json`).
   - Si la categoría no existe, retornar un mensaje de error claro y descriptivo.

3. **Validaciones y Buenas Prácticas**
   - Garantizar que no se puedan eliminar categorías que estén asociadas a productos existentes.
   - Documentar los nuevos endpoints en la documentación interactiva de la API (`/docs`).
   - Asegurar respuestas consistentes y manejo adecuado de errores.

> **Sugerencia:** Utilice Pydantic para la validación de datos y asegúrese de mantener la integridad referencial entre productos y categorías.

---
