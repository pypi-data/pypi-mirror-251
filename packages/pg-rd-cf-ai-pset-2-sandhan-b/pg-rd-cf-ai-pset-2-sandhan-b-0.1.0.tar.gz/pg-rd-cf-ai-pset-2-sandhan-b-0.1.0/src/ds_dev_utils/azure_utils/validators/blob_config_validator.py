from pydantic import BaseModel

class ValidateBlobParams(BaseModel):
    container_name: str
    blob_name: str
    sas_connection_str: str
    as_file: bool