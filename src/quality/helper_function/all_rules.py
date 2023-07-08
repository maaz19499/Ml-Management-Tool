import os
import pandas as pd
import great_expectations as ge
# from utils import *



    # If function
def get_fun(row,data):
        if row.Expectation == 'column_to_exist':
            data = get_col_to_exist(data,row['Source Columns'])
        elif row.Expectation == 'max_to_be_between':
            data = get_col_max_to_be_between(data,row['Source Columns'],row.Lower_limit,row.Upper_limit)
        elif row.Expectation == 'mean_to_be_between':
            data = get_col_mean_to_be_between(data,row['Source Columns'],row.Lower_limit,row.Upper_limit)
        elif row.Expectation == 'median_to_be_between':
            data = get_col_median_to_be_between(data,row['Source Columns'],row.Lower_limit,row.Upper_limit)
        elif row.Expectation == 'min_to_be_between':
            data = get_col_min_to_be_between(data,row['Source Columns'],row.Lower_limit,row.Upper_limit)
        elif row.Expectation == 'quantile_values_to_be_between':
            data = get_col_quantile_values_to_be_between(data,row['Source Columns'],row.Lower_limit,row.Upper_limit)
        elif row.Expectation == 'stdev_to_be_between':
            data = get_col_stdev_to_be_between(data,row['Source Columns'],row.Lower_limit,row.Upper_limit)
        elif row.Expectation == 'sum_to_be_between':
            data = get_col_sum_to_be_between(data,row['Source Columns'],row.Lower_limit,row.Upper_limit)
        elif row.Expectation == 'value_lengths_to_be_between':
            data = get_col_value_lengths_to_be_between(data,row['Source Columns'],row.Lower_limit,row.Upper_limit)
        elif row.Expectation == 'values_to_be_between':
            data = get_col_values_to_be_between(data,row['Source Columns'],row.Lower_limit,row.Upper_limit)
        elif row.Expectation == 'unique_value_count_to_be_between':
            data = get_col_unique_value_count_to_be_between(data,row['Source Columns'],row.Lower_limit,row.Upper_limit)
        elif row.Expectation == 'value_lengths_to_equal':
            data = get_col_value_lengths_to_equal(data,row['Source Columns'],row.Constant)
        elif row.Expectation == 'most_common_value_to_be_in_set':
            data = get_col_most_common_value_to_be_in_set(data,row['Source Columns'],row.Lists)
        elif row.Expectation == 'values_to_be_in_set':
            data = get_col_values_to_be_in_set(data,row['Source Columns'],row.Lists)
        elif row.Expectation == 'values_to_not_be_in_set':
            data = get_col_values_to_not_be_in_set(data,row['Source Columns'],row.Lists)
        elif row.Expectation == 'distinct_values_to_be_in_set':
            data = get_col_distinct_values_to_be_in_set(data,row['Source Columns'],row.Lists)
        elif row.Expectation == 'values_to_be_unique':
            data = get_col_values_to_be_unique(data,row['Source Columns'],row.Constant)
        elif row.Expectation == 'values_to_be_null':
            data = get_col_values_to_be_null(data,row['Source Columns'],row.Constant)
        elif row.Expectation == 'values_to_not_be_null':
            data = get_col_values_to_not_be_null(data,row['Source Columns'],row.Constant)
        elif row.Expectation == 'values_to_be_of_type':
            data = get_col_values_to_be_of_type(data,row['Source Columns'],row.Constant)
        elif row.Expectation == 'values_to_be_in_type_list':
            data = get_col_values_to_be_in_type_list(data,row['Source Columns'],row.Constant)
        return(data)
    
    
    # Great expectation functions
       
def get_col_to_exist(data,col_name):
        data.expect_column_to_exist(col_name)
        return(data)
    
def get_col_max_to_be_between(data,col_name,Lower,Upper):
        data.expect_column_max_to_be_between(col_name,Lower,Upper)
        return(data)
    
def get_col_mean_to_be_between(data, col_name,Lower,Upper):
        data.expect_column_mean_to_be_between(col_name,Lower,Upper)
        return(data)
    
def get_col_median_to_be_between(data, col_name,Lower,Upper):
        data.expect_column_median_to_be_between(col_name,Lower,Upper)
        return(data)
    
def get_col_min_to_be_between(data, col_name,Lower,Upper):
        data.expect_column_min_to_be_between(col_name,Lower,Upper)
        return(data)
    
def get_col_quantile_values_to_be_between(data, col_name,Lower,Upper):
        data.expect_column_quantile_values_to_be_between(col_name,Lower,Upper)
        return(data)
    
def get_col_stdev_to_be_between(data, col_name,Lower,Upper):
        data.expect_column_to_be_between(col_name,Lower,Upper)
        return(data)
    
def get_col_sum_to_be_between(data, col_name,Lower,Upper):
        data.expect_column_sum_to_be_between(col_name,Lower,Upper)
        return(data)
    
def get_col_value_lengths_to_be_between(data, col_name,Lower,Upper):
        data.expect_column_value_lengths_to_be_between(col_name,Lower,Upper)
        return(data)
    
def get_col_values_to_be_between(data, col_name,Lower,Upper):
        data.expect_column_values_to_be_between(col_name,Lower,Upper)
        return(data)
    
def get_col_unique_value_count_to_be_between(data, col_name,Lower,Upper):
        data.expect_column_unique_value_count_to_be_between(col_name,Lower,Upper)
        return(data)
    
def get_col_value_lengths_to_equal(data, col_name,Constant):
        data.expect_column_value_lengths_to_equal(col_name,Constant)
        return(data)
    
def get_col_most_common_value_to_be_in_set(data, col_name,Lists):
        data.expect_column_most_common_value_to_be_in_set(col_name,Lists)
        return(data)
    
def get_col_values_to_be_in_set(data, col_name,Lists):
        data.expect_column_values_to_be_in_set(col_name,Lists)
        return(data)
    
def get_col_values_to_not_be_in_set(data, col_name,Lists):
        data.expect_column_values_to_not_be_in_set(col_name,Lists)
        return(data)
    
def get_col_distinct_values_to_be_in_set(data, col_name,Lists):
        data.expect_column_distinct_values_to_be_in_set(col_name,Lists)
        return(data)
    
def get_col_values_to_be_unique(data, col_name,Constant):
        data.expect_column_values_to_be_unique(col_name,Constant)
        return(data)
    
def get_col_values_to_be_null(data, col_name,Constant):
        data.expect_column_values_to_be_null(col_name,Constant)
        return(data)
    
def get_col_values_to_not_be_null(data, col_name,Constant):
        data.expect_column_values_to_not_be_null(col_name,Constant)
        return(data)
    
def get_col_values_to_be_of_type(data, col_name,Constant):
        data.expect_column_values_to_be_of_type(col_name,Constant)
        return(data)
    
def get_col_values_to_be_in_type_list(data, col_name,Constant):
        data.expect_column_values_to_be_in_type_list(col_name,Constant)
        return(data)