
import streamlit as st
from . import examples



def show_examples():

    st.write(
        """
        
        # 환경을 아끼는 방법
        
        ---
        
        1. 쓰레기를 깔끔하게 모아둔다.
        
        2. 처리방법을 알고싶은 쓰레기를 촬영한다.
        
        #### 3. AI 퀴즈를 풀고 리워드를 받는다!
        
        4. 구체적인 폐기방법을 알게 된다.
        
        ### 5. 환경보호에 힘쓴다!
        
        
        
        
        ---
        
        
        
        """
    )

    examples.show()


if __name__ == "__main__":
    pass