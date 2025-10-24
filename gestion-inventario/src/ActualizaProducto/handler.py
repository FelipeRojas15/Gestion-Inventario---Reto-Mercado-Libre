import json
from .signature import Signature
from .inventory import Inventory
from .exceptions import SignatureError, InventoryError

class LambdaHandler:
    """
    Realiza el control de la  funcion Lambda.

    Gestiona la recepción del evento SNS, la validación de la firma y
    la ejecución de las operaciones de inventario.
    """
    def handle(self, event):
        """
        Procesa el evento del broker SNS, valida la integridad de la firma y logica
        en el inventario

        arg:
            event: Evento SNS con mensaje JSON 

        Returns:
            respuesta (Dict): Resultado de la validacion de la firma y operacion realizada  

        Raises:
            SignatureError: Si ocurre un error en la validacion de la firma.
            InventoryError: Si ocurre un error en la operacion del inventario.
        """
        try:
            message_str = event['Records'][0]['Sns']['Message']

            try:
                message = json.loads(message_str)
            except json.JSONDecodeError:
                return {"error": "El mensaje SNS no es un JSON válido"}

            signature = Signature(message)
            signatureValidation = signature.checkSignature()

            if signatureValidation == "Invalida":
                respuesta = {
                    "RespuestaFirma": signatureValidation,
                    "Respuesta": "Firma inválida. Operación cancelada."
                }
            else:
                inventario = Inventory()
                body = message.get("body", {})
                respuestaInv = inventario.updateInventory(body)
                respuesta = {
                    "RespuestaFirma": signatureValidation,
                    "RespuestaMovimiento": respuestaInv
                }

            return respuesta

        except SignatureError as e:
            return self.respuesta(403, {"error": str(e)})

        except InventoryError as e:
            return self.respuesta(500, {"error": str(e)})

        except Exception as e:
            return self.respuesta(500, {"error": "Error interno del servidor"})

    def respuesta(self, status, body):
        return {
            "statusCode": status,
            "body": json.dumps(body)
        }
