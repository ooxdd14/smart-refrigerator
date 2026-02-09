import streamlit as st
from PIL import Image
import requests
import io
import urllib3

# SSL 경고 무시
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# n8n Production URL
URL = "https://primary-production-b57a.up.railway.app/webhook/5e2bd96c-0881-458f-8a4f-31795b4b066c"

st.title("스마트 영수증 관리자 📋")

# 1. 전송 상태를 기억할 금고(session_state) 초기화
if 'last_uploaded_file' not in st.session_state:
    st.session_state.last_uploaded_file = None

img_file = st.file_uploader("영수증 사진을 선택하세요", type=['png', 'jpg', 'jpeg'])

if img_file is not None:
    # 2. 새로운 파일이 올라왔는지 확인
    if st.session_state.last_uploaded_file != img_file.name:
        
        try:
            image = Image.open(img_file)
            st.image(image, caption="업로드됨", use_container_width=True)
            
            # 자동 전송 시작
            with st.spinner("자동 분석 중..."):
                buf = io.BytesIO()
                image.convert("RGB").save(buf, format="JPEG")
                byte_im = buf.getvalue()

                files = {"data": (img_file.name, byte_im, "image/jpeg")}
                response = requests.post(URL, files=files, verify=False, timeout=30)
                
                if response.status_code == 200:
                    # 3. 전송 성공 시 파일 이름을 저장해서 중복 전송 방지
                    st.session_state.last_uploaded_file = img_file.name
                    st.success("✅ 자동으로 전송되었습니다!")
                    st.balloons()
                else:
                    st.error(f"전송 실패: {response.status_code}")
                    
        except Exception as e:
            st.error(f"오류 발생: {e}")
    else:
        # 이미 전송한 파일일 경우 화면에 표시만 함
        image = Image.open(img_file)
        st.image(image, caption="분석 완료된 영수증", use_container_width=True)
        st.info("💡 이미 처리가 완료된 사진입니다.")

# 새로 하기 버튼 (필요할 때 세션 초기화)
if st.button("초기화 (새 영수증)"):
    st.session_state.last_uploaded_file = None
    st.rerun()
