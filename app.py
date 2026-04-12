import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
from streamlit_gsheets import GSheetsConnection

# 1. 페이지 설정
st.set_page_config(page_title="Alpha Dashboard", layout="wide")

# 2. 구글 시트 연결
conn = st.connection("gsheets", type=GSheetsConnection)

# 시트에서 데이터 읽어오기
try:
    # 자산 현황 시트 (Sheet1)
    df_assets = conn.read(worksheet="Sheet1", usecols=[0, 1]).dropna()
    # 루틴 기록 시트 (Sheet2 - 미리 만들어두어야 함)
    df_routine = conn.read(worksheet="Sheet2")
except:
    # 에러 발생 시 기본값 (연동 전)
    df_assets = pd.DataFrame({
        "항목": ["코인", "해외성장주", "국내성장주", "해외배당주", "예적금", "어음", "달러", "현금"],
        "평가금": [11383883, 37683442, 7563500, 97951399, 22620000, 5346391, 9202528, 40181771]
    })
    df_routine = pd.DataFrame(columns=["날짜", "점수", "지출"])

# --- 메인 로직 ---
today = datetime.now().date()
weekday = datetime.now().weekday()
workout = {0:"헬스", 2:"헬스", 4:"헬스", 5:"수영"}.get(weekday, "개인정비")

st.title(f"🚀 My Personal Alpha Dashboard")

col_left, col_right = st.columns([3, 2])

with col_left:
    st.subheader("💰 자산 실시간 관리")
    edited_assets = st.data_editor(df_assets, use_container_width=True, key="asset_editor")
    
    st.divider()
    
    st.subheader("🗓️ 루틴 체크 및 캘린더")
    c1 = st.checkbox(f"운동 ({workout})")
    c2 = st.checkbox("영어: 20분 프리토킹")
    c3 = st.checkbox("영어: 구동사 3개 암기")
    c4 = st.checkbox("독서: 30분")
    c5 = st.checkbox("경제 공부: 30분")
    
    current_score = sum([c1, c2, c3, c4, c5])
    
    # 캘린더 그리드 (좌측 하단)
    st.write("---")
    cal_cols = st.columns(7)
    # 시트 데이터 기반으로 색상 결정 로직 (예시)
    for i in range(1, 31):
        with cal_cols[(i-1)%7]:
            st.write(f"**{i:02d}**")
            # 오늘 날짜는 실시간 점수 반영, 과거는 시트 데이터 반영
            if i == today.day:
                marks = {5:"🔵", 4:"🟢", 3:"🟢", 2:"🟡", 1:"🟠", 0:"🔴"}
                st.write(marks[current_score])
            else:
                st.write("⚪")

with col_right:
    st.subheader("💸 오늘의 소비 내역")
    if 'spending' not in st.session_state:
        st.session_state.spending = pd.DataFrame(columns=['항목', '세부내용', '금액'])
    
    with st.form("spend_form", clear_on_submit=True):
        f_item = st.selectbox("항목", ["식비", "교통", "쇼핑", "자기계발", "기타"])
        f_detail = st.text_input("세부내용")
        f_amount = st.number_input("금액", step=1000)
        if st.form_submit_button("추가"):
            new_row = pd.DataFrame([[f_item, f_detail, f_amount]], columns=['항목', '세부내용', '금액'])
            st.session_state.spending = pd.concat([st.session_state.spending, new_row], ignore_index=True)
    
    st.table(st.session_state.spending)
    total_spent = st.session_state.spending['금액'].sum()
    st.metric("오늘의 총 지출", f"{total_spent:,.0f} 원")

st.divider()
st.subheader("📰 경제 동향 및 영작")
# 뉴스 요약 및 영작 섹션 (생략된 이전 코드와 동일)
