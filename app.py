import streamlit as st
import requests
import urllib3

# SSL 경고 무시
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# n8n Webhook URL
URL = "https://primary-production-b57a.up.railway.app/webhook-test/5e2bd96c-0881-458f-8a4f-31795b4b066c"

st.title("스마트 영수증 관리자 📋")

# 사진 업로드 (이미지 올리자마자 아래 코드가 바로 실행됨)
img_file = st.file_uploader("영수증 사진을 업로드하세요", type=['png', 'jpg', 'jpeg'])

if img_file is not None:
    st.image(img_file, caption="업로드됨", use_container_width=True)
    
    # 버튼 없이 바로 n8n으로 전송
    with st.spinner("분석 중..."):
        try:
            files = {
                "data": ("receipt.jpg", img_file.getvalue(), "image/jpeg")
            }
            # 전송 실행
            response = requests.post(URL, files=files, verify=False)
            
            if response.status_code == 200:
                st.success("전송 완료!")
            else:
                st.error(f"오류 발생: {response.status_code}")
        except Exception as e:
            st.error(f"에러: {e}")
