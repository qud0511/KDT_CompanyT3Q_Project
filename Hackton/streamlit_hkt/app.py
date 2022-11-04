import streamlit as st
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import altair as alt
import cv2
import sys
from pathlib import Path
import tensorflow as tf
from tensorflow import keras

# model = keras.models.load_model("./best_model.h5")
# model.predict(picture)

file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

try:
    sys.path.remove(str(parent))
except ValueError:  # Already removed
    pass

VERSION = ".".join(st.__version__.split(".")[:2])

from demos import orchestrator

demo_pages = {
    "챌린지 게임 시작하기": orchestrator.show_examples,
}



contributors = []

intro = f"""
"""

release_notes=''

def draw_main_page():
    st.write(
        f"""
        ### ***분리수거 챌린지에 오신 것을 환영합니다!*** 👋
        """
    )
    st.image('./recycle1.jpg')

    st.write(intro)

    st.write(release_notes)


# Draw sidebar
pages = list(demo_pages.keys())

if len(pages):
    pages.insert(0, "들어가기 전에")
    st.sidebar.title(f"MENU")
    query_params = st.experimental_get_query_params()
    if "page" in query_params and query_params["page"][0] == "headliner":
        index = 1
    
    else:
        index = 0
    selected_demo = st.sidebar.radio("", pages, index, key="pages")
else:
    selected_demo = "시작하기"

# Draw main page
if selected_demo in demo_pages:
    demo_pages[selected_demo]()
else:
    draw_main_page()    
    

# # 디렉토리와 파일을 주면, 해당 디렉토리에 파일을 저장하는 함수
# def save_uploaded_file(directory, file):
#     # 1. 디렉토리가 있는지 확인, 없으면 만듬.
#     if not open(os.path.join(directory, file.name), 'wb') as f:
#         os.makedirs(directory)
#     # 2. 디렉토리가 있으면 파일을 저장
#     with open(os.path.join(directory, file.name), 'wb') as f:
#         f.write(file.getbuffer())
#     return st.success('Saved file : {} in {}'.format(file.name, directory)