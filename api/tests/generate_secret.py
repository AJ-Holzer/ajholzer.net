import secrets
import base64

secret_length: int = int(input("How many bytes should be secret have? >> "))
secret: str = base64.urlsafe_b64encode(secrets.token_bytes(secret_length)).decode()

print(secret)
