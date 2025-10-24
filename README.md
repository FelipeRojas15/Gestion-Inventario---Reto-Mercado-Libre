# 🧩 Gestion de Inventario

Este proyecto está compuesto por múltiples funciones **AWS Lambda** organizadas en módulos, diseñadas para gestionar un sistema de inventario utilizando **AWS DynamoDB** y **SNS**.  
A continuación se describe cada componente y su propósito.

---

## 🏗️ Arquitectura del Sistema - Diagrama de Componentes

La siguiente imagen muestra la arquitectura de componentes, incluyendo los componentes de **API Gateway**, **SNS**, **DynamoDB** y las funciones **Lambda** encargadas de gestionar el inventario.

![Arquitectura del Sistema](https://github.com/FelipeRojas15/Gestion-Inventario---Reto-Mercado-Libre/blob/main/Imagenes/Reto%201%20-%20Diagrama%20de%20componentes%20-%20Arquitectura_Reto_MELI.png)

---
## 🧩 Justificación de la Arquitectura

La arquitectura implementada es **orientada a eventos (Event-Driven Architecture, EDA)**, complementado con patrones de **API Gateway**, **Shared Database** y **tácticas de verificación de integridad y trazabilidad distribuida**.  
Este diseño busca garantizar **desacoplamiento, latencia, escalabilidad  y consistencia** en la gestión del inventario dentro de un entorno altamente dinámico.

---

### 1. 📨 Uso de colas y priorización de eventos

El uso de **tópicos SNS** permite manejar de forma eficiente los flujos asincrónicos entre los distintos componentes del sistema.  

---

### 2. ⚙️ Desacoplamiento y escalabilidad independiente

Cada componente del sistema (por ejemplo, `OrdenCompra`, `MovimientoInventario`, `ActualizaProducto`) está **desacoplado** mediante el uso de eventos y funciones Lambda autónomas.  
Este desacoplamiento favorece que cada servicio pueda **escalar de forma independiente**, tanto vertical como horizontalmente, de acuerdo con la demanda. Esto permite ante eventos estocasticos o picos de carga, garantizar la resiliencia operativa.

---

### 3. 🗄️ Persistencia compartida y consistencia de datos

Se adopta la táctica **Shared Database**, permitiendo que múltiples funciones Lambda interactúen con la misma base de datos (**DynamoDB**) para mantener la consistencia del inventario. 
Esto crea acoplamiento en el sistema, sin embargo, asegura la integridad transaccional en tiempo real.

#### 📋 Tabla principal: `product_t`

| Atributo | Tipo | Descripción |
|:----------|:------|:-------------|
| `producto_id` | **String (PK)** | Identificador único del producto dentro del sistema. Notacion: (PRO000) |
| `nombre` | **String** | Nombre descriptivo del producto. |
| `stock` | **Number** | Cantidad disponible en el inventario. |
| `precio` | **Number** | Valor unitario del producto. |
| `estado` | **Boolean** | Indica si el producto está activo (`True`) o eliminado (`False`). 
---

### 4. 🔍 Observabilidad y trazabilidad distribuida

El sistema se apoya en **Amazon CloudWatch** para el monitoreo de logs, métricas y alarmas.  
Cada evento publicado en SNS incluye metadatos que facilitan la **trazabilidad distribuida** de los mensajes, permitiendo auditar y diagnosticar el flujo completo de una transacción desde el API Gateway hasta la persistencia.

---

### 5. 🔐 Verificación e integridad de mensajes

Para garantizar la seguridad y confiabilidad del sistema, se implemento la tactica de **Verificacion integridad de los mensajes** esto nos permite darnos cuenta si estamos siendo vulnerados por **Tampering**. Al cifrar el request con la llave privada y luego validar la firma en el destino, encriptando de nuevo y comparando la firma en el destino, nos protege ante alguna manipulacion o alteracion no autorizada de los mensajes dentro del sistema   

---

A continuación se listan los **endpoints disponibles** para interactuar con la aplicación desplegada en AWS Lambda:

| Método | Descripción | Endpoint |
|:--------|:-------------|:----------|
| `POST` | Eliminar productos del inventario | [https://ywmxzuuip5yfvxxnzir3s66fpa0uistt.lambda-url.us-east-2.on.aws/dev/eliminar-productos](https://ywmxzuuip5yfvxxnzir3s66fpa0uistt.lambda-url.us-east-2.on.aws/dev/eliminar-productos) |
| `POST` | Actualizar información de un producto | [https://ywmxzuuip5yfvxxnzir3s66fpa0uistt.lambda-url.us-east-2.on.aws/dev/actualizar-producto](https://ywmxzuuip5yfvxxnzir3s66fpa0uistt.lambda-url.us-east-2.on.aws/dev/actualizar-producto) |
| `POST` | Registrar una orden de venta | [https://ywmxzuuip5yfvxxnzir3s66fpa0uistt.lambda-url.us-east-2.on.aws/dev/orden-venta](https://ywmxzuuip5yfvxxnzir3s66fpa0uistt.lambda-url.us-east-2.on.aws/dev/orden-venta) |
| `POST` | Registrar una orden de compra | [https://ywmxzuuip5yfvxxnzir3s66fpa0uistt.lambda-url.us-east-2.on.aws/dev/orden-compra](https://ywmxzuuip5yfvxxnzir3s66fpa0uistt.lambda-url.us-east-2.on.aws/dev/orden-compra) |
| `GET` | Obtener el inventario actual | [https://ywmxzuuip5yfvxxnzir3s66fpa0uistt.lambda-url.us-east-2.on.aws/dev/obtener-inventario](https://ywmxzuuip5yfvxxnzir3s66fpa0uistt.lambda-url.us-east-2.on.aws/dev/obtener-inventario) |

---

📌 **Nota:** 
- Todos los endpoints están protegidos mediante validación de firma HMAC-SHA256 para garantizar la **integridad y autenticidad de los mensajes**.
- En la ruta Gestion-Inventario---Reto-Mercado-Libre/gestion-inventario/test se deja disponible una coleccion de PostMan y el pre-request que se debe tener en cuenta para   cada peticion 
---


### 🧠 Conclusión

Esta arquitectura de microservicios, basada en eventos, permite construir un sistema de inventario **altamente resiliente, escalable y seguro**, donde cada componente cumple una función específica.  

---
## 📦 Estructura del Proyecto

### 1. `config.py`
Contiene la configuración base del sistema:

- 🔑 Clave secreta para validación de firmas (`SECRET_KEY`).
- 🗃️ Nombre de la tabla DynamoDB (`TABLE_NAME`).
- ⚙️ Inicialización del recurso DynamoDB.

---

### 2. `exceptions.py`
Define excepciones personalizadas para manejo de errores:

- **`SignatureError`** → errores en la validación de firmas.  
- **`InventoryError`** → errores en operaciones de inventario.  
- **`LambdaHandlerError`** → errores en el controlador principal.  
- **`SNSPublisherError`** → errores al publicar en SNS.

---

### 3. `inventory.py`
Contiene la clase **`Inventory`** con métodos para gestionar productos:

- `addInventory` → agrega o actualiza productos.  
- `updateInventory` → modifica los datos de un producto existente.  
- `getInventory` → obtiene todos los productos del inventario.  
- `subtractInventory` → descuenta stock de un producto.  
- `deleteInventory` → marca un producto como inactivo (`estado = False`).

---

### 4. `signature.py`
Clase **`Signature`** para validar la integridad de los mensajes usando **HMAC-SHA256**:

- `checkSignature` → compara la firma recibida con la calculada.

---

### 5. `handler.py`
Controlador principal de cada Lambda:

- Recibe eventos desde **SNS**.  
- Valida la firma.  
- Ejecuta la operación correspondiente en el inventario.

Cada Lambda tiene su propio `handler.py` adaptado al tipo de operación:

- Agregar producto.  
- Actualizar producto.  
- Obtener inventario.  
- Eliminar producto.  
- Restar stock.

---

### 6. `lambda_function.py`
Punto de entrada para cada función **Lambda**.  
Invoca el `LambdaHandler` correspondiente.

---

### 7. `sns_publisher.py`
Clase **`SNSPublisher`** para publicar mensajes en tópicos **SNS**:

- `publish` → envía mensajes JSON a un tópico SNS.

---

### 8. `SNSLambdaDispatcher`
Lambda que actúa como **dispatcher** para solicitudes HTTP desde **API Gateway**:

- En solicitudes **GET**, invoca directamente la Lambda de inventario.  
- En solicitudes **POST**, publica mensajes en el tópico SNS correspondiente.

---

## 🚀 Despliegue

Este sistema está diseñado para ejecutarse en **AWS Lambda** y comunicarse mediante **SNS**.  
Se recomienda usar **AWS SAM** o **Serverless Framework** para el despliegue.

---

## ✅ Requisitos

- Python **3.9+**  
- AWS SDK (**boto3**)  
- Permisos adecuados para acceso a **DynamoDB**, **SNS** y **Lambda**.

---

## 📌 Notas

- Todas las operaciones están protegidas por validación de firma **HMAC-SHA256**.  
- El campo `estado` en los productos determina si están activos o eliminados.  
