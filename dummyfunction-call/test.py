from azure.keyvault.secrets import SecretClient
from azure.identity import AzureCliCredential
import requests

key_vault_name = "keyvault-dweebseye"
key_vault_url = f"https://{key_vault_name}.vault.azure.net"
secret_name = "dummy-dweebseye-key"
function_url = f"https://dummy-dweebseye.azurewebsites.net/api/httpexample"

credential = AzureCliCredential()
client = SecretClient(vault_url=key_vault_url, credential=credential)
function_key = client.get_secret(secret_name).value

payload = {'code':function_key, 'name':"Gustavo"}
response = requests.post(function_url, params=payload)
print(response.text)
