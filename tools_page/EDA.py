import streamlit as st
import time
import numpy as np
import pandas as pd
from src.utils_function.data_loaders import snowflake_client,mssql_client
from st_aggrid import AgGrid,GridOptionsBuilder,GridUpdateMode
import streamlit.components.v1 as components
from pandas_profiling import ProfileReport
import sweetviz as sv
# from dataprep.eda import create_report

# st.set_page_config(page_title="AutoML", page_icon="📈")

# progress_bar = st.sidebar.progress(0)

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


def sweetvi_comp(first_data,second_data,target_feature):
    re_col0,re_col1,re_col2 = st.columns([2,4,2])
    generate_report = re_col0.button('Generate Report')
    if generate_report:
        with st.spinner('Loading,Please wait...'):
            sweet_report = sv.compare([first_data, "First Data"], [second_data, "Second Data"],target_feature)
            report = sweet_report.show_html(filepath='src/eda/reports/sweetviz_report.html', open_browser=False, layout='vertical', scale=1.0)
            HtmlFile = open("src/eda/reports/sweetviz_report.html", 'r', encoding='utf-8')
            source_code = HtmlFile.read() 
            components.html(source_code, width=None, height=1200, scrolling=True)
            # # sweet_report = sweet_report.
            # components.html(sweet_report.show_notebook(),height = 1200,width=None,scrolling=True)
            # st.markdown(profile_report,unsafe_allow_html=True)
            generate_report_save = re_col2.download_button('Download the Report',source_code,"EDA report.html")

def report_generate(data):
    re_col0,re_col1,re_col2 = st.columns([2,4,2])
    generate_report = re_col0.button('Generate Report')
    if generate_report:
        with st.spinner('Loading,Please wait...'):
            if data.shape[0] < 15000:
                profile = ProfileReport(data, html={'style': {'full_width': True}}, sort=None)
                report = profile.to_html()
                components.html(report,height = 1200,width=None,scrolling=True)
                # generate_report_save = re_col2.download_button('Download the Report',report,"EDA report.html")
            else:
                sweet_report = sv.analyze(data)
                sw_report = sweet_report.show_html(filepath='src/eda/reports/sweetviz_report.html', open_browser=False, layout='vertical', scale=1.0)
                HtmlFile = open("src/eda/reports/sweetviz_report.html", 'r', encoding='utf-8')
                report = HtmlFile.read() 
                components.html(report, width=None, height=1200, scrolling=True)
            generate_report_save = re_col2.download_button('Download the Report',report,"EDA report.html")
            # st.markdown(profile_report,unsafe_allow_html=True)

def load_button_activate():
    st.session_state["load_data_button"] = True
            

