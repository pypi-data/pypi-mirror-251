# pip install azure-keyvault-keys azure-identity

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential, CredentialUnavailableError
from azure.keyvault.secrets import SecretClient
from azure.core.exceptions import ClientAuthenticationError

try:
    # Set up the Key Vault URL and Key Name
    key_vault_url = "https://data-howdah2.vault.azure.net/"
    secret_name = "mustafah-secret"

    # Authenticate to Azure
    credential = DefaultAzureCredential()

    # Connect to the Key Vault
    secret_client = SecretClient(vault_url=key_vault_url, credential=credential)

    # Retrieve the secret
    retrieved_secret = secret_client.get_secret(secret_name)
    encryption_key = retrieved_secret.value

    print(encryption_key)

except CredentialUnavailableError:
    print("❌ No credential available to access Key Vault. Please log in ...")
    # Here you can add logic to prompt the user to log in
    # For example, you might open a browser window for Azure login
    # or provide instructions to use Azure CLI for login

except ClientAuthenticationError as e:
    print("❌ Authentication error ...")
    # Handle other authentication related errors

except Exception as e:
    print("❌ An error occurred:", e.message)