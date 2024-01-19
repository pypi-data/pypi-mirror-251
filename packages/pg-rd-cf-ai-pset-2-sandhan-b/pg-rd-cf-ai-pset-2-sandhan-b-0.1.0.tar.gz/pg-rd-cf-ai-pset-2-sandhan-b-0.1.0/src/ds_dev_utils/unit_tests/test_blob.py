from unittest import TestCase
from unittest.mock import patch
from pydantic import ValidationError
import os, pytest
from ds_dev_utils.unit_tests.mock.mock import FakeBlobServiceClient
from ds_dev_utils.azure_utils.blob import blob_file
from ds_dev_utils.azure_utils import blob

@pytest.mark.usefixtures("mock_engine", "mock_blob_config")
class TestAzureBlobCall(TestCase):    
    @patch.object(blob.BlobServiceClient, "from_connection_string", FakeBlobServiceClient({
        "hello_world" : os.path.realpath(os.path.join(os.path.dirname(__file__),'mock', 'mock_file_storage', 'hello_world.txt'))
    }).from_connection_string)
    def test_blob_file(
        self,
    ) -> None:
        validation_error_config = self.mock_config_3

        # Test invalid input

        with self.assertRaises(ValidationError):
            blob_file(**validation_error_config)
        
        # Test as_file True and False cases

        test_config = [self.mock_config_1, self.mock_config_2]
        for cfg in test_config:
            with blob_file(**cfg) as file:
                if cfg["as_file"]:
                    f = file.read()
                    self.assertEqual(f, b"Hello World!")                
                else:
                    f_name = file.split("/")[-1]
                    self.assertEqual(f_name, "hello_world.txt")