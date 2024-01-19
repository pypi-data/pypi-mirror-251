from typing import Dict
from collections.abc import Iterable

from pyspark.sql import SparkSession, DataFrame

def df_from_dict(spark: SparkSession, data: Dict[str, Iterable]) -> DataFrame:
    """
    This function provides an easy way to create a DataFrame from a python dictionary of iterable values.

    Args:
        spark (SparkSession): The spark session to use.
        data (Dict[str, Iterable]): The data to create a DataFrame from

    Returns:
        DataFrame: _description_
    """
    # Assert each element in the dict is a iterable with same size
    size = None
    for val in data.values():
        assert isinstance(val, Iterable), "Dictionary must contain only iterable elements"

        if size is None:
            size = len(val)
        else:
            assert size == len(val), "Dictionary elements must be all of the same size"

        # Validate uniform type
        col_type = None
        for x in val:
            if col_type is None and x is not None:
                col_type = type(x)
            else:
                assert type(x) == col_type or x is None, "The dictionary iterables should only contain values with the same type and 'None'"


    rows = []
    for i in range(size):
        row = [col[i] for col in data.values()]

        rows.append(row)

    return spark.sparkContext.parallelize(rows).toDF(list(data.keys()))