import streamlit as st
import time
import numpy as np
import pandas as pd
from src.utils_function.data_loaders import snowflake_client,mssql_client
from st_aggrid import AgGrid,GridOptionsBuilder,GridUpdateMode
import streamlit.components.v1 as components
from sdv.tabular import CopulaGAN,TVAE
from sdv.evaluation import evaluate
from table_evaluator import load_data, TableEvaluator


def save_generated_df(df):
   return df.to_csv(index=False).encode('utf-8')

def load_button_activate():
    st.session_state["load_data_button"] = True

def create_grid(df,key=None):
    gb = GridOptionsBuilder.from_dataframe(df,editable=True)
    gb.configure_auto_height(True)
    gb.configure_pagination(paginationPageSize=10,paginationAutoPageSize=False)
    gb.configure_side_bar()
    # gb.configure_selection(selection_mode="multiple", use_checkbox=True)
    # gb.configure_grid_options(onRowSelected = js, pre_selected_rows = []) 
    gb.configure_default_column(groupable=True, value=True, enableRowGroup=False, aggFunc="sum", editable=True,min_column_width=5)
    gridOptions = gb.build()
    if key is not None:
        grid_data = AgGrid(df, gridOptions=gridOptions,key=key, enable_enterprise_modules=True,update_mode=GridUpdateMode.SELECTION_CHANGED)
    else:
        grid_data = AgGrid(df, gridOptions=gridOptions, enable_enterprise_modules=True,update_mode=GridUpdateMode.SELECTION_CHANGED)
    return grid_data

def result_eval(real_data,new_data):
    score = evaluate(real_data,new_data)
    st.write('Similarity score between Real and Generated Data(Score closer to 1 means more Similar)')
    st.write(score)
    tableevaluator = TableEvaluator(real_data, new_data)
    out = tableevaluator.evaluate()
    st.write(out)


def Data_generation_render():
    st.header("Synthetic Data Generation")
    data_source = st.radio("Data Source Type:",('Snowflake','MSSQL','CSV/Excel'),horizontal = True)
    if data_source == 'CSV/Excel':
        st.warning('**It is against company policy to store the ascend data in your local system.', icon="⚠️")
        local_file = st.file_uploader("Choose the Data file",type=['csv','xlsx'],accept_multiple_files=False)
        if local_file:
            try:
                if local_file.type == 'text/csv':
                    real_data = pd.read_csv(local_file)
                elif local_file.type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                    real_data = pd.read_excel(local_file)
                col1,col2 = st.columns(2)
                no_sample = int(col1.number_input('Number of samples'))
                primary_key = col2.selectbox('Primary Key column',(['None']+real_data.columns.tolist()))
                chosen_tech = st.radio('Select the technique to use',('CopulaGAN','TVAE GAN'),horizontal=True)
                col10,col11,col12 = st.columns([2,4,2])
                gen_sample = col10.button('Generate samples')
                if gen_sample:
                    with st.spinner("Generating the Synthetic Data"):
                        if chosen_tech == 'CopulaGAN':
                            if primary_key != 'None':
                                model = CopulaGAN(primary_key=primary_key)
                                model.fit(real_data)
                                new_data = model.sample(no_sample)
                            else:
                                model = CopulaGAN()
                                model.fit(real_data)
                                new_data = model.sample(no_sample)
                        elif chosen_tech == 'TVAE GAN':
                            if primary_key != 'None':
                                model = TVAE(primary_key=primary_key)
                                model.fit(real_data)
                                new_data = model.sample(no_sample)
                            else:
                                model = TVAE()
                                model.fit(real_data)
                                new_data = model.sample(no_sample)
                        create_grid(new_data)
                        new_data_save = col12.download_button('Download Synthetic Data',save_generated_df(new_data),"Synthetic_Data.csv")
                        result_eval(real_data,new_data)            
            except:
                st.error("Please upload the file correctly")
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
                explain_data = pd.read_sql_query(data_query, conn)
                st.info("Data is Loaded Successfully")
                col1,col2 = st.columns(2)
                no_sample = int(col1.number_input('Number of samples'))
                primary_key = int(col2.selectbox('Primary Key column'))
                chosen_tech = st.radio('Select the technique to use',('CopulaGAN','TVAE GAN'),horizontal=True)
                col10,col11,col12 = st.columns([2,4,2])
                gen_sample = col10.button('Generate samples')
                if gen_sample:
                    with st.spinner("Generating the Synthetic Data"):
                        if chosen_tech == 'CopulaGAN':
                            if primary_key != 'None':
                                model = CopulaGAN(primary_key=primary_key)
                                model.fit(real_data)
                                new_data = model.sample(no_sample)
                            else:
                                model = CopulaGAN()
                                model.fit(real_data)
                                new_data = model.sample(no_sample)
                        elif chosen_tech == 'TVAE GAN':
                            if primary_key != 'None':
                                model = TVAE(primary_key=primary_key)
                                model.fit(real_data)
                                new_data = model.sample(no_sample)
                            else:
                                model = TVAE()
                                model.fit(real_data)
                                new_data = model.sample(no_sample)
                        create_grid(new_data)
                        new_data_save = col12.download_button('Download Synthetic Data',save_generated_df(new_data),"Synthetic_Data.csv")
                        result_eval(real_data,new_data)
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
                explain_data = pd.read_sql_query(data_query, conn)
                st.info("Data is Loaded Successfully")
                col1,col2 = st.columns(2)
                no_sample = int(col1.number_input('Number of samples'))
                primary_key = int(col2.selectbox('Primary Key column'))
                chosen_tech = st.radio('Select the technique to use',('CopulaGAN','TVAE GAN'),horizontal=True)
                col10,col11,col12 = st.columns([2,4,2])
                gen_sample = col10.button('Generate samples')
                if gen_sample:
                    with st.spinner("Generating the Synthetic Data"):
                        if chosen_tech == 'CopulaGAN':
                            if primary_key != 'None':
                                model = CopulaGAN(primary_key=primary_key)
                                model.fit(real_data)
                                new_data = model.sample(no_sample)
                            else:
                                model = CopulaGAN()
                                model.fit(real_data)
                                new_data = model.sample(no_sample)
                        elif chosen_tech == 'TVAE GAN':
                            if primary_key != 'None':
                                model = TVAE(primary_key=primary_key)
                                model.fit(real_data)
                                new_data = model.sample(no_sample)
                            else:
                                model = TVAE()
                                model.fit(real_data)
                                new_data = model.sample(no_sample)
                        create_grid(new_data)
                        new_data_save = col12.download_button('Download Synthetic Data',save_generated_df(new_data),"Synthetic_Data.csv")
                        result_eval(real_data,new_data)
            except:
                st.error("Please provide the correct details")
        # else:
        #     st.info("Please provide all the details")

    else:
        st.info("Please select the data source")
