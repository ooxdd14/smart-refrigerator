import streamlit as st
from PIL import Image
import requests
import io
import urllib3

# SSL 경고 무시
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# [체크] 주소 중간에 'webhook-test'가 아니라 'webhook'인지 백만번 확인!
URL = "https://primary-production-b57a.up.railway.app/webhook/5e2bd96c-0881-458f-8a4f-31795b4b066c"

st.title("스마트 영수증 관리자 📋")

# 세션 초기화 (기억 장치)
if 'last_file' not in st.session_state:
    st.session_state.last_file = None

img_file = st.file_uploader("영수증 사진을 선택하세요", type=['png', 'jpg', 'jpeg'])

if img_file is not None:
    # 1. 화면에 일단 사진 띄우기
    image = Image.open(img_file)
    st.image(image, caption="업로드됨", use_container_width=True)

    # 2. 새로운 파일일 때만 전송 실행
    if st.session_state.last_file != img_file.name:
        with st.status("🚀 n8n으로 데이터 전송 중...", expanded=True) as status:
            try:
                # 이미지 세탁 (RGB 변환)
                buf = io.BytesIO()
                image.convert("RGB").save(buf, format="JPEG")
                byte_im = buf.getvalue()

                files = {"data": (img_file.name, byte_im, "image/jpeg")}
                
                # 전송
                response = requests.post(URL, files=files, verify=False, timeout=30)
                
                if response.status_code == 200:
                    st.session_state.last_file = img_file.name # 성공 기록
                    status.update(label="✅ 전송 완료!", state="complete", expanded=False)
                    st.success(f"데이터가 성공적으로 전송되었습니다! ({img_file.name})")
                    st.balloons()
                else:
                    status.update(label="❌ 전송 실패", state="error")
                    st.error(f"서버 응답 오류: {response.status_code}")
                    st.info("n8n에서 'Active' 스위치가 켜져 있는지 다시 확인하세요.")
            except Exception as e:
                status.update(label="⚠️ 연결 오류 발생", state="error")
                st.error(f"에러 내용: {e}")
    else:
        st.info("💡 이 영수증은 이미 처리가 완료되었습니다.")

# 초기화 버튼
if st.button("다른 영수증 올리기"):
    st.session_state.last_file = None
    st.rerun()
