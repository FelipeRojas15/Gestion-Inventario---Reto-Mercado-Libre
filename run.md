### 1. ⚙️ Como ejecutar el proyecto:


A continuación se listan los **endpoints disponibles** para interactuar con la aplicación desplegada en AWS Lambda:

| Método | Descripción | Endpoint |
|:--------|:-------------|:----------|
| `POST` | Eliminar productos del inventario | [https://ywmxzuuip5yfvxxnzir3s66fpa0uistt.lambda-url.us-east-2.on.aws/dev/eliminar-productos](https://ywmxzuuip5yfvxxnzir3s66fpa0uistt.lambda-url.us-east-2.on.aws/dev/eliminar-productos) |
| `POST` | Actualizar información de un producto | [https://ywmxzuuip5yfvxxnzir3s66fpa0uistt.lambda-url.us-east-2.on.aws/dev/actualizar-producto](https://ywmxzuuip5yfvxxnzir3s66fpa0uistt.lambda-url.us-east-2.on.aws/dev/actualizar-producto) |
| `POST` | Registrar una orden de venta | [https://ywmxzuuip5yfvxxnzir3s66fpa0uistt.lambda-url.us-east-2.on.aws/dev/orden-venta](https://ywmxzuuip5yfvxxnzir3s66fpa0uistt.lambda-url.us-east-2.on.aws/dev/orden-venta) |
| `POST` | Registrar una orden de compra | [https://ywmxzuuip5yfvxxnzir3s66fpa0uistt.lambda-url.us-east-2.on.aws/dev/orden-compra](https://ywmxzuuip5yfvxxnzir3s66fpa0uistt.lambda-url.us-east-2.on.aws/dev/orden-compra) |
| `GET` | Obtener el inventario actual | [https://ywmxzuuip5yfvxxnzir3s66fpa0uistt.lambda-url.us-east-2.on.aws/dev/obtener-inventario](https://ywmxzuuip5yfvxxnzir3s66fpa0uistt.lambda-url.us-east-2.on.aws/dev/obtener-inventario) |

---
### 2. Ejemplo de ejecucion:

![Ejemlo de ejecucion script](https://github.com/FelipeRojas15/Gestion-Inventario---Reto-Mercado-Libre/blob/main/Imagenes/Ejemplo_Ejecucion.jpg)

![Ejemplo de ejecucion body](https://github.com/FelipeRojas15/Gestion-Inventario---Reto-Mercado-Libre/blob/main/Imagenes/Ejemplo_Ejecucion2.jpg)
---

📌 **Nota:** 
- Todos los endpoints están protegidos mediante validación de firma HMAC-SHA256 para garantizar la **integridad y autenticidad de los mensajes**.
- En la ruta Gestion-Inventario---Reto-Mercado-Libre/gestion-inventario/test se deja disponible una coleccion de PostMan y el pre-request que se debe tener en cuenta para   cada peticion 

---