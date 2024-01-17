from azure.core.exceptions import ClientAuthenticationError
from azure.identity import DefaultAzureCredential, CredentialUnavailableError
from azure.keyvault.secrets import SecretClient
from cryptography.fernet import Fernet
from tqdm import tqdm
from typing import Union, List
from urllib.parse import urlparse
import base64
import getpass
import hashlib
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd

class DataHowdah(pd.DataFrame):

    def __init__(self, data_source, *args, **kwargs):
        """
        Initialize DreamHowdah with a DataFrame or a file path to load the DataFrame.
        """
        if isinstance(data_source, pd.DataFrame):
            super().__init__(data_source, *args, **kwargs)
        elif isinstance(data_source, str):
            super().__init__(self._load_dataframe(data_source), *args, **kwargs)
        else:
            raise TypeError("data_source must be a pandas DataFrame or a file path string")

        object.__setattr__(self, "_original_df", self.copy())
        # self._original_df = self.copy()

    @staticmethod
    def _load_dataframe(file_path):
        """
        Load a DataFrame from a file based on the file extension.
        """
        _, file_extension = os.path.splitext(file_path)
        if file_extension.lower() in ['.csv', '.txt']:
            return pd.read_csv(file_path)
        elif file_extension.lower() in ['.xlsx', '.xls']:
            return pd.read_excel(file_path)
        elif file_extension.lower() == '.json':
            return pd.read_json(file_path)
        elif file_extension.lower() == '.parquet':
            return pd.read_parquet(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")

    @staticmethod
    def _add_noise(series, scale=1.0):
        """
        Add noise to a numeric series while maintaining its distribution.
        Converts the series to numeric type before adding noise.
        """
        numeric_series = pd.to_numeric(series, errors='coerce')
        noise = np.random.normal(0, scale * numeric_series.std(), size=len(numeric_series))
        return numeric_series.add(noise, fill_value=0)

    def _parse_columns_to_mask(self, columns_to_mask, df_columns):
        """
        Parse the columns_to_mask input to get the actual columns to mask.
        """
        if columns_to_mask is None:
            return df_columns

        actual_columns_to_mask = []
        for item in columns_to_mask:
            if isinstance(item, range):
                actual_columns_to_mask.extend(df_columns[item])
            elif isinstance(item, int):
                actual_columns_to_mask.append(df_columns[item])
            else:
                actual_columns_to_mask.append(item)

        return [col for col in actual_columns_to_mask if col in df_columns]

    def mask(self, columns_to_mask: Union[List[Union[int, str, range]], None] = None, scale=1.0, plots=False):
        """
        Apply noise to specified numeric columns.
        columns_to_mask can be a list of column names, indices, or ranges.
        If plot is True, plot original and masked data for each specified column.
        """
        df_columns = self.columns
        actual_columns_to_mask = self._parse_columns_to_mask(columns_to_mask, df_columns)

        for col in actual_columns_to_mask:
            # original_col = self[col].copy()
            original_col = pd.to_numeric(self[col].copy(), errors='coerce')
            self[col] = self._add_noise(self[col], scale)
            if plots:
                self._plot_column(original_col, self[col], col)

        return self

    def _plot_column(self, original_col, masked_col, col_name):
        """
        Plot original and masked data for a specified column in cyberpunk style.
        """
        # Reset to default style before applying cyberpunk style
        # plt.style.use('default')
        plt.style.use('cyberpunk')
        plt.figure(figsize=(12, 6))

        # Plotting both original and masked data on the same plot
        plt.hist(original_col, bins=30, alpha=0.7, label='Original')
        plt.hist(masked_col, bins=30, alpha=0.7, label='Masked')

        plt.title(f"Original vs Masked - {col_name}")
        plt.xlabel('Value')
        plt.ylabel('Frequency')
        plt.legend()

        # Adding the cyberpunk style
        # mplcyberpunk.add_glow_effects()

        plt.show()
        plt.close()

    @staticmethod
    def _get_key():
        """
        Retrieve the encryption key from Azure Key Vault or environment.
        """
        azure_secret_url = os.environ.get('DATA_HOWDAH_AZURE_KEY_VAULT_SECRET_URL')
        if azure_secret_url:
            parsed_url = urlparse(azure_secret_url)
            vault_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
            secret_name = parsed_url.path.split('/')[-1]

            try:
                credential = DefaultAzureCredential()
                secret_client = SecretClient(vault_url=vault_url, credential=credential)
                retrieved_secret = secret_client.get_secret(secret_name)
                key = retrieved_secret.value
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
        else:
            # Fallback to environment variable or manual input
            key = os.environ.get('DATA_HOWDAH_ENCRYPTION_KEY')
            if not key:
                key = getpass.getpass('Enter encryption key: ')
        
        # Ensure the key is in the correct format for Fernet
        hashed_key = hashlib.sha256(key.encode()).digest()
        return base64.urlsafe_b64encode(hashed_key)

    @staticmethod
    def _encrypt_column(series, key):
        """
        Encrypt a DataFrame column.
        """
        f = Fernet(key)
        return series.apply(lambda x: base64.urlsafe_b64encode(f.encrypt(str(x).encode())).decode() if pd.notna(x) else x)

    @staticmethod
    def _encrypt_column_name(col_name, key):
        """
        Encrypt a column name.
        """
        f = Fernet(key)
        encrypted_name = f.encrypt(('ENCRYPTED_' + col_name).encode())
        return base64.urlsafe_b64encode(encrypted_name).decode()


    def encrypt(self, columns_to_encrypt: Union[List[Union[int, str, range]], None] = None, key=None):
        print()
        print("★·.·´¯`·.·★ ♥ ★·.·´¯`·.·★ <DataHowdah🐫>")
        print()
        """
        Encrypt specified columns and their names.
        """
        if key is None:
            key = self._get_key()

        df_columns = self.columns
        actual_columns_to_encrypt = self._parse_columns_to_mask(columns_to_encrypt, df_columns)

        # Encrypt column names
        new_column_names = {}
        for col in tqdm(actual_columns_to_encrypt, desc="🤫 Encrypting"):
            encrypted_col_name = self._encrypt_column_name(col, key)
            new_column_names[col] = encrypted_col_name
            self[col] = self._encrypt_column(self[col], key)

        self.rename(columns=new_column_names, inplace=True)
        print()
        print("★·.·´¯`·.·★ ♥ ★·.·´¯`·.·★ </DataHowdah🐫>")
        print()

        return self
    
    @staticmethod
    def _decrypt_column(series, key):
        """
        Decrypt a DataFrame column.
        """
        f = Fernet(key)
        return series.apply(lambda x: f.decrypt(base64.urlsafe_b64decode(x)).decode() if pd.notna(x) else x)
    
    @staticmethod
    def _decrypt_column_name(encrypted_col_name, key):
        """
        Decrypt an encrypted column name.
        """
        f = Fernet(key)
        name = base64.urlsafe_b64decode(encrypted_col_name)
        return f.decrypt(name).decode()
    
    def decrypt(self, key=None):
        print()
        print("★·.·´¯`·.·★ ♥ ★·.·´¯`·.·★ <DataHowdah🐫>")
        print()
        """
        Decrypt previously encrypted columns based on their names.
        """
        if key is None:
            key = self._get_key()

        new_column_names = {}
        for col in tqdm(self.columns, desc="🔑🔓 Decrypting"):
            try:
                # Attempt to decrypt the column name
                decrypted_col_name = self._decrypt_column_name(col, key)
                if decrypted_col_name.startswith('ENCRYPTED_'):
                    original_col_name = decrypted_col_name[len('ENCRYPTED_'):]
                    new_column_names[col] = original_col_name
                    self[col] = self._decrypt_column(self[col], key)
            except Exception:
                # If decryption fails, assume the column was not encrypted
                continue

        self.rename(columns=new_column_names, inplace=True)
        print()
        print("★·.·´¯`·.·★ ♥ ★·.·´¯`·.·★ </DataHowdah🐫>")
        print()
        return self