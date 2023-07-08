import streamlit as st
import time
import numpy as np
import pandas as pd
from src.utils_function.data_loaders import snowflake_client,mssql_client
from st_aggrid import AgGrid,GridOptionsBuilder,GridUpdateMode
import streamlit.components.v1 as components
from pandas_profiling import ProfileReport
from src.utils_function.utils import *
from src.automl import automl_app
from sklearn.metrics import ConfusionMatrixDisplay, RocCurveDisplay
import joblib
import pickle
from tools_page import Explainability
# import dataframe_image as dfi


# st.set_page_config(page_title="AutoML", page_icon="📈")

# progress_bar = st.sidebar.progress(0)

# def create_auto_doc():
#     dfi.export(df, 'src/automl/report/space_df.png')
#     auto_dict = {
#         'Data Source' : data_source,
#         'Train filename' : Train_file.filename,
#         'Train filepath' : Train_file,
#         'Test filename' : Test_file.filename,
#         'Test filepath' : Test_file,
#         'Input columns' : imput_var,
#         'Target column' : target_var,
#         'Class Label' : class_label,
#         'Scoring Method' : scoring_method,
#         'Score on' : score_on,
#         'Classifier Selected' : selected_model,
#         'Maximum Trails'  : max_trails,

#         'g'

#     }
st.set_option('deprecation.showPyplotGlobalUse', False)
def create_grid(df,reload_data):
    gb = GridOptionsBuilder.from_dataframe(df,editable=True)
    gb.configure_auto_height(True)
    gb.configure_pagination(paginationPageSize=10,paginationAutoPageSize=False)
    gb.configure_side_bar()
    # gb.configure_selection(selection_mode="multiple", use_checkbox=True)
    # gb.configure_grid_options(onRowSelected = js, pre_selected_rows = []) 
    gb.configure_default_column(groupable=True, value=True, enableRowGroup=False, aggFunc="sum", editable=True,min_column_width=5)
    gridOptions = gb.build()
    grid_data = AgGrid(df, gridOptions=gridOptions,reload_data=reload_data, enable_enterprise_modules=True,update_mode=GridUpdateMode.VALUE_CHANGED)
    return grid_data

def report(data):
    re_col0,re_col1,re_col2 = st.columns([2,4,2])
    generate_report = re_col0.button('Generate Report')
    if generate_report:
        with st.spinner('Loading,Please wait...'):
            profile = ProfileReport(data, html={'style': {'full_width': True}}, sort=None)
            profile_report = profile.to_html()
            components.html(profile_report,height = 1200,width=800,scrolling=True)
            # st.markdown(profile_report,unsafe_allow_html=True)
            generate_report_save = re_col2.download_button('Download the Report',profile_report,"EDA report.html")

def load_button_activate():
    st.session_state["load_data_button"] = True

