import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_calendar import calendar

st.set_page_config(page_title="Growth Dashboard", layout="wide")

# --- 1. 요일별 운동 자동 설정 ---
today = datetime.now()
weekday = today.weekday()  # 0:월, 1:화, 2:수, 3:목, 4:금, 5:토, 6:일

workout_map = {0: "헬스", 2: "헬스", 4: "헬스", 5: "수영"}
today_workout = workout_map.get(weekday, "개인 정비") # 월수금토 외에는 개인 정비로 표시

# --- 2. 사이드바 루틴 설정 ---
st.sidebar.header("📅 Daily Routine")
st.sidebar.write(f"오늘은 **{today.strftime('%Y-%m-%d')}** 입니다.")

with st.sidebar:
    st.subheader("체크리스트")
    done1 = st.checkbox(f"운동 ({today_workout})")
    done2 = st.checkbox("영어: 20분 프리토킹")
    done3 = st.checkbox("영어: 구동사 3개 외우기")
    done4 = st.checkbox("독서: 30분")
    done5 = st.checkbox("경제 공부: 30분")
    
    # 완료 개수 계산
    score = sum([done1, done2, done3, done4, done5])
    
    if st.button("오늘 루틴 저장하기"):
        # 실제 운영 시에는 DB나 파일에 저장하는 로직이 필요하지만, 
        # 우선 현재 세션에서 성공 메시지만 띄웁니다.
        st.success(f"오늘 {score}개 완료! 저장되었습니다.")

# --- 3. 메인 화면 ---
col1, col2 = st.columns([2, 3])

with col1:
    st.subheader("💰 자산 현황")
    st.info("이전 코드를 유지하거나 시세를 확인하는 버튼을 여기에 배치하세요.")
    # (기존에 드린 자산 시세 코드를 이 부분에 넣으시면 됩니다.)

with col2:
    st.subheader("🗓️ 월간 달성도 캘린더")
    
    # 성취도별 색상 정의
    # 파랑(5개), 초록(4~3개), 노랑(2개), 주황(1개), 빨강(0개)
    # 실제 데이터 연동 전 예시 마킹 데이터입니다.
    calendar_events = [
        {"title": "🔵", "start": "2026-04-01", "color": "#1E90FF"}, # 5개
        {"title": "🟢", "start": "2026-04-02", "color": "#32CD32"}, # 3~4개
        {"title": "🟡", "start": "2026-04-03", "color": "#FFD700"}, # 2개
        {"title": "🟠", "start": "2026-04-04", "color": "#FF8C00"}, # 1개
        {"title": "🔴", "start": "2026-04-05", "color": "#FF4500"}, # 0개
    ]
    
    calendar_options = {
        "editable": "false",
        "selectable": "true",
        "headerToolbar": {
            "left": "today",
            "center": "title",
            "right": "prev,next",
        },
    }
    
    calendar(events=calendar_events, options=calendar_options)
    
    st.markdown("""
    **[범례]** 🔵 완료 5개 | 🟢 완료 3-4개 | 🟡 완료 2개 | 🟠 완료 1개 | 🔴 완료 0개
    """)
        st.success("내용이 임시 저장되었습니다.")
