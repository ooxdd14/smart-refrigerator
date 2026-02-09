import streamlit as st
from PIL import Image # 이미지 처리를 위해 추가

st.title("영수증 관리자 (테스트 모드) 📋")

# 사진 업로드
img_file = st.file_uploader("영수증 사진을 선택하세요", type=['png', 'jpg', 'jpeg'])

if img_file is not None:
    try:
        # 1. 파일을 이미지 객체로 변환
        image = Image.open(img_file)
        
        # 2. 화면에 출력 (용량을 줄여서 출력)
        st.image(image, caption="업로드 성공!", use_container_width=True)
        st.success("사진이 정상적으로 읽혔습니다. 이제 전송 기능을 연결해도 됩니다.")
        
    except Exception as e:
        st.error(f"사진을 불러오는 중 오류 발생: {e}")
