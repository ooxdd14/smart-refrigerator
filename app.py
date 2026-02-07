import streamlit as st
import requests

# --- 1. 설정: n8n에서 복사한 주소를 여기에 넣으세요 ---
# 반드시 따옴표("") 안에 주소를 넣어야 합니다!
URL = "https://primary-production-b57a.up.railway.app/webhook-test/5e2bd96c-0881-458f-8a4f-31795b4b066c"

st.set_page_config(page_title="스마트 냉장고 관리자", page_icon="🧾")

st.title("🧾 영수증 사진 업로드")
st.write("갤러리에서 영수증 사진을 선택하면 AI가 분석을 시작합니다.")

# --- 2. 파일 업로드 칸 (갤러리 사진 선택) ---
img_file = st.file_uploader("영수증 사진을 골라주세요", type=['png', 'jpg', 'jpeg'])

# 사진이 선택되면 실행되는 구역
if img_file:
    # 화면에 내가 올린 사진 미리보기
    st.image(img_file, caption='선택한 영.수.증', use_container_width=True)
    
    # 전송 버튼을 만들거나, 선택하자마자 바로 보낼 수 있습니다.
    # 여기서는 선택하자마자 바로 n8n으로 쏘도록 설정했습니다.
    with st.spinner("n8n 서버로 안전하게 보내는 중..."):
        try:
            # 파일을 n8n이 받을 수 있는 형태로 변환
           files = {"data": ("receipt.jpg", img_file.getvalue(), "image/jpeg")}
           response = requests.post(URL, files=files) # 위아래 줄 시작 위치가 같아야 함!
            
            # n8n Webhook으로 전송
            response = requests.post(URL, files=files)
            
            if response.status_code == 200:
                st.success("✅ 전송 성공! n8n 워크플로우를 확인하세요.")
                st.balloons() # 축하 풍선 효과
            else:
                st.error(f"❌ 전송 실패 (에러 코드: {response.status_code})")
                st.info("n8n의 Webhook 노드가 'Listen for Test Event' 상태인지 확인해 보세요.")
                
        except Exception as e:
            st.error(f"⚠️ 연결 중 오류 발생: {e}")

st.divider()
st.caption("Tip: 사진을 올린 후 n8n 화면에서 데이터가 들어오는지 새로고침하며 확인하세요.")



