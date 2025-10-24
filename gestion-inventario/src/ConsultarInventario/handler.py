import json
from decimal import Decimal
from .inventory import Inventory
from .exceptions import LambdaHandlerError


def decimal_default(obj):
    if isinstance(obj, Decimal):
        if obj % 1 == 0:
            return int(obj)
        return float(obj)
    raise TypeError


class LambdaHandler:
    def handle(self, event, context):
        """
        Realiza el control de la funcion Lambda.

        Gestiona la recepción del evento y context, para la busqueda total del inventario.

        arg:
            event (dict): Evento recibido directo por otra lambda.
            context (object): Contexto de ejecución proporcionado por AWS Lambda

        Returns:
            respuesta (Dict): Resultado de la validacion de la firma y operacion realizada

        Raises:
            LambdaHandlerError: Si ocurre un error en la operacion del inventario.
        """
        try:
            inventario = Inventory()
            resultado = inventario.getInventory()

            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps(
                    {"mensaje": "Inventario obtenido correctamente", "data": resultado},
                    default=decimal_default
                )
            }
        except LambdaHandlerError as e:
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": str(e)})
            }
        except Exception as e:
            return {
                "statusCode": 500,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": str(e)})
            }
