# import streamlit as st
# import time
# import numpy as np
# import pandas as pd
# from src.utils_function.data_loaders import snowflake_client,mssql_client
# from st_aggrid import AgGrid,GridOptionsBuilder,GridUpdateMode
# import streamlit.components.v1 as components
# import pickle
# import joblib
# from raiwidgets import FairnessDashboard
# import threading
# from streamlit.runtime.scriptrunner.script_run_context import add_script_run_ctx

# # st.set_page_config(page_title="Bias_fairness", page_icon="📈")

# def background_dash(bias_data,sensitive_features,target_feature,y_pred):
#     FairnessDashboard(sensitive_features=bias_data[sensitive_features],
#                             y_true=bias_data[target_feature].tolist(),
#                             y_pred=y_pred)

# def load_button_activate():
#     st.session_state["load_data_button"] = True

# def Bias_fairness_render():
#     st.header("Bias and Fairness Assesment Tool")
#     ex_model = st.file_uploader("Choose the Model file",type=['pkl','joblib'],accept_multiple_files=False)
#     data_source = st.radio("Data Source Type:",('Snowflake','MSSQL','CSV/Excel'),horizontal = True)
#     if data_source == 'CSV/Excel':
#         st.warning('**It is against company policy to store the ascend data in your local system.', icon="⚠️")
#         local_file = st.file_uploader("Choose the Data file",type=['csv','xlsx'],accept_multiple_files=False)
#         if local_file and ex_model:
#             try:
#                 try:
#                     model = pickle.loads(ex_model.read())
#                 except:
#                     model = joblib.load(ex_model.read())
#                 if local_file.type == 'text/csv':
#                     bias_data = pd.read_csv(local_file)
#                 elif local_file.type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
#                     bias_data = pd.read_excel(local_file)
#                 fea0,fea1 = st.columns([2,4])
#                 target_feature = fea0.selectbox('Target Feature',bias_data.columns.tolist())
#                 # bias_no_target = bias_data.drop([target_feature]) 
#                 sensitive_features = fea1.multiselect('Sensitive Features',bias_data.columns.tolist())
#                 get_bias_check = st.button('Check Bias and Fairness')
#                 if get_bias_check:
#                     with st.spinner("Building the Bias and Fairness Asessment Dashboard"):
#                         features = model.feature_names_in_.tolist()
#                         y_pred = model.predict(bias_data[features])
#                         # dashboard = FairnessDashboard(
#                         #     sensitive_features=bias_data[sensitive_features],
#                         #     y_true=bias_data[target_feature].tolist(),
#                         #     y_pred=y_pred,
#                         #     # sensitive_feature_names=[sensitive_features],
#                         #     # metric_fns=metrics
#                         # )
#                         t1 = threading.Thread(target=background_dash,args=(bias_data,sensitive_features,target_feature,y_pred))
#                         add_script_run_ctx(t1)
#                         t1.start()
#                         time.sleep(8)
#                         dashboardurl = 'http://localhost:5001/'
#                         components.iframe(dashboardurl, height=1500, scrolling=True)
#             except:
#                 st.error("Please upload the file correctly")
#         else:
#             st.info("Please upload the data file")
#     elif data_source == 'Snowflake': 
#         if 'load_data_button' not in st.session_state:
#                 st.session_state["load_data_button"] = False
#         with st.form('Form1'):
#             sn10,sn11,sn12,sn13 = st.columns(4)
#             warehouse = sn10.text_input("Warehouse")
#             database = sn11.text_input("Database")
#             account = sn12.text_input("Account")
#             role = sn13.text_input("Role")
            
#             sn21,sn22 = st.columns([1.5,4])
#             user_name = sn21.text_input("User_Name")
#             password_key = sn22.file_uploader("Password key",type=['p8'],accept_multiple_files=False)
#             data_query = st.text_input("Snowflake Query")

