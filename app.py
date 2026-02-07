import streamlit as st
import requests

URL = "https://primary-production-b57a.up.railway.app/webhook-test/5e2bd96c-0881-458f-8a4f-31795b4b066c"

st.title("🧾 스마트 영수증 관리자")
st.write("영수증을 업로드하면 AI가 냉장고에 자동 등록합니다.")

# 1. 사진 업로드/촬영 칸 (모바일 접속 시 카메라 자동 실행)
img_file = st.camera_input("영수증을 촬영하거나 업로드하세요")

if img_file:
    with st.spinner("Upstage AI가 분석 중..."):
        # 2. Upstage OCR API 호출 부분
        # (이미지 파일을 업스테이지 서버로 보내 데이터를 받아옴)
        api_key = "YOUR_UPSTAGE_API_KEY"
        headers = {"Authorization": f"Bearer {api_key}"}
        files = {"document": img_file.getvalue()}
        
        # 실제 API 호출
        response = requests.post("https://api.upstage.ai/v1/document-ai/ocr", headers=headers, files=files)
        
        if response.status_code == 200:
            st.success("데이터 추출 완료!")
            # 여기서 받아온 데이터(품목, 날짜)를 보여줌
            # 예: "우유 / 유통기한: 2026-02-14"
        else:

            st.error("AI 연결 오류가 발생했습니다.")


