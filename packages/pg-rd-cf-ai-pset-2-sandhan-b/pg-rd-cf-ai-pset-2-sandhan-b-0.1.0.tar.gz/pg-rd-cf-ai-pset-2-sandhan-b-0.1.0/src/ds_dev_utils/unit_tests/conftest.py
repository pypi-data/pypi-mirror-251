import os, pytest
from ds_dev_utils.unit_tests.mock.mock import FakeBlobServiceClient

@pytest.fixture(scope="class", autouse=True)
def mock_engine(request) -> FakeBlobServiceClient:
    file_dict = {
        "hello_world" : os.path.realpath(os.path.join(os.path.dirname(__file__),'mock', 'mock_file_storage', 'hello_world.txt'))
    }
    request.cls.client = FakeBlobServiceClient(file_dict)
    file_path = file_dict.get("hello_world")
    with open(file_path, "r") as f:
        request.cls.file_content = f.read()


@pytest.fixture(scope="class", autouse=True)
def mock_blob_config(request) -> dict:
    request.cls.mock_config_1 = {
        "container_name": "milky_way",
        "sas_connection_string": "solar_system",
        "blob_name" : "hello_world",
        "as_file" : True
    }
    request.cls.mock_config_2 = {
        "container_name": "milky_way",
        "sas_connection_string": "solar_system",
        "blob_name" : "hello_world",
        "as_file" : False
    }
    request.cls.mock_config_3 = {
        "container_name": 41,
        "sas_connection_string": "solar_system",
        "blob_name" : "hello_world",
        "as_file" : False
    }