#             # if warehouse and database and account and role and user_name and password_key and data_query:
#             get_data = st.form_submit_button("Load Data",on_click = load_button_activate)
            
#         if get_data or st.session_state["load_data_button"]:
#             conn = snowflake_client.get_engine(warehouse,database,account,role,user_name,password_key)
#             try:
#                 bias_data = pd.read_sql_query(data_query, conn)
#                 st.info("Data is Loaded Successfully")
#                 fea0,fea1 = st.columns([2,4])
#                 target_feature = fea0.selectbox('Target Feature',bias_data.columns.tolist())
#                 bias_no_target = bias_data.drop([target_feature]) 
#                 sensitive_features = fea1.multiselect('Sensitive Features',bias_data.columns.tolist())
#                 get_bias_check = st.button('Check Bias and Fairness')
#                 if get_bias_check:
#                     with st.spinner("Building the Explainability Dashboard"):
#                         features = model.feature_names_in_.tolist()
#                         y_pred = model.predict(bias_data[features])
#                         # dashboard = FairnessDashboard(
#                         #     sensitive_features=bias_data[sensitive_features],
#                         #     y_true=bias_data[target_feature].tolist(),
#                         #     y_pred=y_pred,
#                         #     # sensitive_feature_names=[sensitive_features],
#                         #     # metric_fns=metrics
#                         # )
#                         t1 = threading.Thread(target=background_dash,args=(bias_data,sensitive_features,target_feature,y_pred))
#                         add_script_run_ctx(t1)
#                         t1.start()
#                         time.sleep(8)
#                         dashboardurl = 'http://localhost:5001/'
#                         components.iframe(dashboardurl, height=1500, scrolling=True)

#             except:
#                 st.error("Please provide the correct details")
#         # else:
#         #     st.info("Please provide all the details")

#     elif data_source == 'MSSQL':
#         if 'load_data_button' not in st.session_state:
#                 st.session_state["load_data_button"] = False
#         with st.form('Form1'):
#             sn10,sn11 = st.columns(2)
#             server = sn10.text_input("Warehouse")
#             database = sn11.text_input("Database")
#             user_name = sn10.text_input("User_Name")
#             password = sn11.text_input("Password")
#             data_query = st.text_input("SQL Query")

#             get_data = st.form_submit_button("Load Data",on_click = load_button_activate)
            
#         if get_data or st.session_state["load_data_button"]:
#             conn = mssql_client.mssql_engine(server, database, user_name, password)
#             try:
#                 bias_data = pd.read_sql_query(data_query, conn)
#                 st.info("Data is Loaded Successfully")
#                 fea0,fea1 = st.columns([2,4])
#                 target_feature = fea0.selectbox('Target Feature',bias_data.columns.tolist())
#                 bias_no_target = bias_data.drop([target_feature]) 
#                 sensitive_features = fea1.multiselect('Sensitive Features',bias_data.columns.tolist())
#                 get_bias_check = st.button('Check Bias and Fairness')
#                 if get_bias_check:
#                     with st.spinner("Building the Explainability Dashboard"):
#                         features = model.feature_names_in_.tolist()
#                         y_pred = model.predict(bias_data[features])
#                         # dashboard = FairnessDashboard(
#                         #     sensitive_features=bias_data[sensitive_features],
#                         #     y_true=bias_data[target_feature].tolist(),
#                         #     y_pred=y_pred,
#                         #     # sensitive_feature_names=[sensitive_features],
#                         #     # metric_fns=metrics
#                         # )
#                         t1 = threading.Thread(target=background_dash,args=(bias_data,sensitive_features,target_feature,y_pred))
#                         add_script_run_ctx(t1)
#                         t1.start()
#                         time.sleep(8)
#                         dashboardurl = 'http://localhost:5001/'
#                         components.iframe(dashboardurl, height=1500, scrolling=True)
#             except:
#                 st.error("Please provide the correct details")
#         # else:
#         #     st.info("Please provide all the details")

#     else:
#         st.info("Please select the data source")
