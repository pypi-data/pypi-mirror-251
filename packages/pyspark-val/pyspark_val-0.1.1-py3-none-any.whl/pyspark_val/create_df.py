from typing import Dict
from collections.abc import Iterable

from pyspark.sql import SparkSession, DataFrame

def from_dict(spark: SparkSession, d: Dict[str, Iterable]) -> DataFrame:
    # Assert each element in the dict is a iterable with same size
    size = None
    for val in d.values():
        assert isinstance(val, Iterable), "Dictionary must contain only iterable elements"

        if size is None:
            size = len(val)
        else:
            assert size == len(val), "Dictionary elements must be all of the same size"

    rows = []
    for i in range(size):
        row = [col[i] for col in d.values()]
        rows.append(row)

    return spark.sparkContext.parallelize(rows).toDF(list(d.keys()))