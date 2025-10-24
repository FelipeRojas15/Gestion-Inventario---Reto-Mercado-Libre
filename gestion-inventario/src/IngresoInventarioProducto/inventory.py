from botocore.exceptions import ClientError
from .config import table
from .exceptions import InventoryError

class Inventory:
    """
    Gestiona las operaciones relacionadas con el inventario en DynamoDB.

    Esta clase permite agregar, vender, actualizar
    y eliminar productos
    """
    def addInventory(self, body):
        """ 
        Agrega un producto al inventario o aumenta su stock en caso de que 
        ya exista.

        Args:
            body (dict): Contiene los datos del producto a agregar.

        Returns:
            str: Mensaje indicando el resultado de la operación.

        Raises:
            InventoryError: Si ocurre un error en addInventory o en DynamoDB durante la operacion.

        """
        try:
            producto_id = body.get("producto_id", "")
            cantidad = body.get("cantidad", 0)
            nombre = body.get("nombre", "")
            precio = body.get("precio", 0)

            if not producto_id:
                raise InventoryError("El campo 'producto_id' es obligatorio.")

            respuesta = table.get_item(Key={"producto_id": producto_id})
            item = respuesta.get("Item")

            if item:
                nuevo_stock = item.get("stock", 0) + cantidad
                table.update_item(
                    Key={"producto_id": producto_id},
                    UpdateExpression="SET stock = :s, estado = :d",
                    ExpressionAttributeValues={":s": nuevo_stock, ":d": True},
                )
                mensaje = f"PRODUCTO ACTUALIZADO: {item['nombre']}, El stock es: {nuevo_stock}"
            else:
                table.put_item(
                    Item={
                        "producto_id": producto_id,
                        "nombre": nombre,
                        "precio": precio,
                        "stock": cantidad,
                        "estado": True
                    }
                )
                mensaje = f"PRODUCTO NUEVO AGREGADO: {nombre} con stock {cantidad}"

            return mensaje
        except ClientError as e:
            raise InventoryError(f"Error en DynamoDB: {e.response['Error']['Message']}")
        except Exception as e:
            raise InventoryError(f"Error en addInventory: {str(e)}")
