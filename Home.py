# from streamlit_shap import st_shap
# import shap
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import os
import logging
import numpy as np
from tools_page import Data_Quality_Tool, Description,EDA,AutoML
from tools_page import Explainability,Baisness_Fairness,Data_Generation


# st.set_page_config(page_title="Main", page_icon="📈")
# st.write("""# Data Science Managment Tool""")
# st.markdown(
#         """
#         End to End Machine learning pipeline
        
#         **👈 Select your objective from the left side bar""")
    
# st.sidebar.header("Tasks")
# st.sidebar.markdown("### Select the your task here!")
# st.set_page_config(layout="wide")
# "padding": "0!important"

def main():

    # st.set_page_config(page_title="Option Menu with Pages Example", page_icon=":guardsman:", layout="wide")
    
    with st.sidebar:
        choose = option_menu("Frameworks", ["Description","EDA", "Data Generation", "Quality Tool","AutoML","Explainability","Baisness & Fairness","Pipeline"],
                            icons=['house', 'clipboard-data', 'kanban', 'ui-checks','joystick','question-lg','tools'],
                            menu_icon="app-indicator",
                            styles={
            "container": {"background-color": "#fafafa"},
            "icon": {"color": "orange", "font-size": "22px"}, 
            "nav-link": {"font-size": "14px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#02ab21"},
        }
        )

    if choose == "Description":
        # st.experimental_memo.clear()
        Description.render()
    elif choose == "Quality Tool":
        # st.experimental_memo.clear()
        Data_Quality_Tool.Quality_render()
    elif choose == "EDA":
        # st.experimental_memo.clear()
        EDA.EDA_render()
    elif choose == "AutoML":
        # st.experimental_memo.clear()
        AutoML.AutoML_render()
    elif choose == "Explainability":
        # st.experimental_memo.clear()
        Explainability.Explain_render()
    elif choose == "Baisness & Fairness":
        # st.experimental_memo.clear()
        Baisness_Fairness.Bias_fairness_render()
    elif choose == "Data Generation":
        # st.experimental_memo.clear()
        Data_Generation.Data_generation_render()
        
if __name__ == '__main__':
    with st.spinner('In progress...'):
        main()
        # st.success('Done!')
    
