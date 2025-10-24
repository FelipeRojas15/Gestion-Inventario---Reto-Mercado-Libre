from botocore.exceptions import ClientError
from decimal import Decimal
from .config import table
from .exceptions import InventoryError

class Inventory:
    """
    Gestiona las operaciones relacionadas con el inventario en DynamoDB.

    Esta clase permite agregar, vender, actualizar, consultar
    y eliminar productos
    """
    def getInventory(self):
        """ 
        Obtiene todos los productos que existan en la tabla product_t

        Returns:
            items (list): Lista con todos los productos.

        Raises:
            InventoryError: Si ocurre un error en getInventory o en DynamoDB durante la operacion.
        """
        try:
            items = []
            last_evaluated_key = None

            while True:
                if last_evaluated_key:
                    response = table.scan(ExclusiveStartKey=last_evaluated_key)
                else:
                    response = table.scan()

                items.extend(response.get('Items', []))
                last_evaluated_key = response.get('LastEvaluatedKey')

                if not last_evaluated_key:
                    break

            return items
        except ClientError as e:
            raise InventoryError(f"Error en DynamoDB: {e.response['Error']['Message']}")
        except Exception as e:
            raise InventoryError(f"Error en getInventory: {str(e)}")
