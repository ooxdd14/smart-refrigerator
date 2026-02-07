import streamlit as st
import requests

# n8n Webhook URL (사용자님의 URL로 확인하세요)
URL = "https://primary-production-b57a.upstage.app/webhook-test/5e2bd96c-0881-458f-8a4f-31795b4b066c"

st.title("스마트 영수증 관리자 📋")

img_file = st.file_view_container = st.file_uploader("영수증 사진을 업로드하세요", type=['png', 'jpg', 'jpeg'])

if img_file is not None:
    st.image(img_file, caption="업로드된 이미지", use_column_width=True)
    
    if st.button("영수증 분석하기"):
        with st.spinner("n8n으로 데이터를 전송 중입니다..."):
            try:
                # n8n이 'Binary' 탭으로 인식하도록 파일명과 타입을 명시합니다.
                files = {
                    "data": ("receipt.jpg", img_file.getvalue(), "image/jpeg")
                }
                
                # 데이터를 전송합니다.
                response = requests.post(URL, files=files)
                
                if response.status_code == 200:
                    st.success("전송 성공! n8n 화면을 확인하세요.")
                else:
                    st.error(f"전송 실패 (상태 코드: {response.status_code})")
                    st.write(response.text)
            except Exception as e:
                st.error(f"에러 발생: {e}")






