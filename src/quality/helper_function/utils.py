 # Importing the necessary libraries
import os
import pandas as pd
import numpy as np
import great_expectations as ge
import pandas as pd
from great_expectations.render.renderer import (
    ValidationResultsPageRenderer,
    ExpectationSuitePageRenderer,
)
from great_expectations.render.view import DefaultJinjaPageView
import re
from src.quality.helper_function.rules import get_fun
import datetime as dt
# 
 
 # Converting the Great Expectation Validating Result into HTML format
def render_html(data):
        result = data.validate()
        print(result)
        document_model = ValidationResultsPageRenderer().render(result)
        report = DefaultJinjaPageView().render(document_model)
        report = re.sub('\n', '',report)
     
        return(report)
    
    # Checking whether the data is from CSV or SQL 
# def load_data(data_source_dict,user_id,user_password):
#         if data_source_dict['Source Format'] == 'CSV': 
#             source_data, target_data= csv_data(data_source_dict)    
#         elif data_source_dict['Source Format'] == 'MSSQL':    
#             source_data, target_data = sql_data(data_source_dict,user_id,user_password)
#         elif data_source_dict['Source Format'] == 'SNOWFLAKE':
#             source_data, target_data = snowfalke_data(data_source_dict,user_id,user_password)
#         else:
#             source_data, target_data = pd.DataFrame(), pd.DataFrame()
#         return(source_data, target_data)
    
    # Reading the Configuration File
def get_data_source_config(config_path):
        is_config_exist= os.path.exists(config_path)
        if is_config_exist:
            xls = pd.ExcelFile(config_path)
            try:
                data_source = pd.read_excel(xls, 'data_source_settings')
            except:
                raise FileExistsError('Configuration file does not have data_source_settings worksheet')
            # Converting into dictionary format    
            config = dict(zip(data_source.Header, data_source.Value))
            return(config)
        else:
            raise FileExistsError('Configuration file is missing. It should be available in the same location where this notebook is placed')
    
    # Validating the Schema
def validate_schema(self):
        pass


    
    # Function to save the html report in the report folder
def save_html_report(report,path):
        path_split = os.path.splitext(path)
        if path_split[1] !='.html':
            ext='.html'
            path =path_split[0]+'/'+ext
        with open(path, "w",encoding= 'utf8') as file:
            file.write(report)

    # Reading the rules from the config file
def get_rules_config(config_path):
        is_config_exist= os.path.exists(config_path)
        if is_config_exist:
            xls = pd.ExcelFile(config_path)
            try:
                rules = pd.read_excel(xls, 'schema_settings')
            except:
                raise FileExistsError('Configuration file does not have schema_settings worksheet')
            return(rules)
        else:
            raise FileExistsError('Configuration file is missing. It should be available in the same location where this notebook is placed')
     
# Specifying the Output Directory or Report Directory
def output_dir(data_config,config_file_path):
        report_dir = data_config.get('out_dir', np.nan)
        if np.isnan(report_dir):
            script_path = os.path.realpath(__file__)
            helper_dir = os.path.dirname(script_path)
            script_dir = os.path.dirname(helper_dir)
            report_dir = os.path.join(script_dir,'report')
            if not os.path.exists(report_dir):
                os.mkdir(report_dir)
            print('Since Output directory is not provided it is saved in location :' +report_dir)
        return(report_dir)

# Report Generating Function
def generate_ge_report(data, rules):
        int_lst = ['int','int32','int64','integer']
        float_lst = ['float','float32','float64']
        string_lst = ['object','object_']
        for index,row in rules.iterrows():
            if (isinstance(row.Lists,str)):
                row.Lists = row.Lists.split(',')
            # int_list = ['int','int32','int64','integer']
            elif row.Constant == 'integer':
                if data.dtypes[row['Source Columns']] not in int_lst:
                    col = row['Source Columns']
                    raise ValueError(f'The data type of the column {col} is not integer')
                elif data.dtypes[row['Source Columns']] in int_lst:
                    row.Constant = str(data.dtypes[row['Source Columns']])    
            elif row.Constant == 'float':
                if data.dtypes[row['Source Columns']] not in float_lst:
                    col = row['Source Columns']
                    raise ValueError(f'The data type of the column {col} is not integer')
                elif data.dtypes[row['Source Columns']] in float_lst:
                    row.Constant = str(data.dtypes[row['Source Columns']])     
            elif row.Constant == 'datetime':
                row.Constant = 'datetime64' 
                data[row['Source Columns']] = pd.to_datetime(data[row['Source Columns']])  
            elif row.Constant == 'date':
                row.Constant = 'datetime64'
                data[row['Source Columns']] = pd.to_datetime(data[row['Source Columns']])
            elif row.Constant == 'time':
                row.Constant = 'datetime64'
                data[row['Source Columns']] = pd.to_datetime(data[row['Source Columns']])
            elif row.Constant == 'string':
                if data.dtypes[row['Source Columns']] not in string_lst:
                    col = row['Source Columns']
                    raise ValueError(f'The data type of the column {col} is not integer')
                elif data.dtypes[row['Source Columns']] in string_lst:
                    row.Constant = str(data.dtypes[row['Source Columns']])  
            data = get_fun(row=row, data=data)    
        report = render_html(data=data)
        return(report)
    
    
# Concerting the Pandas Profilling Report into HTML format 
# def generate_profile_report(data):
#         profile = ProfileReport(data, html={'style': {'full_width': True}}, sort=None)
#         pro_html = profile.to_html()
#         return(pro_html)


        