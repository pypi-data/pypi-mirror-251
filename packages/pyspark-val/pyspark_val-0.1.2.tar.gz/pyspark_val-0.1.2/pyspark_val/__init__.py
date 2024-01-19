import pytest

pytest.register_assert_rewrite("pyspark_val.assertion")

from ._backwards import assert_pyspark_df_equal