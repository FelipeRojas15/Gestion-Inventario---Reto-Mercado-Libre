from botocore.exceptions import ClientError
from .config import table
from .exceptions import InventoryError

class Inventory:
    """
    Gestiona las operaciones relacionadas con el inventario en DynamoDB.

    Esta clase permite agregar, vender, actualizar
    y eliminar productos
    """
    def updateInventory(self, body):
        """ 
        Actualiza un producto del inventario.

        Args:
            body (dict): Contiene los datos del producto a actualizar.

        Returns:
            str: Mensaje indicando el resultado de la operación.

        Raises:
            InventoryError: Si ocurre un error en updateInventory o en DynamoDB durante la operacion.
        """
        try:
            nombre = body.get("nombre", "")
            precio = body.get("precio", 0)
            stock = body.get("cantidad", 0)
            estado = body.get("estado", "")
            producto_id = body.get("producto_id", "")

            respuesta = table.get_item(Key={"producto_id": producto_id})
            item = respuesta.get("Item")

            if estado.lower() == "true":
                estado = True
            elif estado.lower() == "false":
                estado = False

            if item:
                table.update_item(
                    Key={"producto_id": producto_id},
                    UpdateExpression="SET nombre = :nombre, precio = :precio, stock = :stock, estado = :estado",
                    ExpressionAttributeValues={
                        ":nombre": nombre,
                        ":precio": precio,
                        ":stock": stock,
                        ":estado": estado
                    }
                )
                mensaje = f"PRODUCTO ACTUALIZADO: {nombre}"
            else:
                mensaje = f"NO EXISTE EL PRODUCTO: {nombre}"

            return mensaje
        except ClientError as e:
            raise InventoryError(f"Error en DynamoDB: {e.response['Error']['Message']}")
        except Exception as e:
            raise InventoryError(f"Error en updateInventory: {str(e)}")
