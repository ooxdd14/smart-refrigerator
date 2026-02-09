import streamlit as st
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# n8n Production URL
URL = "https://primary-production-b57a.up.railway.app/webhook/5e2bd96c-0881-458f-8a4f-31795b4b066c"

st.title("스마트 영수증 관리자 📋")

# 사진 업로드
img_file = st.file_uploader("영수증 사진을 업로드하세요", type=['png', 'jpg', 'jpeg'])

if img_file is not None:
    st.image(img_file, caption="업로드됨", use_container_width=True)
    
    # [수정] 버튼을 눌러야만 전송되게 하여 무한 루프 방지 및 여러 번 실행 가능하게 함
    if st.button("영수증 분석 및 전송"):
        with st.spinner("AI가 분석 중입니다..."):
            try:
                files = {
                    "data": (img_file.name, img_file.getvalue(), img_file.type)
                }
                # Production URL로 전송
                response = requests.post(URL, files=files, verify=False, timeout=30)
                
                if response.status_code == 200:
                    st.success("✅ 분석 완료! 구글 시트에 기록되었습니다.")
                    st.balloons()
                else:
                    st.error(f"서버 응답 실패: {response.status_code}")
            except Exception as e:
                st.error(f"연동 에러: {e}")

st.info("💡 새로운 사진을 올리고 버튼을 누르면 계속해서 추가 등록이 가능합니다.")
