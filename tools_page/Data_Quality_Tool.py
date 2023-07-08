import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import time
import yaml
import json
import numpy as np
import great_expectations as ge
from st_aggrid import AgGrid,GridOptionsBuilder,GridUpdateMode
from pandas.api.types import is_bool_dtype, is_numeric_dtype
# from src.quality.helper_function.rules import *
from src.quality.helper_function.utils import *
from src.utils_function.data_loaders import snowflake_client,mssql_client


# st.set_page_config(page_title="Quality Tool", page_icon="📈",layout="wide")





if "rules_df" in st.session_state:
    del st.session_state["rules_df"]

if "grid" in st.session_state:
    del st.session_state["grid"]

# if "load_data_button" in st.session_state:
#     del st.session_state["load_data_button"]


def Quality_render():
    st.header("Data Quality Tool")
    data_source = st.radio("Data Source Type:",('Snowflake','MSSQL','CSV/Excel'),horizontal = True)
    if data_source == 'CSV/Excel':
        st.warning('**It is against company policy to store the ascend data in your local system.', icon="⚠️")
        local_file = st.file_uploader("Choose a Data file",type=['csv','xlsx'],accept_multiple_files=False)
        if local_file is not None:
            # print(local_file.type)
            # try:
                if local_file.type == 'text/csv':
                    quality_data = pd.read_csv(local_file)
                elif local_file.type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                    quality_data = pd.read_excel(local_file)
                st.info("Data is Loaded Successfully")
                config_file = {"Datafile_path":local_file,"Datafile_Type":data_source}
                print(config_file)
                create_rules(quality_data,config_file)
            # except:
            #     st.error("Please upload the file correctly")
        else:
            st.info("Please upload the data file")
    elif data_source == 'Snowflake':
        if 'load_data_button' not in st.session_state:
                st.session_state["load_data_button"] = False
        with st.form('Form1'):
            sn10,sn11,sn12,sn13 = st.columns(4)
            warehouse = sn10.text_input("Warehouse")
            database = sn11.text_input("Database")
            account = sn12.text_input("Account")
            role = sn13.text_input("Role")
            
            sn21,sn22 = st.columns([1.5,4])
            user_name = sn21.text_input("User_Name")
            password_key = sn22.file_uploader("Password key",type=['p8'],accept_multiple_files=False)
            data_query = st.text_input("Snowflake Query")
            # if warehouse and database and account and role and user_name and password_key and data_query:
            get_data = st.form_submit_button("Load Data",on_click = load_button_activate)
            
        if get_data or st.session_state["load_data_button"]:
            conn = snowflake_client.get_engine(warehouse,database,account,role,user_name,password_key)
            try:
                quality_data = pd.read_sql_query(data_query, conn)
                st.info("Data is Loaded Successfully")
                config_file = {"Datafile_Type":data_source,"Warehouse":warehouse,"Database":database,"Account":account,"Role":role,"Query":data_query}
                create_rules(quality_data,config_file)
            except:
                st.error("Please provide the correct details")
        # else:
        #     st.info("Please provide all the details")

    elif data_source == 'MSSQL':
        if 'load_data_button' not in st.session_state:
                st.session_state["load_data_button"] = False
        with st.form('Form1'):
            sn10,sn11 = st.columns(2)
            server = sn10.text_input("Warehouse")
            database = sn11.text_input("Database")
            user_name = sn10.text_input("User_Name")
            password = sn11.text_input("Password")
            data_query = st.text_input("SQL Query")

            get_data = st.form_submit_button("Load Data",on_click = load_button_activate)
            
        if get_data or st.session_state["load_data_button"]:
            conn = mssql_client.mssql_engine(server, database, user_name, password)
            try:
                quality_data = pd.read_sql_query(data_query, conn)
                st.info("Data is Loaded Successfully")
                config_file = {"Datafile_Type":data_source,"Server":server,"Database":database,"Query":data_query}
                create_rules(quality_data,config_file)
            except:
                st.error("Please provide the correct details")
        # else:
        #     st.info("Please provide all the details")

    else:
        st.info("Please select the data source")

