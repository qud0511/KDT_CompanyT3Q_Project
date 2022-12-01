# 모듈 로딩
import sqlite3, cv2
import streamlit as st
from PIL import Image, ImageEnhance
import requests, json, os
import numpy as np
import pandas as pd
import pydeck as pdk
import yolo_v5.detect as detect
from tkinter.tix import COLUMN
from pyparsing import empty

# 레이아웃 관련
st.set_page_config(layout="wide")

# 로그인 화면
conn = sqlite3.connect('database.db')
c = conn.cursor()

import hashlib


def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()


def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False


def create_user():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_user(username, password):
    c.execute('INSERT INTO userstable(username,password) VALUES (?,?)', (username, password))
    conn.commit()


def login_user(username, password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?', (username, password))
    data = c.fetchall()
    return data


def main():
    # st.title("로그인 기능 테스트")

    menu = ["Login", "signUp", "Dectection", "Map"]
    choice = st.sidebar.selectbox("MENU", menu)

    if choice == "Login":
        st.subheader("로그인 해주세요")

        username = st.sidebar.text_input("유저명을 입력해주세요")
        password = st.sidebar.text_input("비밀번호를 입력해주세요", type='password')
        if st.sidebar.checkbox("Login"):
            create_user()
            hashed_pswd = make_hashes(password)

            result = login_user(username, check_hashes(password, hashed_pswd))
            if result:

                st.success("{}님으로 로그인했습니다.".format(username))

            else:
                st.warning("사용자 이름이나 비밀번호가 잘못되었습니다.")

    elif choice == "signUp":
        st.subheader("새 계정을 만듭니다.")
        new_user = st.text_input("유저명을 입력해주세요")
        new_password = st.text_input("비밀번호를 입력해주세요", type='password')

        if st.button("signUp"):
            create_user()
            add_user(new_user, make_hashes(new_password))
            st.success("계정 생성에 성공했습니다.")
            st.info("로그인 화면에서 로그인 해주세요.")

    # Detection 탭
    elif choice == "Dectection":
        st.subheader("위험물 탐지")
        selected_item = st.sidebar.radio("select", ("Image", "Video"))
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        # Image 업로드 탭
        if selected_item == "Image":
            file = st.file_uploader("Upload Image", type=['jpg', 'png', 'jpeg'])
            if file != None:
                img = Image.open(file)
                img.save('./temp/temp.png', 'PNG')
                st.image(img)
                if st.button("추론 결과"):
                    img_result, video_result = detect.run(source=f'./temp/temp.png')
                    st.image(img_result)
        # Video 업로드 탭
        elif selected_item == "Video":
            selected_video = st.radio(label="영상을 선택해주세요.", options=['1', '2', '3', '4'])
            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
            if selected_video == "1":
                st.video('./temp/temp_1.mp4', start_time=0)
                if st.button("추론 결과"):
                    # img_result, video_result = detect.run(source=f'./temp/temp_1_result.mp4')
                    st.video('./temp/temp_1_result.mp4', 'rb', start_time=0)
            elif selected_video == "2":
                st.video('./temp/temp_1.mp4', start_time=0)
                if st.button("추론 결과"):
                    st.video('./temp/temp_1.mp4', start_time=0)
            elif selected_video == "3":
                st.video('./temp/temp_1.mp4', start_time=0)
                if st.button("추론 결과"):
                    st.video('./temp/temp_1.mp4', start_time=0)
            elif selected_video == "4":
                st.video('./temp/temp_1.mp4', start_time=0)
                if st.button("추론 결과"):
                    st.video('./temp/temp_1.mp4', start_time=0)


    elif choice == "Map":
        # 현재위치 좌표 얻기
        def current_location():
            here_req = requests.get("http://www.geoplugin.net/json.gp")

            if (here_req.status_code != 200):
                print("현재좌표를 불러올 수 없음")
            else:
                location = json.loads(here_req.text)
                crd = {float(location["geoplugin_latitude"]), float(location["geoplugin_longitude"])}
                crd = list(crd)
                gps = pd.DataFrame([[crd[1], crd[0]]], columns=['위도', '경도'])

            return gps

        # 맵에 위치 표시 ------------------------------------------------------------------------------------------

        # 위치정보 상세 (단, data에 위도, 경도 컬럼이 있어야 함)

        def location_detail(data_c):
            data = data_c.copy()

            # 아이콘 이미지 불러오기
            ICON_URL = "https://cdn-icons-png.flaticon.com/128/2268/2268142.png"
            icon_data = {
                # Icon from Wikimedia, used the Creative Commons Attribution-Share Alike 3.0
                # Unported, 2.5 Generic, 2.0 Generic and 1.0 Generic licenses
                "url": ICON_URL,
                "width": 242,
                "height": 242,
                "anchorY": 242,
            }
            data["icon_data"] = None
            for i in data.index:
                data["icon_data"][i] = icon_data
            la, lo = np.mean(data["위도"]), np.mean(data["경도"])

            layers = [
                pdk.Layer(
                    type="IconLayer",
                    data=data,
                    get_icon="icon_data",
                    get_size=4,
                    size_scale=15,
                    get_position="[경도, 위도]",
                    pickable=True,
                )
            ]

            # Deck 클래스 인스턴스 생성
            deck = pdk.Deck(
                map_style=None, initial_view_state=pdk.ViewState(longitude=lo, latitude=la, zoom=11, pitch=50),
                layers=layers
            )

            st.pydeck_chart(deck, use_container_width=True)

        # 실시간 위치 지도 표시 함수 실행 ------------------------------------------------------------------------
        gps = current_location()
        location_detail(gps)


if __name__ == '__main__':
    main()
