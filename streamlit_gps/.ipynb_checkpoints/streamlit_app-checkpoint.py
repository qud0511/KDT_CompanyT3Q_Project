# 실행코드-------------------------------------------
# streamlit run streamlit_app.py
#----------------------------------------------------

import streamlit as st 
st.set_page_config(layout="wide")

# title 쓰기
st.title(' 대구광역시 유지보수 필요한 포트홀 위치정보 ')
# 지역을 고르는 select box
option = st.sidebar.selectbox(
    '어떤 지역을 고르시겠습니까?',
    ('대구 전체','북구', '중구', '서구', '동구',"남구", "수성구", "달서구", "달성군"))

# if st.sidebar.selectbox('실행'):


# [ 현재위치 좌표 수집 함수 ] --------------------------------------------------------------
import requests, json
import pandas as pd
import numpy as np

def current_location():
    here_req = requests.get("http://www.geoplugin.net/json.gp")

    if (here_req.status_code != 200):
        print("현재좌표를 불러올 수 없음")
    else:
        location = json.loads(here_req.text)
        crd = {float(location["geoplugin_latitude"]), float(location["geoplugin_longitude"])}
        crd = list(crd)
        gps = pd.DataFrame( [[crd[1],crd[0]]], columns=['위도','경도'])
    
    return gps
    


# [ 맵에 위치 표시 함수] ------------------------------------------------------------------------------------------
import numpy as np
import pandas as pd
import pydeck as pdk
import streamlit as st

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
            get_position="[경도, 위도]",
            pickable=True,
        )
    ]
    
    if len(data_c) == 0:
        pass
    else:
        # Deck 클래스 인스턴스 생성
        deck = pdk.Deck(height=100,
                        #width=1000,
                        map_style=None, 
                        initial_view_state=pdk.ViewState(longitude=lo, 
                                                        latitude=la, 
                                                        zoom=12, 
                                                        pitch=50), 
                        layers=layers,
                        tooltip={"text":"{주소}\n{위도}/{경도}"})

        st.pydeck_chart(deck, use_container_width=True)

# r = pdk.Deck(
#     layers=[layer],
#     initial_view_state=view_state,
#     tooltip={"text": "{name}\n{address}"},
#     map_style=pdk.map_styles.ROAD,
# )

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
from geopy.geocoders import Nominatim

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
    st.dataframe(df)

    # 해당 지역 위치정보 개수 표기
    st.write(option,'지역, 보수가 필요한 구역: ',len(df),'개')
    
    return df_map
#---------------------------------------------------------------

# [ 지도 함수 실행 코드 ]------------------------------------------------------------------------

# 실시간 위치정보 수집
gps = current_location()

# 기존 위치정보데이터에 실시간 위치정보 추가 갱신
add_gps_all(gps)

# 최종 수정된 전체 위치정보 파일 불러오기
gps_all = pd.read_csv('gps_all.csv')

# 주소 데이터프레임 표시
df_map = createDF(gps_all) 
# 전체 위치정보 웹 지도에 표시
location_detail(df_map)