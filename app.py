import streamlit as st
import requests
import urllib3

# SSL 경고 무시
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# n8n Webhook URL (반드시 Production URL로 넣으세요!)
URL = "https://primary-production-b57a.up.railway.app/webhook/5e2bd96c-0881-458f-8a4f-31795b4b066c"

# 1. [차이점] 결과값을 저장할 '금고(session_state)' 만들기
if 'ocr_done' not in st.session_state:
    st.session_state['ocr_done'] = False

st.title("스마트 영수증 관리자 📋")

img_file = st.file_uploader("영수증 사진을 업로드하세요", type=['png', 'jpg', 'jpeg'])

if img_file is not None:
    st.image(img_file, caption="업로드됨", use_container_width=True)
    
    # 2. [차이점] 이미 분석이 끝났다면 다시 전송하지 않도록 조건 추가
    if not st.session_state['ocr_done']:
        with st.spinner("분석 중..."):
            try:
                files = {
                    "data": ("receipt.jpg", img_file.getvalue(), "image/jpeg")
                }
                response = requests.post(URL, files=files, verify=False)
                
                if response.status_code == 200:
                    # 3. [차이점] 성공했다는 사실을 금고에 저장
                    st.session_state['ocr_done'] = True
                    st.success("전송 완료!")
                    # 필요하다면 응답 내용도 보여줍니다
                    st.balloons() 
                else:
                    st.error(f"오류 발생: {response.status_code}")
            except Exception as e:
                st.error(f"에러: {e}")

# 4. [차이점] 분석이 완료된 상태라면 계속 "완료" 메시지를 띄워둠
if st.session_state['ocr_done']:
    st.info("✅ n8n으로 데이터 전송 및 구글 시트 기록이 완료되었습니다.")
