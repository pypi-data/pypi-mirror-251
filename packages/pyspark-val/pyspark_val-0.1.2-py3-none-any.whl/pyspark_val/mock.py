from typing import Dict, Any
from unittest.mock import Mock

from pyspark.sql.readwriter import PathOrPaths

def mock_read_parquet(paths: Dict[str, Any], mock: Mock = None) -> Mock:
    """
    This function provides an facility for mocking `spark.read.parquet` calls. See the example below.

    ```python
    paths = {
        'file/one.parquet': '_value_one_',
        'file/two.parquet': '_value_two_'
    }
    spark = mock_read_parquet(paths)

    spark.read.parquet('file/one.parquet')
    >>> '_value_one_'
    spark.read.parquet('file/two.parquet')
    >>> '_value_two_'
    ```

    Args:
        type (str): The type of read to mock.
        paths (Dict[str, Any]): A dictionary containing a mapping from input paths to objects returned.
        mock (Mock, optional): Existing mock object. Defaults to None.

    Returns:
        Mock: The mock with functionality displayed above
    """
    return mock_read('parquet', paths, mock)

def mock_read(type: str, paths: Dict[str, Any], mock: Mock = None) -> Mock:
    """
    This function provides a facility for mocking `spark.read` calls. See the example below.

    ```python
    paths = {
        'file/one.parquet': '_value_one_',
        'file/two.parquet': '_value_two_'
    }
    spark = mock_read('parquet', paths)

    spark.read.parquet('file/one.parquet')
    >>> '_value_one_'
    spark.read.parquet('file/two.parquet')
    >>> '_value_two_'
    ```

    Args:
        type (str): The type of read to mock.
        paths (Dict[str, Any]): A dictionary containing a mapping from input paths to objects returned.
        mock (Mock, optional): Existing mock object. Defaults to None.

    Returns:
        Mock: The mock with functionality displayed above
    """
    if mock is None:
        mock = Mock()

    def side_effect(path: str, *args, **kwargs):
        nonlocal paths

        if path not in paths:
            raise RuntimeError(f"Path not found in the mock's 'paths' dict: {path}")

        return paths[path]

    # Apply side effect to mock
    read_type = getattr(mock.read, type)
    read_type.side_effect = side_effect

    return mock