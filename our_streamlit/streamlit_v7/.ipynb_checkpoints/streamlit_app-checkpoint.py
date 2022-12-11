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
from geopy.geocoders import Nominatim
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode
import tempfile
# from streamlit.cli import main
import time
# 레이아웃 관련
st.set_page_config(layout="wide")

# -
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

    menu = [ "회원가입", "📌 로그인", "⚠️ Dectection", "🗺️ 포트홀 등 도로손상 현황", 'LiveCam']
    choice = st.sidebar.selectbox("MENU", menu)

    if choice == "회원가입":
        st.subheader("새 계정을 만듭니다")
        new_user = st.text_input("유저명을 입력해주세요")
        new_password = st.text_input("비밀번호를 입력해주세요", type='password')

        if st.button("signUp"):
            create_user()
            add_user(new_user, make_hashes(new_password))
            st.success("계정 생성에 성공했습니다.")
            st.info("로그인 화면에서 로그인 해주세요.")
            st.balloons() 

    elif choice == "📌 로그인":
        st.subheader("로그인 해주세요")

        username = st.text_input("유저명을 입력해주세요")
        password = st.text_input("비밀번호를 입력해주세요", type='password')
        if st.button("Login"):
            create_user()
            hashed_pswd = make_hashes(password)

            result = login_user(username, check_hashes(password, hashed_pswd))
            if result:

                st.success("{}님으로 로그인했습니다.".format(username))
                st.balloons() 

            else:
                st.warning("사용자 이름이나 비밀번호가 잘못되었습니다.")        


    # Detection 탭
    elif choice == "⚠️ Dectection":
        st.header('⚠ 도로 위 위험물 탐지 ⚠')
        selected_item = st.sidebar.radio("select", ("Image", "Video"))
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        # Image 업로드 탭
        if selected_item == "Image":
            file = st.file_uploader("사진을 업로드하세요", type=['jpg', 'png', 'jpeg'])
            if file != None:
                col1, col2, col3 = st.columns([4,0.8,4])
                img = Image.open(file)
                img.save('./temp/temp.png', 'PNG')
                with col1:
                    html='<h2>원본 이미지<h2>'
                    st.components.v1.html(html="<center>" + html + "</center>", height=48)
                    st.image(img)
                with col2:
                    st.header('    ')
                    st.header('    ')
                    st.header('    ')
                    st.header('    ')
                    st.header('    ')
                    st.header('    ')
                    if st.button("추론 결과"):
                        with st.empty():
                            for seconds in range(1):
                                st.components.v1.html(html="<center>" +'⏳' + "</center>")
                                time.sleep(1)
                            st.components.v1.html(html="<center>" +'✔️' + "</center>")                                                
                            img_result, video_result = detect.run(source=f'./temp/temp.png')
                        with col3:
                            html='<h2>탐지된 이미지<h2>'
                            st.components.v1.html(html="<center>" + html + "</center>", height=48)
                            st.image(img_result)
        # Video 업로드 탭
        elif selected_item == "Video":
            #html='<h3>영상을 업로드하세요<h3>'
            #st.components.v1.html(html=html, height=50)
            selected_video = st.radio(label='영상을 업로드하세요', options=['1', '2', '3', '4'])
            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
            col1, col2, col3 = st.columns([4.3,0.8,4.3])
            
            if selected_video == "1":
                with col1:
                    html='<h2>원본 영상<h2>'
                    st.components.v1.html(html="<center>" + html + "</center>", height=48)           
                    st.video('./temp/temp_1.mp4', start_time=0)
                with col2:
                    st.header('    ')
                    st.header('    ')
                    st.header('    ')
                    st.header('    ')
                    st.header('    ')
                    st.header('    ')
                with col2:
                    #m = st.markdown("""<div style=" text-align: center;"> <button style=" display: inline-block;">버튼클릭!!</button> </div>""", unsafe_allow_html=True)
                    if st.button("추론결과"):  
                        with st.empty():
                            for seconds in range(1):
                                st.components.v1.html(html="<center>" +'⏳' + "</center>")
                                time.sleep(1)
                            st.components.v1.html(html="<center>" +'✔️' + "</center>")                            
                    # img_result, video_result = detect.run(source=f'./temp/temp_1_result.mp4')
                        with col3: 
                            html='<h2>탐지된 영상<h2>'
                            st.components.v1.html(html="<center>" + html + "</center>", height=48) 
                            st.video('./temp/temp_1_result.mp4', 'rb', start_time=0)
            elif selected_video == "2":
                with col1:
                    html='<h2>원본 영상<h2>'
                    st.components.v1.html(html="<center>" + html + "</center>", height=48)           
                    st.video('./temp/temp_1.mp4', start_time=0)
                with col2:
                    st.header('    ')
                    st.header('    ')
                    st.header('    ')
                    st.header('    ')
                    st.header('    ')
                    st.header('    ')
                with col2:
                    if st.button("추론결과"):  
                        with st.empty():
                            for seconds in range(1):
                                st.components.v1.html(html="<center>" +'⏳' + "</center>")
                                time.sleep(1)
                            st.components.v1.html(html="<center>" +'✔️' + "</center>") 
                    # img_result, video_result = detect.run(source=f'./temp/temp_1_result.mp4')
                        with col3: 
                            html='<h2>탐지된 영상<h2>'
                            st.components.v1.html(html="<center>" + html + "</center>", height=48) 
                            st.video('./temp/temp_1_result.mp4', 'rb', start_time=0)
            elif selected_video == "3":
                with col1:
                    html='<h2>원본 영상<h2>'
                    st.components.v1.html(html="<center>" + html + "</center>", height=48)           
                    st.video('./temp/temp_1.mp4', start_time=0)
                with col2:
                    st.header('    ')
                    st.header('    ')
                    st.header('    ')
                    st.header('    ')
                    st.header('    ')
                    st.header('    ')
                with col2:
                    if st.button("추론결과"):  
                        with st.empty():
                            for seconds in range(1):
                                st.components.v1.html(html="<center>" +'⏳' + "</center>")
                                time.sleep(1)
                            st.components.v1.html(html="<center>" +'✔️' + "</center>") 
                    # img_result, video_result = detect.run(source=f'./temp/temp_1_result.mp4')
                        with col3: 
                            html='<h2>탐지된 영상<h2>'
                            st.components.v1.html(html="<center>" + html + "</center>", height=48) 
                            st.video('./temp/temp_1_result.mp4', 'rb', start_time=0)         
            elif selected_video == "4":
                with col1:
                    html='<h2>원본 영상<h2>'
                    st.components.v1.html(html="<center>" + html + "</center>", height=48)           
                    st.video('./temp/temp_1.mp4', start_time=0)
                with col2:
                    st.header('    ')
                    st.header('    ')
                    st.header('    ')
                    st.header('    ')
                    st.header('    ')
                    st.header('    ')
                with col2:
                    if st.button("추론결과"):  
                        with st.empty():
                            for seconds in range(1):
                                st.components.v1.html(html="<center>" +'⏳' + "</center>")
                                time.sleep(1)
                            st.components.v1.html(html="<center>" +'✔️' + "</center>") 
                    # img_result, video_result = detect.run(source=f'./temp/temp_1_result.mp4')
                        with col3: 
                            html='<h2>탐지된 영상<h2>'
                            st.components.v1.html(html="<center>" + html + "</center>", height=48) 
                            st.video('./temp/temp_1_result.mp4', 'rb', start_time=0)
    elif choice == "LiveCam":
        st.title("Webcam Live Feed")
        run = st.checkbox('Run')        
        #result = detect.run(source=f'./123.mp4')
        #st.video(result)

        FRAME_WINDOW = st.image([])
        camera = cv2.VideoCapture()
        while run:
            _, frame = camera.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            FRAME_WINDOW.image(frame)
        else:
            st.write('Stopped')

    elif choice == "🗺️ 포트홀 등 도로손상 현황":
        option = st.sidebar.selectbox(
            '어떤 지역을 고르시겠습니까?',
            ('대구 전체','북구', '중구', '서구', '동구',"남구", "수성구", "달서구", "달성군"))
        
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
        #실시간 위치정보 수집(시연용) - 경북대학교
        def geocoding():
            geolocoder = Nominatim(user_agent = 'South Korea', timeout=None)
            geo = geolocoder.geocode("대구 북구 경북대학교 글로벌플라자")
            crd = {"lat": str(geo.latitude), "lng": str(geo.longitude)}
            gps = pd.DataFrame( [[crd['lat'],crd['lng']]], columns=['위도','경도'])
            return gps
        # 맵에 위치 표시 ------------------------------------------------------------------------------------------

        # 위치정보 상세 (단, data에 위도, 경도 컬럼이 있어야 함)

        def location_detail(data_c):
            data = data_c.copy()

            # 아이콘 이미지 불러오기
            ICON_URL = "https://cdn-icons-png.flaticon.com/512/2711/2711648.png"
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
                    get_position=['경도', '위도'],
                    pickable=True,
                    auto_highlight=True,
                    extruded=True
                )
            ]
            view_state = pdk.ViewState(longitude=lo, 
                                        latitude=la, 
                                        zoom=12, 
                                        pitch=50)
            # ============================================================================================================
            # Ag-Grid
            col1, col2 = st.columns(2)
            with col1:
                
                selection = aggrid_interactive_table(df_map)
            with col2:
                try:
                    if selection:
                        # st.write(selection["selected_rows"][0]["_selectedRowNodeInfo"]["nodeRowIndex"])
                        img=Image.open(f'./result/{int(selection["selected_rows"][0]["_selectedRowNodeInfo"]["nodeRowIndex"])}.jpg')
                        img = img.resize((500, 200))
                        st.image(img, use_column_width=True)
                        
                        view_state = pdk.ViewState(longitude=selection['selected_rows'][0]['경도'], 
                                            latitude=selection['selected_rows'][0]['위도'], 
                                            zoom=17, 
                                            pitch=50)
                        deck.initial_view_state = view_state
                        deck.update()

                        
                except:
                    pass
            # ============================================================================================================
            if len(data_c) == 0:
                pass
            else:
                # Deck 클래스 인스턴스 생성
                deck = pdk.Deck(height=100,
                                #width=1000,
                                map_style='road', 
                                initial_view_state=view_state, 
                                layers=layers,
                                tooltip={"text":"{주소}\n{위도}/{경도}"})
                
                st.pydeck_chart(deck, use_container_width=True)
                
                
        # [ gps 데이터셋 갱신 및 누적 함수 ]--------------------------------------------------
        def add_gps_all(gps):
            # gps_all(기존) 불러오기
            gps_all = pd.read_csv('gps_all.csv')

            # gps_all(기존), gps(추가 갱신) 데이터프레임 결합 
            gps_all = pd.concat([gps_all,gps]).reset_index()
            gps_all = gps_all.drop('index',axis=1)

            # 중복 위치정보 제거
            gps_all = gps_all.drop_duplicates(['위도','경도'])

            # 추가 위치정보 저장된 데이터프레임 저장
            gps_all.to_csv('gps_all.csv',index = False)
            
        # [위도,경도 -> 주소 변환 함수]-----------------------------------------------------    
        def geocoding_reverse(lat_lng_str): 
            geolocoder = Nominatim(user_agent = 'South Korea', timeout=None)
            address = geolocoder.reverse(lat_lng_str)

            return address            
                
        # [ 지역 구별 주소 데이터프레임 함수 ]----------------------------------------------------
        def createDF(gps_all):
        # 위도,경도 -> 주소 변환
            address_list = []
            for i in range(len(gps_all)):

                lat = gps_all['위도'][i]
                lng = gps_all['경도'][i]
                address = geocoding_reverse(f'{lat}, {lng}')

                # 카테고리 선택 
                if option =='대구 전체':
                    address_list.append(address)
                elif option in address[0]:
                    address_list.append(address)

            df = pd.DataFrame(address_list, columns=['주소','위치정보(위도,경도)'])

            df_map = pd.DataFrame(columns=['주소','위도','경도'])
            for i in range(len(df)):
                df_map.loc[i] = [df.loc[i]['주소'],df.loc[i][1][0],df.loc[i][1][1]]

            # 위도,경도 주소변환 데이터프레임 시각화
            # st.dataframe(df)

            # 해당 지역 위치정보 개수 표기
            st.write(option,'지역, 보수가 필요한 구역: ',len(df),'개')

            return df_map
        
        # 데이터프레임 상호작용 함수
        def aggrid_interactive_table(df):
            options = GridOptionsBuilder.from_dataframe(
                df,  enableRowGroup=True, enableValue=True, enablePivot=True
            )
            options.configure_side_bar()

            options.configure_selection('single')
            selection = AgGrid(
                df,
                enable_enterprise_modules=True,
                gridOptions=options.build(),
                update_mode=GridUpdateMode.MODEL_CHANGED,
                allow_unsafe_jscode=True,
                height=300
            )

            return selection

        # [ 지도 함수 실행 코드 ]------------------------------------------------------------------------
##############
        if st.sidebar.button('현재 위치 추가'):
        # 실시간 위치정보 수집
            gps=geocoding()
            # 기존 위치정보데이터에 실시간 위치정보 추가 갱신
            add_gps_all(gps)

        # 최종 수정된 전체 위치정보 파일 불러오기
        gps_all = pd.read_csv('gps_all.csv')

        # 주소 데이터프레임 표시
        df_map = createDF(gps_all) 
        # 전체 위치정보 웹 지도에 표시
        location_detail(df_map)
    
if __name__ == '__main__':
    main()
