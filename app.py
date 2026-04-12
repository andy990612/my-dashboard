import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(page_title="My Growth App", layout="wide")

# --- 2. 요일별 운동 자동 설정 ---
today = datetime.now()
weekday = today.weekday()  # 0:월, 1:화, 2:수, 3:목, 4:금, 5:토, 6:일
workout_map = {0: "헬스", 2: "헬스", 4: "헬스", 5: "수영"}
today_workout = workout_map.get(weekday, "개인 정비")

# --- 3. 사이드바: 루틴 체크리스트 ---
st.sidebar.header(f"📅 {today.strftime('%Y-%m-%d')} 루틴")

with st.sidebar:
    done1 = st.checkbox(f"운동 ({today_workout})")
    done2 = st.checkbox("영어: 20분 프리토킹")
    done3 = st.checkbox("영어: 구동사 3개 외우기")
    done4 = st.checkbox("독서: 30분")
    done5 = st.checkbox("경제 공부: 30분")
    
    score = sum([done1, done2, done3, done4, done5])
    
    if st.button("오늘 루틴 저장하기"):
        st.balloons()
        st.success(f"총 {score}개 완료! 대단해요!")

# --- 4. 메인 화면 레이아웃 ---
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("💰 실시간 자산 현황")
    # 종목과 수량을 본인 것에 맞게 나중에 수정하세요
    my_assets = {"Ticker": ["SCHD", "JEPQ", "QLD", "TSLA", "BTC-USD"], "Qty": [1, 1, 1, 1, 1]}
    
    if st.button('시세 새로고침'):
        with st.spinner('가격을 불러오는 중...'):
            df = pd.DataFrame(my_assets)
            prices = {t: yf.Ticker(t).history(period="1d")['Close'].iloc[-1] for t in my_assets["Ticker"]}
            df['Price'] = df['Ticker'].map(prices)
            df['Value'] = df['Qty'] * df['Price']
            st.metric("Total Asset Value", f"${df['Value'].sum():,.2f}")
            fig = px.pie(df, values='Value', names='Ticker', hole=0.4, template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(df.style.format({"Price": "{:.2f}", "Value": "{:,.2f}"}))

with col2:
    st.subheader("🗓️ Monthly Growth Tracker")
    
    # 상단 범례 (심플하게)
    st.write("🔵5 | 🟢3-4 | 🟡2 | 🟠1 | 🔴0")
    
    # 7열 그리드 달력 만들기
    days = [str(i).zfill(2) for i in range(1, 31)] # 1~30일
    # 예시 성취도 (나중에 데이터 연동 시 실제 값으로 바뀜)
    perf = ["🔵", "🟢", "🟢", "🟡", "🔴", "🔵", "🟢"] * 5 

    # 7개씩 끊어서 한 줄씩 출력
    for i in range(0, len(days), 7):
        cols = st.columns(7)
        for j in range(7):
            if i + j < len(days):
                with cols[j]:
                    st.write(f"**{days[i+j]}**")
                    st.write(perf[i+j])
    
    st.divider()
    st.subheader("📝 Today's Note")
    st.text_area("영어 문장이나 아이디어를 기록하세요.", height=150)
