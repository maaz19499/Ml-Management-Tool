import streamlit as st
import time
import numpy as np
from src.quality.qa_app import QaApp

st.set_page_config(page_title="AutoML", page_icon="📈")

progress_bar = st.sidebar.progress(0)
qa = QaApp()
qa.call()

result = st.button('Run')
if result:
    st.write('Done!')