def load_button_activate():
    st.session_state["load_data_button"] = True


def get_blank_from_dtype(dtype):
    """Return correct values for the new line: 0 if column is numeric, "" if column is object, ..."""
    if is_numeric_dtype(dtype):
        return 0
    elif is_bool_dtype(dtype):
        return False
    else:
        return ""

def add_row_data(df):
    df = df.append(
        pd.Series(
            [
                get_blank_from_dtype(dtype)
                for dtype in df.dtypes
            ],
            index=df.columns,
        ),
        ignore_index=True,
    )
    return df


def delete_row_data(df, grid):
    if grid['selected_rows']:
        rows_to_delete = pd.DataFrame(grid['selected_rows'])
        if "rowIndex" in rows_to_delete:
            rows_to_delete = rows_to_delete.drop(['rowIndex'],axis=1)
            ds1 = set(map(tuple, df.values))
            ds2 = set(map(tuple, rows_to_delete.values))
            new_rules_df = pd.DataFrame(list(ds1.difference(ds2)),columns = df.columns)
        else:
            ds1 = set(map(tuple,df.values))
            ds2 = set(map(tuple, rows_to_delete.values))
            new_rules_df = pd.DataFrame(list(ds1.difference(ds2)),columns = df.columns)
    return new_rules_df

def save_rules_df(df):
   return df.to_csv(index=False).encode('utf-8')

def create_grid(df):
    gb = GridOptionsBuilder.from_dataframe(df,editable=True)
    gb.configure_auto_height(True)
    gb.configure_pagination(paginationPageSize=10,paginationAutoPageSize=True)
    gb.configure_side_bar()
    gb.configure_selection(selection_mode="multiple", use_checkbox=True)
    # gb.configure_grid_options(onRowSelected = js, pre_selected_rows = []) 
    gb.configure_default_column(groupable=True, value=True, enableRowGroup=False, aggFunc="sum", editable=True,min_column_width=5)
    gridOptions = gb.build()
    grid_data = AgGrid(df, gridOptions=gridOptions, enable_enterprise_modules=True,update_mode=GridUpdateMode.SELECTION_CHANGED)

    return grid_data

def on_delete():
    try:
        st.session_state.rules_df = delete_row_data(st.session_state.rules_df, st.session_state.grid)
    except:
        st.error("Please select the rows to delete")

def upload_rules():
    rules_file = st.file_uploader("Please upload the rules files",type=['csv'],accept_multiple_files=False)
    if rules_file:
        uploaded_rules = pd.read_csv(rules_file)
        st.session_state.rules_df = uploaded_rules

def save_config_rules(config,rules):
    with pd.ExcelWriter("Quality Rules.xlsx") as writer:
        config.to_excel(writer, sheet_name="Config", index=False)
        rules.to_excel(writer, sheet_name="quality_rules", index=False)
    return writer

