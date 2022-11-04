import streamlit as st
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import altair as alt
import cv2

import sys
from pathlib import Path

file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

try:
    sys.path.remove(str(parent))
except ValueError:  # Already removed
    pass

import streamlit as st

VERSION = ".".join(st.__version__.split(".")[:2])

from demos import orchestrator

demo_pages = {
    "st.camera_input": orchestrator.show_examples,
}



contributors = []

intro = f"""
This release launches Camera Input as well as other improvements and bug fixes.
"""

release_notes = f"""
---
**Highlights**
- 📸 Introducing `st.camera_input` for uploading images straight from your camera.
**Notable Changes**
- 🚦 Widgets now have the `disabled` parameter that removes interactivity.
- 🚮 Clear `st.experimental_memo` and `st.experimental_singleton` programmatically by using the `clear()` method on a cached function.
- 📨 Developers can now configure the maximum size of a message to accommodate larger messages within the Streamlit application. See `server.maxMessageSize`.
- 🐍 We formally added support for Python 3.10.
**Other Changes**
- 😵‍💫 Calling `str` or `repr` on `threading.current_thread()` does not cause a RecursionError ([#4172](https://github.com/streamlit/streamlit/issues/4172)).
- 📹 Gracefully stop screencast recording when user removes permission to record ([#4180](https://github.com/streamlit/streamlit/pull/4180)).
- 🌇 Better scale images by using a higher-quality image bilinear resampling algorithm ([#4159](https://github.com/streamlit/streamlit/pull/4159)).
[Click here](https://github.com/streamlit/streamlit/compare/1.3.0...1.4.0) to check out all updates. As always, thank you to all [our contributors](https://github.com/streamlit/streamlit/graphs/contributors) who help make Streamlit awesome!
"""

# End release updates


def draw_main_page():
    st.write(
        f"""
        # Welcome to Streamlit 1.4.0! 👋
        """
    )

    st.write(intro)

    st.write(release_notes)


# Draw sidebar
pages = list(demo_pages.keys())

if len(pages):
    pages.insert(0, "Release Notes")
    st.sidebar.title(f"Streamlit v1.4.0 🎈")
    query_params = st.experimental_get_query_params()
    if "page" in query_params and query_params["page"][0] == "headliner":
        index = 1
    else:
        index = 0
    selected_demo = st.sidebar.radio("", pages, index, key="pages")
else:
    selected_demo = "Release Notes"

# Draw main page
if selected_demo in demo_pages:
    demo_pages[selected_demo]()
else:
    draw_main_page()

# def file_selector(folder_path='.'):
#     filenames = os.listdir(folder_path)
#     selected_filename = st.selectbox('Select a file', filenames)
#     return os.path.join(folder_path, selected_filename)


# if __name__ == '__main__':
#     # Select a file
#     if st.checkbox('Select a file in current directory'):
#         folder_path = '.'
#         if st.checkbox('Change directory'):
#             folder_path = st.text_input('Enter folder path', '.')
#         filename = file_selector(folder_path=folder_path)
#         st.write('You selected `%s`' % filename)
    

    # # 디렉토리와 파일을 주면, 해당 디렉토리에 파일을 저장하는 함수
    # def save_uploaded_file(directory, file):
    #     # 1. 디렉토리가 있는지 확인, 없으면 만듬.
    #     if not open(os.path.join(directory, file.name), 'wb') as f:
    #         os.makedirs(directory)
    #     # 2. 디렉토리가 있으면 파일을 저장
    #     with open(os.path.join(directory, file.name), 'wb') as f:
    #         f.write(file.getbuffer())
    #     return st.success('Saved file : {} in {}'.format(file.name, directory)