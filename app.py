import streamlit as st
import requests
import urllib3

# SSL 경고 메시지를 안 보이게 숨겨줍니다
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# n8n Webhook URL
URL = "https://primary-production-b57a.upstage.app/webhook-test/5e2bd96c-0881-458f-8a4f-31795b4b066c"

st.title("스마트 영수증 관리자 📋")

img_file = st.file_uploader("영수증 사진을 업로드하세요", type=['png', 'jpg', 'jpeg'])

if img_file is not None:
    st.image(img_file, caption="업로드된 이미지", use_container_width=True)
    
    if st.button("영수증 분석하기"):
        with st.spinner("n8n으로 데이터를 전송 중입니다..."):
            try:
                files = {
                    "data": ("receipt.jpg", img_file.getvalue(), "image/jpeg")
                }
                
                # verify=False를 추가해서 SSL 에러를 강제로 통과시킵니다.
                response = requests.post(URL, files=files, verify=False)
                
                if response.status_code == 200:
                    st.success("전송 성공! n8n 화면을 확인하세요.")
                else:
                    st.error(f"전송 실패 (상태 코드: {response.status_code})")
                    st.write(response.text)
            except Exception as e:
                st.error(f"에러 발생: {e}")
