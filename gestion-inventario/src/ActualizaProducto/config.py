SECRET_KEY = b"Mercado Libre"
TABLE_NAME = "product_t"

import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)
