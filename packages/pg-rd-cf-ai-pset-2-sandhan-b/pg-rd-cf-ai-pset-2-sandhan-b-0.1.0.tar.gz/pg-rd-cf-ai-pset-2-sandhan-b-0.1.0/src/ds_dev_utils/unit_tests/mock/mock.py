"""Mock implementation of BlobServiceClient."""


class FakeBlobServiceClient:
    """Provides a Fake interface for azure.storage.blob.BlobServiceClient including
    implementation for:
    - BlobServiceClient.get_connection_str
    - BlobServiceClient.get_container_client
    - BlobContainerClient.get_blob_client
    - Blob.read_all

    e.g BlobServiceClient.from_connection_string(cnx_str). \
            get_container_client(cntr_name).get_blob_client(blob_name). \
            download_blob().readall()

    """

    def __init__(self, file_dict: dict=None):
        self.file_dict = file_dict
    
    @property
    def file_directory(self):
        return self.file_dict
    
    @file_directory.setter
    def file_directory(self, update_dict: dict):
        if isinstance(update_dict, dict):
            self.file_dict.update(update_dict)
        else:
            raise ValueError("Only type dict is accepted as a parameter!")

    def get_blob_client(self, blob, *args, **kwargs):

        f_location = self.file_dict.get(blob, None)
        f_dict = {"blob_service_selected_file": f_location}

        return FakeBlobServiceClient(f_dict)

    def download_blob(self, *args, **kwargs):
        return self

    def get_container_client(self, *args, **kwargs):
        return self
    
    def from_connection_string(self, *args, **kwargs):
        return self

    def readall(self):
        if len(self.file_dict) != 1:
            raise FileNotFoundError("File not found")
        f = open(self.file_dict["blob_service_selected_file"])
        f_contents = f.read()
        f.close()
        return bytes(f_contents, "utf-8")
