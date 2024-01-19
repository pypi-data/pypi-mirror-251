from functools import wraps

from .assertion import dfs_equal

# Thin wrapper to maintain backwards compatibility with pyspark-test
@wraps(dfs_equal)
def assert_pyspark_df_equal(*args, **kwargs):
    return dfs_equal(*args, **kwargs)