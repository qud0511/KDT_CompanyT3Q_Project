

import streamlit as st
import cv2
from PIL import Image,ImageEnhance
import numpy as np
import pandas as pd
import glob
import random
import os
import streamlit as st
import pandas as pd
import cv2
from PIL import Image, ImageEnhance
import numpy as np
import os
#import tensorflow as tf
#import tensorflow_hub as hub
import time ,sys
#from streamlit_embedcode import github_gist
import urllib.request
import urllib
#import moviepy.editor as moviepy
import cv2

import time
import sys
import sqlite3 
import hashlib
import streamlit as st
import pandas as pd
import cv2
from PIL import Image, ImageEnhance
import os
import tensorflow as tf
import tensorflow_hub as hub
import time ,sys
from streamlit_embedcode import github_gist
import urllib.request
import urllib
import moviepy.editor as moviepy
import cv2
import numpy as np
import time
import sys
import requests, json
import pandas as pd
import numpy as np
import numpy as np
import pandas as pd
import pydeck as pdk


# 로그인 화면 
conn = sqlite3.connect('database.db')
c = conn.cursor()

import hashlib
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False

def create_user():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')

def add_user(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data

def main():

	#st.title("로그인 기능 테스트")

	menu = ["Login","signUp","Dectection", "LiveWebcam", "Map"]
	choice = st.sidebar.selectbox("MENU",menu)



    
	if choice == "Login":
		st.subheader("로그인 해주세요")

		username = st.sidebar.text_input("유저명을 입력해주세요")
		password = st.sidebar.text_input("비밀번호를 입력해주세요",type='password')
		if st.sidebar.checkbox("Login"):
			create_user()
			hashed_pswd = make_hashes(password)

			result = login_user(username,check_hashes(password,hashed_pswd))
			if result:

				st.success("{}님으로 로그인했습니다.".format(username))

			else:
				st.warning("사용자 이름이나 비밀번호가 잘못되었습니다.")

	elif choice == "signUp":
		st.subheader("새 계정을 만듭니다.")
		new_user = st.text_input("유저명을 입력해주세요")
		new_password = st.text_input("비밀번호를 입력해주세요",type='password')

		if st.button("signUp"):
			create_user()
			add_user(new_user,make_hashes(new_password))
			st.success("계정 생성에 성공했습니다.")
			st.info("로그인 화면에서 로그인 해주세요.")
    
	elif choice == "Dectection":
		st.subheader("위험물 탐지")		
		selected_item = st.sidebar.radio("select", ("Image", "Video"))
		if selected_item == "Image":
			file = st.file_uploader("Upload Image",type=['jpg', 'png', 'jpeg'])
			if file!= None:
				img1 = Image.open(file)
				img2 = np.array(img1)
				st.image(img1, caption = "원본 이미지")
				st.image(img1, caption = "탐지된 이미지")
		elif selected_item == "Video":
			video_file = st.file_uploader('video', type = ['mp4'])
			cap = cv2.VideoCapture(video_file)
	elif choice == "LiveWebcam":
		st.title("Webcam Live Feed")
		run = st.checkbox('Run')
		FRAME_WINDOW = st.image([])
		camera = cv2.VideoCapture(0)

		while run:
			_, frame = camera.read()
			frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
			FRAME_WINDOW.image(frame)
		else:
			st.write('Stopped')	

	elif choice == "Map":
				# 현재위치 좌표 얻기 --------------------------------------------------------------
		

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
				map_style=None, initial_view_state=pdk.ViewState(longitude=lo, latitude=la, zoom=11, pitch=50), layers=layers
			)

			st.pydeck_chart(deck, use_container_width=True)

		# 실시간 위치 지도 표시 함수 실행 ------------------------------------------------------------------------
		gps = current_location()
		location_detail(gps)

if __name__ == '__main__':
	main()

