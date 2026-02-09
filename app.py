import streamlit as st
from PIL import Image
import requests
import io
import urllib3

# SSL 경고 무시
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# [체크] 주소 마지막 확인! (webhook-test 아님, webhook임)
URL = "https://primary-production-b57a.up.railway.app/webhook/5e2bd96c-0881-458f-8a4f-31795b4b066c"

st.title("스마트 영수증 관리자 📋")

img_file = st.file_uploader("영수증 사진을 선택하세요", type=['png', 'jpg', 'jpeg'])

if img_file is not None:
    # 1. 사진 무조건 띄우기
    image = Image.open(img_file)
    st.image(image, caption="분석 중인 사진", use_container_width=True)

    # 2. 사진이 올라오는 순간 무조건 전송 프로세스 시작
    # (session_state 조건문을 아예 뺐습니다)
    with st.spinner("🚀 n8n 서버로 강제 전송 중..."):
        try:
            buf = io.BytesIO()
            image.convert("RGB").save(buf, format="JPEG")
            byte_im = buf.getvalue()

            files = {"data": (img_file.name, byte_im, "image/jpeg")}
            
            # n8n으로 전송
            response = requests.post(URL, files=files, verify=False, timeout=30)
            
            if response.status_code == 200:
                st.success(f"✅ 전송 성공! 구글 시트를 확인하세요. ({img_file.name})")
                st.balloons()
            else:
                st.error(f"❌ 서버 응답 실패: {response.status_code}")
                st.info("n8n 사이트에서 워크플로우 상단 'Active'가 초록색인지 꼭 보세요!")
        except Exception as e:
            st.error(f"⚠️ 연결 오류: {e}")

# 혹시 모르니 강제 새로고침 버튼
if st.button("앱 다시 시작"):
    st.rerun()