def EDA_render():
    st.header("EDA Tool")
    st.info('We have a paid setup in dai, you can visit: https://steam.h2o.ascendlearning.com/oidc-login/')
    data_no = st.radio('Number of Datasets',('One Datasets','Two Datasets'),horizontal=True)
    if data_no == 'One Datasets':
        data_source = st.radio("Data Source Type:",('Snowflake','MSSQL','CSV/Excel'),horizontal = True)
        if data_source == 'CSV/Excel':
            st.warning('**It is against company policy to store the ascend data in your local system.', icon="⚠️")
            local_file = st.file_uploader("Choose a Data file",type=['csv','xlsx'],accept_multiple_files=False)
            if local_file is not None:
                try:
                    if local_file.type == 'text/csv':
                        eda_data = pd.read_csv(local_file)
                    elif local_file.type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                        eda_data = pd.read_excel(local_file)
                    st.info("Data is Loaded Successfully")
                    create_grid(eda_data)
                    report_generate(eda_data)
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

                get_data = st.form_submit_button("Load Data",on_click = load_button_activate)
            
            if get_data or st.session_state["load_data_button"]:
                conn = snowflake_client.get_engine(warehouse,database,account,role,user_name,password_key)
                try:
                    with st.spinner('Loading,Please wait...'):
                        eda_data = pd.read_sql_query(data_query, conn)
                        st.info("Data is Loaded Successfully")
                        create_grid(eda_data)
                        report_generate(eda_data) 
                except:
                    st.error("Please provide the correct details")
            # if eda_data:
                
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
                    with st.spinner('Loading,Please wait...'):
                        eda_data = pd.read_sql_query(data_query, conn)
                        st.info("Data is Loaded Successfully")
                        create_grid(eda_data)
                        report_generate(eda_data)
                except:
                    st.error("Please provide the correct details")
            # else:
            #     st.info("Please provide all the details")

        else:
            st.info("Please select the data source")

    elif data_no == 'Two Datasets':
        data_source = st.radio("Data Source Type:",('Snowflake','MSSQL','CSV/Excel'),horizontal = True)
        if data_source == 'CSV/Excel':
            st.warning('**It is against company policy to store the ascend data in your local system.', icon="⚠️")
            sv0,sv1 = st.columns(2)
            First_file = sv0.file_uploader("Choose a First Data file",type=['csv','xlsx'],accept_multiple_files=False)
            Second_file = sv1.file_uploader("Choose a Second Data file",type=['csv','xlsx'],accept_multiple_files=False)
            if First_file and  Second_file:
                try:
                    if First_file.type == 'text/csv':
                        first_data = pd.read_csv(First_file)
                    elif First_file.type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                        first_data = pd.read_excel(First_file)
                    if Second_file.type == 'text/csv':
                        second_data = pd.read_csv(Second_file)
                    elif Second_file.type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                        second_data = pd.read_excel(Second_file)
                    st.info("Data is Loaded Successfully")
                    target_feature = st.selectbox('Select the target feature if present',(first_data.columns.tolist()))
                    st.subheader('Data Preview')
                    st.write('First Data')
                    create_grid(first_data,key = 'First')
                    st.write('Second data')
                    create_grid(second_data,key='Second')
                    sweetvi_comp(first_data,second_data,target_feature)
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
                sn31,sn32 = st.columns(2)
                first_data_query = sn31.text_input("Snowflake Query for first dataset")
                second_data_query = sn32.text_input("Snowflake Query for Second dataset")
                # target_feature = st.selectbox('Select the target feature if present',(first_data.columns.tolist()))

                get_data = st.form_submit_button("Load Data",on_click = load_button_activate)
            
            if get_data or st.session_state["load_data_button"]:
                    conn = snowflake_client.get_engine(warehouse,database,account,role,user_name,password_key)
                    try:
                        first_data = pd.read_sql_query(first_data_query, conn)
                        second_data = pd.read_sql_query(second_data_query, conn)
                        st.info("Data is Loaded Successfully")
                        target_feature = st.selectbox('Select the target feature if present',(first_data.columns.tolist()))
                        st.subheader('Data Preview')
                        st.write('First Data')
                        create_grid(first_data,key = 'First')
                        st.write('Second data')
                        create_grid(second_data,key='Second')
                        sweetvi_comp(first_data,second_data,target_feature)
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
                first_data_query = sn10.text_input("SQL Query for first dataset")
                second_data_query = sn11.text_input("SQL Query for second dataset")
                # target_feature = st.selectbox('Select the target feature if present',(first_data.columns.tolist()))

                get_data = st.form_submit_button("Load Data",on_click = load_button_activate)
            
            if get_data or st.session_state["load_data_button"]:
                    conn = mssql_client.mssql_engine(server, database, user_name, password)
                    try:
                        first_data = pd.read_sql_query(first_data_query, conn)
                        second_data = pd.read_sql_query(second_data_query, conn)
                        st.info("Data is Loaded Successfully")
                        target_feature = st.selectbox('Select the target feature if present',(first_data.columns.tolist()))
                        st.subheader('Data Preview')
                        st.write('First Data')
                        create_grid(first_data,key = 'First')
                        st.write('Second data')
                        create_grid(second_data,key='Second')
                        sweetvi_comp(first_data,second_data,target_feature)
                    except:
                        st.error("Please provide the correct details")
            # else:
            #     st.info("Please provide all the details")

        else:
            st.info("Please select the data source")
