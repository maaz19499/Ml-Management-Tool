import streamlit as st
import time
import numpy as np

st.set_page_config(page_title="Description", page_icon="📈",layout="wide")

def render():
    st.write("""# Machine learning Management Tool""")
    col1,col2 = st.columns([2,4])
    col2.markdown('-- A tool to manage life cycle of machine learning ecosystem')
    st.markdown(
        """       
    💬 **:orange[About]:**  
        This tool provides a no code platform to perform some important tasks of machine learning life cycle. Additionally, it is a platform that integrate several decoupled frameworks together. This tool has mainly 6 section such as EDA, data generation, AutoML, Explainability etc.

    🎯 **:orange[Objective]:**  
    The primary goal of this tool is not to create a robust and generic product that can solve each and every problem of ML. However, we should consider this tool as substitute incase existing robust systems are not working. 
    Furthermore, this tool brings capability for user to perform most of the important and high level ML work through no code platform.

    🧰 **:orange[Why this tool?]**  
        Below is the list of few use cases where we can see why we need this tool.
    -	We can use AutoML section of this tool if H2O DAI is not providing better model performance.
    -	We can do comparative study of two data sets and understand the differences. This may help to understand data drift. 
    -	We can get feel of UI to do quality test of the data.

    ⛔ **:orange[What is this tool not meant for?]**  
        While creating this platform, we have some basic and initial fundamental principle that we should try to adhere while making changes. Overall, we should not aim to make it very generic tool as Ascend is not a software company and this product is being developed to cater niche business of Ascend. At the same time, we don’t want to compete with other paid tools available in the market.

    🚀 **:orange[Future Development:]**   
        This tool is in inception stage; hence we may need more brainstorming and feedback from other team members to bring it in a good shape.
    1.	Always remember “What is this tool not meant for?” while making new changes
    2.	We need to improve the coding structure of this tool to improve the performance and make it error free.
    3.	Need to integrate experiment tracking
    4.	Pipeline creation: Below steps are based on initial thought, it may change in the future
        -	We can think to create a pipeline via this tool and initial thoughts are as below which may or may not change
        -	Add “Add to pipeline” button on “Quality Tool”, “Auto ML”, Explainability and Biasedness and Fairness tool section
        -	Once user clicks on this button, this tool will create a config file with all the supporting information in pipeline folder one by one (Similar to airflow)
        -	Finally, we can see the created workflow on pipeline section and execute it for further testing.
    5.	Scope to add new rules in quality tool
    6.	We may need to add better EDA tool to get more information
    7.	Add more algorithms in AutoML
    8.	User should be able to save model for explainability section and see list of all the saved/loaded model
    9.	Scope to add comparative model explainability feature for multiple models in one view
    """)