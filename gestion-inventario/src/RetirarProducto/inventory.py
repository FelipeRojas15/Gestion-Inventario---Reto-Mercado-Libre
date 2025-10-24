from botocore.exceptions import ClientError
from .config import table
from .exceptions import InventoryError

class Inventory:
    def deleteInventory(self, body):
        """ 
        Elimina un producto al inventario, cambiandole el estado a False.

        Args:
            body (dict): Contiene los datos del producto a eliminar.

        Returns:
            str: Mensaje indicando el resultado de la operación.

        Raises:
            InventoryError: Si ocurre un error en deleteInventory o en DynamoDB durante la operacion.
        """
        try:
            cantidad = body.get("cantidad", 0)
            producto_id = body.get("producto_id", "")

            respuesta = table.get_item(Key={"producto_id": producto_id})
            item = respuesta.get("Item")

            if item:
                table.update_item(
                    Key={"producto_id": producto_id},
                    UpdateExpression="SET estado = :d",
                    ExpressionAttributeValues={":d": False}
                )
                mensaje = f"PRODUCTO ACTUALIZADO: {item['nombre']} y su estado es {item['estado']}"
            else:
                mensaje = f"PRODUCTO NO EXISTE EN EL INVENTARIO: {producto_id}"

            return mensaje
        except ClientError as e:
            raise InventoryError(f"Error en DynamoDB: {e.response['Error']['Message']}")
        except Exception as e:
            raise InventoryError(f"Error en deleteInventory: {str(e)}")
