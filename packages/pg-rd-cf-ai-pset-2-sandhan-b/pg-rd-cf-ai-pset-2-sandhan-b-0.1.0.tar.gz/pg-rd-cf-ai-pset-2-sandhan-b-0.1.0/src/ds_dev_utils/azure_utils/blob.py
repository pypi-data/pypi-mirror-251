from azure.storage.blob import BlobServiceClient
import os, tempfile
from ds_dev_utils.azure_utils.validators.blob_config_validator import ValidateBlobParams

class blob_file:

    """
    
    Custom context manager module that returns a file handler or a file directory of a 
    file downloaded from a specified Azure blob storage.

    Parameters:
    container_name (str): Name of the Azure container
    blob_name (str): Name of the storage blob
    sas_connection_string (str): Secret string to establish connection with Azure blob storage
    as_file (bool): Flag indicating if return type is a file handler (True) or a file directory (False)

    Returns:
    File handle or String File Directory.

    """

    def __init__(
            self,
            container_name: str,
            blob_name: str,
            sas_connection_string:str,
            as_file:bool,
    ) -> None:
        self.container_name = container_name
        self.blob_name = blob_name
        self.sas_connection_string = sas_connection_string
        self.as_file = as_file
        _ = ValidateBlobParams(
            container_name=self.container_name,
            blob_name=self.blob_name,
            sas_connection_str=self.sas_connection_string,
            as_file=self.as_file
        )
    
    def __enter__(self):
        _service_client = BlobServiceClient.from_connection_string(self.sas_connection_string)
        _client = _service_client.get_container_client(self.container_name)
        _blob_client = _client.get_blob_client(self.blob_name)
        temp_dir = tempfile.TemporaryDirectory()
        temp_file_path = os.path.join(temp_dir.name, f'{self.blob_name}.txt')
        with open(temp_file_path, 'wb') as temp_blob:
            download_stream = _blob_client.download_blob()
            temp_blob.write(download_stream.readall())
        temp_blob = open(temp_file_path, 'rb')
        if self.as_file:
                return temp_blob
        else:
            return temp_file_path
    
    def __exit__(self, exc_type, exc_val, exc_tb):
    	if exc_type is not None:
            print(f'exception type: {exc_type}')
            print(f'exception value: {exc_val}')
            print(f'exception traceback: {exc_tb}')