def create_rules(data,config_file):
            
    rules_lst = ["column_to_exist","max_to_be_between","mean_to_be_between","median_to_be_between","min_to_be_between"
                        ,"quantile_values_to_be_between","stdev_to_be_between","sum_to_be_between","value_lengths_to_be_between","values_to_be_between"
                        ,"unique_value_count_to_be_between","value_lengths_to_equal","most_common_value_to_be_in_set","values_to_be_in_set","values_to_not_be_in_set"
                        ,"distinct_values_to_be_in_set","values_to_be_unique","values_to_be_null","values_to_not_be_null","values_to_be_of_type","values_to_be_in_type_list"]

    lowup_rule_lst = ["max_to_be_between","mean_to_be_between","median_to_be_between","min_to_be_between"
                    ,"quantile_values_to_be_between","stdev_to_be_between","sum_to_be_between","value_lengths_to_be_between","values_to_be_between"
                    ,"unique_value_count_to_be_between"]
    
    Const_rule_lst = ["column_to_exist","value_lengths_to_equal","values_to_be_unique","values_to_be_null","values_to_not_be_null","values_to_be_of_type","values_to_be_in_type_list"]

    List_rule_lst = ["most_common_value_to_be_in_set","values_to_be_in_set","values_to_not_be_in_set","distinct_values_to_be_in_set"]
    
            
    if "rules_df" not in st.session_state:
        st.session_state.rules_df = pd.DataFrame(columns=['Source Columns', 'Expectation', 'Lower_limit', 'Upper_limit', 'Constant', 'Lists'])

    st.subheader("Add Rules")
    col1, col2, col3, col4= st.columns([3,4,2,2])
    # idx= col0.text_input('Idx')
    Source_Columns = col1.selectbox('Col_Name',(data.columns))
    Expectation = col2.selectbox('Rule',(rules_lst) )
    if Expectation in lowup_rule_lst:
        Lower_limit = int(col3.number_input('Lower_limit'))
        Upper_limit = int(col4.number_input('Upper_limit'))
        Constant = " "
        Lists = " "
    elif Expectation in Const_rule_lst:
        true_false_list = ["column_to_exist","values_to_be_unique","values_to_be_null","values_to_not_be_null"]
        if Expectation in true_false_list:
            Lower_limit = " "
            Upper_limit = " "
            Constant = col3.selectbox('Constant',('True','False'))
            Lists = " "
        else:
            Lower_limit = " "
            Upper_limit = " "
            Constant = col3.text_input('Constant')
            Lists = " "

    elif Expectation in List_rule_lst:
        Lower_limit = " "
        Upper_limit = " "
        Constant = " "
        Lists = col3.text_input('List')

    b_cols0, b_cols1,b_cols3,b_cols4 = st.columns([0.8,1,4,1])
    add_row = b_cols0.button('➕ Add row')
    delete_row = b_cols1.button('➖ Delete row',on_click=on_delete)
    upload_rules_button = b_cols3.file_uploader("Upload", type="csv",accept_multiple_files=False,label_visibility='collapsed')
    
    df_new = pd.DataFrame([[ Source_Columns,Expectation,Lower_limit,Upper_limit, Constant,Lists]],
                columns=['Source Columns', 'Expectation', 'Lower_limit', 'Upper_limit', 'Constant', 'Lists'])

    if upload_rules_button:
        uploaded_rules= pd.read_csv(upload_rules_button)
        st.session_state.rules_df = uploaded_rules
        # os.remove(upload_rules_button)

    if add_row:
        st.session_state.rules_df = pd.concat([st.session_state.rules_df, df_new], axis=0)
    st.session_state.grid = create_grid(st.session_state.rules_df)
    b_cols4.download_button('Download Rules',save_rules_df(st.session_state.rules_df),"Quality Rules.csv")
    

    # df_rules = st.session_state.rules_df

    # if df_rules is not None:
    # config_data = pd.DataFrame.from_dict(config_file)#columns=['Credentials'])
    # print(config_data)
        # b_cols4.download_button('Save the Rules',save_config_rules(config_data,df_rules),"Quality Rules.xlsx")
    
    df_rules = st.session_state.rules_df
    if df_rules is not None:
        # df_rules['Lower_limit'] = pd.to_numeric(data["column_name"]
        report(data,df_rules)
    else:
        st.info("Please check the rules")  
    return

def report(data,df_rules):
    re_col0,re_col1,re_col2 = st.columns([2,4,2])
    generate_report = re_col0.button('Generate Report')
    if generate_report:
        df_rules['Lower_limit'] = pd.to_numeric(df_rules['Lower_limit'],errors='coerce')
        df_rules['Upper_limit'] = pd.to_numeric(df_rules['Upper_limit'],errors='coerce')
        ge_data = ge.dataset.PandasDataset(data)
        report = generate_ge_report(data= ge_data, rules=df_rules)
        generate_report_save = re_col2.download_button('Download the Report',report,"Quality report.html")
        components.html(report,height= 1200,width=None,scrolling=True)



        
            
            





