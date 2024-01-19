from typing import Any

import pyspark

try:
    from pyspark.sql.connect.dataframe import DataFrame as CDF

    has_connect_deps = True
except ImportError:
    has_connect_deps = False


def _check_isinstance_df(test: Any, truth: Any):
    types_to_test = [pyspark.sql.DataFrame]
    msg_string = ""
    # If Spark Connect dependencies are not available, the input is not going to be a Spark Connect
    # DataFrame so we can safely skip the validation.
    if has_connect_deps:
        types_to_test.append(CDF)
        msg_string = " or {CDF}"

    test_good = any(map(lambda x: isinstance(test, x), types_to_test))
    truth_good = any(map(lambda x: isinstance(truth, x), types_to_test))
    assert (
        test_good
    ), f"Expected type {pyspark.sql.DataFrame}{msg_string}, found {type(test)} instead"
    assert (
        truth_good
    ), f"Expected type {pyspark.sql.DataFrame}{msg_string}, found {type(truth)} instead"

    # Check that both sides are of the same DataFrame type.
    assert type(test) == type(
        truth
    ), f"Test and truth DataFrames are not of the same type: {type(test)} != {type(truth)}"


def _check_columns(
    check_columns_in_order: bool,
    test_df: pyspark.sql.DataFrame,
    truth_df: pyspark.sql.DataFrame,
):
    if check_columns_in_order:
        assert test_df.columns == truth_df.columns, "df columns name mismatch"
    else:
        assert sorted(test_df.columns) == sorted(
            truth_df.columns
        ), "df columns name mismatch"


def _check_schema(
    check_columns_in_order: bool,
    test_df: pyspark.sql.DataFrame,
    truth_df: pyspark.sql.DataFrame,
):
    if check_columns_in_order:
        assert test_df.dtypes == truth_df.dtypes, "df schema type mismatch"
    else:
        assert sorted(test_df.dtypes, key=lambda x: x[0]) == sorted(
            truth_df.dtypes, key=lambda x: x[0]
        ), "df schema type mismatch"


def _check_df_content(
    test_df: pyspark.sql.DataFrame,
    truth_df: pyspark.sql.DataFrame,
):
    test_df_list = test_df.collect()
    truth_df_list = truth_df.collect()

    for row_index in range(len(test_df_list)):
        for column_name in test_df.columns:
            test_cell = test_df_list[row_index][column_name]
            truth_cell = truth_df_list[row_index][column_name]
            if test_cell == truth_cell:
                assert True
            elif test_cell is None and truth_cell is None:
                assert True
            # elif math.isnan(test_cell) and math.isnan(truth_cell):
            #     assert True
            else:
                msg = f"Data mismatch\n\nRow = {row_index + 1} : Column = {column_name}\n\nACTUAL: {test_cell}\nEXPECTED: {truth_cell}\n"
                assert False, msg


def _check_row_count(test_df, truth_df):
    test_df_count = test_df.count()
    truth_df_count = truth_df.count()
    assert (
        test_df_count == truth_df_count
    ), f"Number of rows are not same.\n\nActual Rows: {test_df_count}\nExpected Rows: {truth_df_count}\n"


def dfs_equal(
    test_df: pyspark.sql.DataFrame,
    truth_df: pyspark.sql.DataFrame,
    check_dtype: bool = True,
    check_column_names: bool = False,
    check_columns_in_order: bool = False,
    order_by: list = None,
) -> None:
    """
    Used to test if two dataframes are same or not

    Args:
        test_df (pyspark.sql.DataFrame): Dataframe to test
        truth_df (pyspark.sql.DataFrame): Dataframe to expect
        check_dtype (bool, optional): Comapred both dataframe have same column and colum type or not. If using check_dtype then check_column_names is not required. Defaults to True.
        check_column_names (bool, optional): Comapare both dataframes have same column or not. Defaults to False.
        check_columns_in_order (bool, optional): Check columns in order. Defaults to False.
        order_by (list, optional): List of column names if we want to sort dataframe before comparing. Defaults to None.
    """

    # Check if
    _check_isinstance_df(test_df, truth_df)

    # Check Column Names
    if check_column_names:
        _check_columns(check_columns_in_order, test_df, truth_df)

    # Check Column Data Types
    if check_dtype:
        _check_schema(check_columns_in_order, test_df, truth_df)

    # Check number of rows
    _check_row_count(test_df, truth_df)

    # Sort df
    if order_by:
        test_df = test_df.orderBy(order_by)
        truth_df = truth_df.orderBy(order_by)

    # Check dataframe content
    _check_df_content(test_df, truth_df)