def AutoML_render():
    st.header("AutoML Tool")
    st.info('We have a paid setup in dai, you can visit: https://steam.h2o.ascendlearning.com/oidc-login/')
    data_source = st.radio("Data Source Type:",('Snowflake','MSSQL','CSV/Excel'),horizontal = True)

    if data_source == 'CSV/Excel':
        st.warning('**It is against company policy to store the ascend data in your local system.', icon="⚠️")
        csv0,csv1 = st.columns(2)
        Train_file = csv0.file_uploader("Choose Train file",type=['csv','xlsx'],accept_multiple_files=False)
        Test_file = csv1.file_uploader("Choose Test file",type=['csv','xlsx'],accept_multiple_files=False)
        if Train_file and Test_file:
                    if Train_file.type == 'text/csv':
                        Train_data = pd.read_csv(Train_file)
                    elif Train_file.type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                        Train_data = pd.read_excel(Train_file)
                    if Test_file.type == 'text/csv':
                        Test_data = pd.read_csv(Test_file)
                    elif Test_file.type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                        Test_data = pd.read_excel(Test_file)
                    st.info("Data is Loaded Successfully")
                    columns = Train_data.columns.tolist()
                    var0,var1 = st.columns([5,2])
                    input_var = var0.multiselect("Input Features",(columns))
                    target_var = var1.selectbox("Target Column",(columns))
                    # print(input_var)
                    if input_var and target_var:
                        if Train_data[target_var].nunique() == 2: 
                            var10,var11,var12 = st.columns(3)
                            class_label = var10.selectbox("Class Label",(Train_data[target_var].unique().tolist()))
                            scoring_method =var11.selectbox("Scoring Method",('Accuracy','F1 Score','Recall','Precision'))
                            score_on = var12.selectbox("Score on",("Train","Test"))
                            selected_model = st.selectbox("Select the Model",('XG Boost','Random Forest','Gradient Boosting','LightGBM'))
                            max_trails = st.slider("Max Trails to perform",min_value=2,max_value=5000,step=10)
                            if selected_model == "XG Boost":
                                with open('src/automl/config/default_xgbparams.yaml', 'r') as xg_file:
                                    default_space = pd.DataFrame(yaml.safe_load(xg_file)).T.reset_index(drop=False).rename(columns={'index':'Param'})
                                    # print(default_space)
                            elif selected_model == "Random Forest":
                                with open('src/automl/config/default_rfparams.yaml', 'r') as rf_file:
                                    default_space = pd.DataFrame(yaml.safe_load(rf_file)).T.reset_index(drop=False).rename(columns={'index':'Param'})
                            elif selected_model == "LightGBM":
                                with open('src/automl/config/default_lgbmparams.yaml', 'r') as rf_file:
                                    default_space = pd.DataFrame(yaml.safe_load(rf_file)).T.reset_index(drop=False).rename(columns={'index':'Param'})
                            elif selected_model == "Gradient Boosting":
                                with open('src/automl/config/default_gbparams.yaml', 'r') as rf_file:
                                    default_space = pd.DataFrame(yaml.safe_load(rf_file)).T.reset_index(drop=False).rename(columns={'index':'Param'})
                                        # print(default_space)
                            reload_data = False
                            res1,res2 = st.columns([5,1.5])
                            reset = res2.button('Reset the table')
                            if reset:
                                grid_change = default_space.copy()
                                reload_data = True
                                grid_change = create_grid(grid_change,reload_data)['data']
                                reload_data = False
                            else:
                                grid_change = create_grid(default_space,reload_data = False)['data']
                            mod0,mod1,mod2,mod3= st.columns([4,5,4,4])
                            model_bestparams = mod0.button("Run Model")
                            if model_bestparams:
                                with st.spinner("Building the model and artifacts"):
                                    d = automl_app.AutoMLApp(target_col=target_var,input_cols=input_var,train=Train_data,test=Test_data
                                            ,maxiter=max_trails,class_label=class_label,score = scoring_method,score_to_calc_on=score_on)
                                    if grid_change is not None:
                                        # st.write("grid_change")
                                        model,best_params = d.run_optim(config = grid_change,algo_name=selected_model)
                                    else:
                                        # st.write("default_space")
                                        model,best_params = d.run_optim(config = default_space,algo_name= selected_model)
                                    # arti_down = mod2.download_button('Download Model',joblib.dump(model),filename = f'{selected_model}_automl.joblib')
                                    if model:
                                        st.write('Best Param:',best_params)
                                        st.header("Train Metrics")
                                        tr_cm,tr_acc,tr_f1,tr_clf_report,tr_roc_score = performance(model=model,X=Train_data[input_var],Y=Train_data[target_var])
                                        st.write('Accuracy: ',tr_acc)
                                        st.write('F1 Score: ',tr_f1)
                                        st.write('Roc_Score: ',tr_roc_score)
                                        st.write('Classification Report:')
                                        st.code(tr_clf_report)
                                        st.subheader("Confusion Matrix") 
                                        ConfusionMatrixDisplay.from_estimator(model,Train_data[input_var],Train_data[target_var], display_labels=Train_data[target_var].unique())
                                        st.pyplot()
                                        st.subheader("ROC Curve") 
                                        RocCurveDisplay.from_estimator(model,Train_data[input_var],Train_data[target_var])
                                        st.pyplot()
                                        st.header("Test Metrics")
                                        ts_cm,ts_acc,ts_f1,ts_clf_report,ts_roc_score = performance(model=model,X=Test_data[input_var],Y=Test_data[target_var])
                                        st.write('Accuracy: ',ts_acc)
                                        st.write('F1 Score: ',ts_f1)
                                        st.write('Roc_Score: ',ts_roc_score)
                                        st.write('Classification Report: ')
                                        st.code(ts_clf_report)
                                        st.subheader("Confusion Matrix") 
                                        ConfusionMatrixDisplay.from_estimator(model,Test_data[input_var],Test_data[target_var], display_labels=Test_data[target_var].unique())
                                        st.pyplot()
                                        st.subheader("ROC Curve") 
                                        RocCurveDisplay.from_estimator(model,Test_data[input_var],Test_data[target_var])
                                        st.pyplot()
                                        # arti_down = mod3.download_button('download Model')
                                        arti_down = mod3.download_button('Download Model',data=pickle.dumps(model),file_name=f'{selected_model}_automl.pkl')
                                        # go_to_explain = mod2.button('Get Explanability')
                                        # if go_to_explain:
                                        #     if "automl_model" not in st.session_state:
                                        #         st.session_state.automl_model = model
                                        #     else:
                                        #         st.session_state.automl_model = model
                                        #     st.session_state.automl_data = Train_data
                                        #     Explanability.Explain_render(model= st.session_state.automl_model,data= st.session_state.automl_data)
                                        
                        else:
                            st.error("This only supports for Binary Classification")
                        

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
            sn30,sn31 = st.columns(2)
            Train_data_query = sn30.text_input("Snowflake Train Query")
            Test_data_query = sn31.text_input("Snowflake Test Query")

            # if warehouse and database and account and role and user_name and password_key and data_query:
            get_data = st.form_submit_button("Load Data",on_click = load_button_activate)
            
        if get_data or st.session_state["load_data_button"]:
            conn = snowflake_client.get_engine(warehouse,database,account,role,user_name,password_key)
            try:
                Train_data = pd.read_sql_query(Train_data_query, conn)
                Test_data = pd.read_sql_query(Test_data_query, conn)
                st.info("Data is Loaded Successfully")
                conn.close()
                columns = Train_data.columns.tolist()
                var0,var1 = st.columns([5,2])
                input_var = var0.multiselect("Input Features",(columns))
                target_var = var1.selectbox("Target Column",(columns))
                # print(input_var)
                if input_var and target_var:
                    if Train_data[target_var].nunique() == 2: 
                        var10,var11,var12 = st.columns(3)
                        class_label = var10.selectbox("Class Label",(Train_data[target_var].unique().tolist()))
                        scoring_method =var11.selectbox("Scoring Method",('Accuracy','F1 Score','Recall','Precision'))
                        score_on = var12.selectbox("Score on",("Train","Test"))
                        selected_model = st.selectbox("Select the Model",('XG Boost','Random Forest','Gradient Boosting','LightGBM'))
                        max_trails = st.slider("Max Trails to perform",min_value=2,max_value=5000,step=10)
                        if selected_model == "XG Boost":
                            with open('src/automl/config/default_xgbparams.yaml', 'r') as xg_file:
                                default_space = pd.DataFrame(yaml.safe_load(xg_file)).T.reset_index(drop=False).rename(columns={'index':'Param'})
                                # print(default_space)
                        elif selected_model == "Random Forest":
                            with open('src/automl/config/default_rfparams.yaml', 'r') as rf_file:
                                default_space = pd.DataFrame(yaml.safe_load(rf_file)).T.reset_index(drop=False).rename(columns={'index':'Param'})
                        elif selected_model == "LightGBM":
                            with open('src/automl/config/default_lgbmparams.yaml', 'r') as rf_file:
                                default_space = pd.DataFrame(yaml.safe_load(rf_file)).T.reset_index(drop=False).rename(columns={'index':'Param'})
                        elif selected_model == "Gradient Boosting":
                            with open('src/automl/config/default_gbparams.yaml', 'r') as rf_file:
                                default_space = pd.DataFrame(yaml.safe_load(rf_file)).T.reset_index(drop=False).rename(columns={'index':'Param'})
                                # print(default_space)
                        reload_data = False
                        res1,res2 = st.columns([5,1.5])
                        reset = res2.button('Reset the table')
                        if reset:
                            grid_change = default_space.copy()
                            reload_data = True
                            grid_change = create_grid(grid_change,reload_data)['data']
                            reload_data = False
                        else:
                            grid_change = create_grid(default_space,reload_data = False)['data']
                        model_bestparams = st.button("Run Model")
                        if model_bestparams:
                            with st.spinner("Building the model and artifacts"):
                                d = automl_app.AutoMLApp(target_col=target_var,input_cols=input_var,train=Train_data,test=Test_data
                                        ,maxiter=max_trails,class_label=class_label,score = scoring_method,score_to_calc_on=score_on)
                                if grid_change is not None:
                                    # st.write("grid_change")
                                    model,best_params = d.run_optim(config = grid_change,algo_name=selected_model)
                                else:
                                    # st.write("default_space")
                                    model,best_params = d.run_optim(config = default_space,algo_name= selected_model)
                                if model:
                                    st.write('Best Param:',best_params)
                                    st.header("Train Metrics")
                                    tr_cm,tr_acc,tr_f1,tr_clf_report,tr_roc_score = performance(model=model,X=Train_data[input_var],Y=Train_data[target_var])
                                    st.write('Accuracy: ',tr_acc)
                                    st.write('F1 Score: ',tr_f1)
                                    st.write('Roc_Score: ',tr_roc_score)
                                    st.write('Classification Report:')
                                    st.code(tr_clf_report)
                                    st.subheader("Confusion Matrix") 
                                    ConfusionMatrixDisplay.from_estimator(model,Train_data[input_var],Train_data[target_var], display_labels=Train_data[target_var].unique())
                                    st.pyplot()
                                    st.subheader("ROC Curve") 
                                    RocCurveDisplay.from_estimator(model,Train_data[input_var],Train_data[target_var])
                                    st.pyplot()
                                    st.header("Test Metrics")
                                    ts_cm,ts_acc,ts_f1,ts_clf_report,ts_roc_score = performance(model=model,X=Test_data[input_var],Y=Test_data[target_var])
                                    st.write('Accuracy: ',ts_acc)
                                    st.write('F1 Score: ',ts_f1)
                                    st.write('Roc_Score: ',ts_roc_score)
                                    st.write('Classification Report: ')
                                    st.code(ts_clf_report)
                                    st.subheader("Confusion Matrix") 
                                    ConfusionMatrixDisplay.from_estimator(model,Test_data[input_var],Test_data[target_var], display_labels=Test_data[target_var].unique())
                                    st.pyplot()
                                    st.subheader("ROC Curve") 
                                    RocCurveDisplay.from_estimator(model,Test_data[input_var],Test_data[target_var])
                                    st.pyplot()
                    else:
                            st.error("This only supports for Binary Classification")
            except:
                st.error("Please provide the correct details")
        # else:
        #     st.info("Please provide all the details")

    elif data_source == 'MSSQL':
        if 'load_data_button' not in st.session_state:
                st.session_state["load_data_button"] = False
        with st.form('Form1'):
            ms10,ms11 = st.columns(2)
            server = ms10.text_input("Warehouse")
            database = ms11.text_input("Database")
            user_name = ms10.text_input("User_Name")
            password = ms11.text_input("Password")

            Train_data_query = ms10.text_input("SQL Train Query")
            Test_data_query = ms10.text_input("SQL Test Query")

            get_data = st.form_submit_button("Load Data",on_click = load_button_activate)
            
        if get_data or st.session_state["load_data_button"]:
            conn = mssql_client.mssql_engine(server, database, user_name, password)
            try:
                Train_data = pd.read_sql_query(Train_data_query, conn)
                Test_data = pd.read_sql_query(Test_data_query, conn)
                st.info("Data is Loaded Successfully")
                conn.close()
                if input_var and target_var:
                    if Train_data[target_var].nunique() == 2: 
                        var10,var11,var12 = st.columns(3)
                        class_label = var10.selectbox("Class Label",(Train_data[target_var].unique().tolist()))
                        scoring_method =var11.selectbox("Scoring Method",('Accuracy','F1 Score','Recall','Precision'))
                        score_on = var12.selectbox("Score on",("Train","Test"))
                        selected_model = st.selectbox("Select the Model",('XG Boost','Random Forest','Gradient Boosting','LightGBM'))
                        max_trails = st.slider("Max Trails to perform",min_value=2,max_value=5000,step=10)
                        if selected_model == "XG Boost":
                            with open('src/automl/config/default_xgbparams.yaml', 'r') as xg_file:
                                default_space = pd.DataFrame(yaml.safe_load(xg_file)).T.reset_index(drop=False).rename(columns={'index':'Param'})
                                # print(default_space)
                        elif selected_model == "Random Forest":
                            with open('src/automl/config/default_rfparams.yaml', 'r') as rf_file:
                                default_space = pd.DataFrame(yaml.safe_load(rf_file)).T.reset_index(drop=False).rename(columns={'index':'Param'})
                        elif selected_model == "LightGBM":
                            with open('src/automl/config/default_lgbmparams.yaml', 'r') as rf_file:
                                default_space = pd.DataFrame(yaml.safe_load(rf_file)).T.reset_index(drop=False).rename(columns={'index':'Param'})
                        elif selected_model == "Gradient Boosting":
                            with open('src/automl/config/default_gbparams.yaml', 'r') as rf_file:
                                default_space = pd.DataFrame(yaml.safe_load(rf_file)).T.reset_index(drop=False).rename(columns={'index':'Param'})
                                # print(default_space)
                        reload_data = False
                        res1,res2 = st.columns([5,1.5])
                        reset = res2.button('Reset the table')
                        if reset:
                            grid_change = default_space.copy()
                            reload_data = True
                            grid_change = create_grid(grid_change,reload_data)['data']
                            reload_data = False
                        else:
                            grid_change = create_grid(default_space,reload_data = False)['data']
                        model_bestparams = st.button("Run Model")
                        if model_bestparams:
                            with st.spinner("Building the model and artifacts"):
                                d = automl_app.AutoMLApp(target_col=target_var,input_cols=input_var,train=Train_data,test=Test_data
                                        ,maxiter=max_trails,class_label=class_label,score = scoring_method,score_to_calc_on=score_on)
                                if grid_change is not None:
                                    # st.write("grid_change")
                                    model,best_params = d.run_optim(config = grid_change,algo_name=selected_model)
                                else:
                                    # st.write("default_space")
                                    model,best_params = d.run_optim(config = default_space,algo_name= selected_model)
                                if model:
                                    st.write('Best Param:',best_params)
                                    st.header("Train Metrics")
                                    tr_cm,tr_acc,tr_f1,tr_clf_report,tr_roc_score = performance(model=model,X=Train_data[input_var],Y=Train_data[target_var])
                                    st.write('Accuracy: ',tr_acc)
                                    st.write('F1 Score: ',tr_f1)
                                    st.write('Roc_Score: ',tr_roc_score)
                                    st.write('Classification Report:')
                                    st.code(tr_clf_report)
                                    st.subheader("Confusion Matrix") 
                                    ConfusionMatrixDisplay.from_estimator(model,Train_data[input_var],Train_data[target_var], display_labels=Train_data[target_var].unique())
                                    st.pyplot()
                                    st.subheader("ROC Curve") 
                                    RocCurveDisplay.from_estimator(model,Train_data[input_var],Train_data[target_var])
                                    st.pyplot()
                                    st.header("Test Metrics")
                                    ts_cm,ts_acc,ts_f1,ts_clf_report,ts_roc_score = performance(model=model,X=Test_data[input_var],Y=Test_data[target_var])
                                    st.write('Accuracy: ',ts_acc)
                                    st.write('F1 Score: ',ts_f1)
                                    st.write('Roc_Score: ',ts_roc_score)
                                    st.write('Classification Report: ')
                                    st.code(ts_clf_report)
                                    st.subheader("Confusion Matrix") 
                                    ConfusionMatrixDisplay.from_estimator(model,Test_data[input_var],Test_data[target_var], display_labels=Test_data[target_var].unique())
                                    st.pyplot()
                                    st.subheader("ROC Curve") 
                                    RocCurveDisplay.from_estimator(model,Test_data[input_var],Test_data[target_var])
                                    st.pyplot()
                    else:
                        st.error("This only supports for Binary Classification")

            except:
                st.error("Please provide the correct details")
        # else:
        #     st.info("Please provide all the details")

    else:
        st.info("Please select the data source")
