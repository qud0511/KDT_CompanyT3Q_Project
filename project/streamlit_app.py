import streamlit as st 

# title 쓰기
st.title('제목 쓰세요')
# 그냥 text 쓰기 
st.write('아무거나 쓰세요')
# markdown tag 쓰고 싶으면
st.markdown('<h1>태그를 쓸 수 있어요</h1>')
# user input 받기 
st.text_input('사용자 입력을 받아보세요: ')

# 이외에도 다양한 기능 엄청 많다~ 
st.button 
st.sidebar 

import requests
import numpy as np

def get_cctv_url(lat, lng):
    # CCTV 탐색 범위 지정을 위해 임의로 ±1 만큼 가감
    minX = str(lng-1)
    maxX = str(lng+1)
    minY = str(lat-1)
    maxY = str(lat+1)

    # 개인key 입력
    api_call = 'https://openapi.its.go.kr:9443/cctvInfo?' \
               'apiKey=개인key' \
               '&type=ex&cctvType=2' \
               '&minX=' + minX + \
               '&maxX=' + maxX + \
               '&minY=' + minY + \
               '&maxY=' + maxY + \
               '&getType=json'

    w_dataset = requests.get(api_call).json()
    cctv_data = w_dataset['response']['data']

    coordx_list = []
    for index, data in enumerate(cctv_data):
        xy_couple = (float(cctv_data[index]['coordy']),float(cctv_data[index]['coordx']))
        coordx_list.append(xy_couple)

    # 입력한 위경도 좌표에서 가장 가까운 위치에 있는 CCTV를 찾는 과정
    coordx_list = np.array(coordx_list)
    leftbottom = np.array((lat, lng))
    distances = np.linalg.norm(coordx_list - leftbottom, axis=1)
    min_index = np.argmin(distances)

    return cctv_data[min_index]


cctv_data = get_cctv_url(36.58629, 128.186793)
print('CCTV명:', cctv_data['cctvname']) # 가장 가까운 CCTV명
print('CCTV 영상 URL:', cctv_data['cctvurl']) # 가장 가까운 CCTV 영상 URL