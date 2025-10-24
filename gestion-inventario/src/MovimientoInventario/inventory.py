from botocore.exceptions import ClientError
from .config import table
from .exceptions import InventoryError

class Inventory:
    """
    Gestiona las operaciones relacionadas con el inventario en DynamoDB.

    Esta clase permite agregar, vender, actualizar
    y eliminar productos
    """
    def subtractInventory(self, body):
        """ 
        Resta stock a un producto del inventario.

        Args:
            body (dict): Contiene los datos del producto que fue comprado.

        Returns:
            str: Mensaje indicando el resultado de la operación.

        Raises:
            InventoryError: Si ocurre un error en subtractInventory o en DynamoDB durante la operacion.
        """
        try:
            cantidad = body.get("cantidad", 0)
            producto_id = body.get("producto_id", "")

            respuesta = table.get_item(Key={"producto_id": producto_id})
            item = respuesta.get("Item")

            if item:
                stock = item.get("stock", 0)
                if stock >= cantidad:
                    nuevo_stock = stock - cantidad
                    table.update_item(
                        Key={"producto_id": producto_id},
                        UpdateExpression="SET stock = :s",
                        ExpressionAttributeValues={":s": nuevo_stock},
                    )
                    mensaje = f"PRODUCTO ACTUALIZADO: {item['nombre']}, El stock es: {nuevo_stock}"
                else:
                    mensaje = f"STOCK INSUFICIENTE: {item['nombre']}"
            else:
                mensaje = f"NO EXISTE EL PRODUCTO: {producto_id}"

            return mensaje
        except ClientError as e:
            raise InventoryError(f"Error en DynamoDB: {e.response['Error']['Message']}")
        except Exception as e:
            raise InventoryError(f"Error en subtractInventory: {str(e)}")
