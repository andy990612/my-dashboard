import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px
from datetime import datetime
from streamlit_calendar import calendar

# 1. 페이지 설정
st.set_page_config(page_title="My Growth App", layout="wide")

# --- 2. 요일별 운동 자동 설정 로직 ---
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
        st.success(f"총 {score}개 완료! (데이터 연동 전)")

# --- 4. 메인 화면 레이아웃 ---
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("💰 실시간 자산 현황")
    
    # 여기에 본인이 보유한 티커와 수량을 입력하세요
    my_assets = {
        "Ticker": ["SCHD", "JEPQ", "QLD", "TSLA", "BTC-USD"],
        "Qty": [1, 1, 1, 1, 1] 
    }
    
    if st.button('시세 새로고침'):
        with st.spinner('가격을 불러오는 중...'):
            tickers = my_assets["Ticker"]
            prices = {}
            for t in tickers:
                prices[t] = yf.Ticker(t).history(period="1d")['Close'].iloc[-1]
            
            df = pd.DataFrame(my_assets)
            df['Price'] = df['Ticker'].map(prices)
            df['Value'] = df['Qty'] * df['Price']
            
            total_val = df['Value'].sum()
            st.metric("총 자산 가치", f"${total_val:,.2f}")
            
            fig = px.pie(df, values='Value', names='Ticker', hole=0.4)
            st.plotly_chart(fig, use_container_width=True)
            st.table(df)

with col2:
    st.subheader("🗓️ 월간 달성도 캘린더")
    
    # 성취도별 예시 데이터 (실제 저장 기능 구현 전 예시)
    calendar_events = [
        {"title": "🔵", "start": "2026-04-11", "color": "#1E90FF"}, # 오늘 날짜 예시
    ]
    
    calendar_options = {
        "headerToolbar": {"left": "today", "center": "title", "right": "prev,next"},
        "initialView": "dayGridMonth",
    }
    
    calendar(events=calendar_events, options=calendar_options)
    
    st.markdown("""
    **[범례]** 🔵5개(완벽) | 🟢3-4개 | 🟡2개 | 🟠1개 | 🔴0개
    """)

    st.divider()
    st.subheader("📝 공부 노트")
    note = st.text_area("아이디어를 적어보세요.", height=150)
