# 🧩 Inventario Lambda System

Este proyecto está compuesto por múltiples funciones **AWS Lambda** organizadas en módulos, diseñadas para gestionar un sistema de inventario utilizando **AWS DynamoDB** y **SNS**.  
A continuación se describe cada componente y su propósito.

---

## 🏗️ Arquitectura del Sistema - Diagrama de Componentes

La siguiente imagen muestra la arquitectura general del sistema, incluyendo los componentes de **API Gateway**, **SNS**, **DynamoDB** y las funciones **Lambda** encargadas de gestionar el inventario.

![Arquitectura del Sistema](https://github.com/FelipeRojas15/Gestion-Inventario---Reto-Mercado-Libre/blob/main/Imagenes/Reto%201%20-%20Diagrama%20de%20componentes%20-%20Arquitectura_Reto_MELI.png)

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
- Las respuestas están formateadas para ser compatibles con **API Gateway**.
