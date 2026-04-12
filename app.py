import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(page_title="Hyeokjun's Alpha Dashboard", layout="wide")

# --- 2. 데이터 초기화 (사용자님 자산 현황 반영) ---
# 요약 데이터 (평가금 순 정렬)
summary_data = {
    "항목": ["해외배당주", "현금", "해외성장주", "예적금", "코인", "달러", "국내성장주", "어음"],
    "평가금": [97951399, 40181771, 37683442, 22620000, 11383883, 9202528, 7563500, 5346391]
}

# 상세 데이터
detail_data = {
    "계좌/플랫폼": ["한국투자", "외화보통", "미래에셋", "우리은행", "업비트", "신한은행", "미래에셋", "키움증권"],
    "종목명": ["SCHD", "현금", "QLD", "정기예금", "BTC", "USD", "국내주식", "발행어음"],
    "평가금": [97951399, 40181771, 37683442, 22620000, 11383883, 9202528, 7563500, 5346391]
}

# --- 3. 상단: 자산 관리 섹션 ---
st.title("🚀 Hyeokjun's Alpha Dashboard")

with st.container():
    st.subheader("💰 실시간 자산 현황")
    col_a, col_b = st.columns([3, 1])
    
    with col_a:
        df_sum = pd.DataFrame(summary_data).sort_values(by="평가금", ascending=False)
        edited_summary = st.data_editor(df_sum, use_container_width=True, key="main_asset_edit")
        total_val = edited_summary['평가금'].sum()
        st.metric("총 자산 합계", f"{total_val:,.0f} 원")
    
    with col_b:
        fig = px.pie(edited_summary, values='평가금', names='항목', hole=0.5, template="plotly_dark")
        fig.update_layout(margin=dict(l=20, r=20, t=20, b=20), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    # 자산 상세 더보기
    with st.expander("🔍 계좌별/종목별 세부 항목 상세 보기"):
        st.data_editor(pd.DataFrame(detail_data).sort_values(by="평가금", ascending=False), use_container_width=True, key="detail_asset_edit")

st.divider()

# --- 4. 월별 통계 리포트 ---
st.subheader("📊 월별 루틴 성취도 리포트")
month_stats = {
    "기준월": ["2026-03", "2026-04(진행중)"],
    "🔵(5개)": [15, 2],
    "🟢(3-4개)": [8, 1],
    "🟡(2개)": [5, 0],
    "🟠(1개)": [2, 0],
    "🔴(0개)": [1, 0]
}
st.table(pd.DataFrame(month_stats))

st.divider()

# --- 5. 중간 섹션: 좌(소비내역) / 우(루틴 & 캘린더) ---
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("💸 Daily Spending Log")
    if 'spending_log' not in st.session_state:
        st.session_state.spending_log = pd.DataFrame(columns=['항목', '세부내용', '금액'])
    
    with st.form("money_form", clear_on_submit=True):
        f1, f2, f3 = st.columns([1, 2, 1])
        item = f1.selectbox("구분", ["식비", "교통", "쇼핑", "자기계발", "기타"])
        detail = f2.text_input("내용")
        price = f3.number_input("금액", step=1000)
        if st.form_submit_button("지출 기록"):
            new_row = pd.DataFrame([[item, detail, price]], columns=['항목', '세부내용', '금액'])
            st.session_state.spending_log = pd.concat([st.session_state.spending_log, new_row], ignore_index=True)
    
    st.table(st.session_state.spending_log)
    st.write(f"**💰 오늘 총 지출 합계: {st.session_state.spending_log['금액'].sum():,.0f} 원**")

with col_right:
    st.subheader("🗓️ Routine Tracker")
    w_day = datetime.now().weekday()
    workout = {0:"헬스", 2:"헬스", 4:"헬스", 5:"수영"}.get(w_day, "개인정비")
    
    c1 = st.checkbox(f"운동 ({workout})")
    c2 = st.checkbox("영어: 20분 프리토킹")
    c3 = st.checkbox("영어: 구동사 3개 암기")
    c4 = st.checkbox("독서: 30분")
    c5 = st.checkbox("경제 공부: 30분")
    
    score = sum([c1, c2, c3, c4, c5])
    marks = {5:"🔵", 4:"🟢", 3:"🟢", 2:"🟡", 1:"🟠", 0:"🔴"}
    
    st.write("---")
    c_days = [str(i).zfill(2) for i in range(1, 31)]
    for i in range(0, len(c_days), 7):
        cols = st.columns(7)
        for j in range(7):
            if i+j < len(c_days):
                day_num = c_days[i+j]
                with cols[j]:
                    st.write(f"**{day_num}**")
                    if int(day_num) == datetime.now().day:
                        st.write(marks[score])
                    else:
                        st.write("⚪")

st.divider()

# --- 6. 최하단 섹션: 미국 시장 및 시사 뉴스 (카테고리별 10선) ---
st.subheader("📰 Global Market & US Insight (Top 10)")

news_data = [
    # 내 종목 관련 (2가지)
    {"cat": "My Assets", "title": "🎯 SCHD: Dividend Growth & Portfolio Analysis (Yahoo Finance)", "url": "https://finance.yahoo.com/quote/SCHD"},
    {"cat": "My Assets", "title": "🎯 QLD: Nasdaq 100 Leveraged Market Data (WSJ)", "url": "https://www.wsj.com/market-data/quotes/QLD"},
    
    # 미국 전체 경제 동향 (3가지)
    {"cat": "US Economy", "title": "🇺🇸 Market Flow: U.S. Markets and Economic Outlook (Reuters)", "url": "https://www.reuters.com/markets/us/"},
    {"cat": "US Economy", "title": "🇺🇸 Fed Watch: Central Bank Policy & Interest Rate News (CNBC)", "url": "https://www.cnbc.com/economy/"},
    {"cat": "US Economy", "title": "🇺🇸 Macro Data: Inflation & Consumer Price Index Trends (Bloomberg)", "url": "https://www.bloomberg.com/markets"},
    
    # 환율 동향 (2가지)
    {"cat": "Forex", "title": "💱 Dollar Strength: U.S. Dollar Index (DXY) Analysis (Barron's)", "url": "https://www.barrons.com/topics/foreign-exchange"},
    {"cat": "Forex", "title": "💱 FX Market: Real-time USD/KRW Exchange Rate (Investing.com)", "url": "https://www.investing.com/currencies/usd-krw"},
    
    # 미국 주요 정치 및 시사 (2가지)
    {"cat": "US Politics", "title": "⚖️ Politics: White House & U.S. Election Coverage (NYT)", "url": "https://www.nytimes.com/section/politics"},
    {"cat": "US Politics", "title": "⚖️ World Affairs: U.S. Foreign Policy & Global Impact (CNN)", "url": "https://edition.cnn.com/politics"},
    
    # 미국 핫이슈 (1가지)
    {"cat": "Hot Issue", "title": "🔥 Viral Trend: TikTok Culture & Tech Viral News (The Verge)", "url": "https://www.theverge.com/culture"}
]

for news in news_data:
    st.markdown(f"**[{news['cat']}]** 🔗 [{news['title']}]({news['url']})")

st.write("---")

# 영작 섹션
st.subheader("✍️ English Writing Practice (Daily 10)")
for i in range(1, 11):
    st.text_input(f"Sentence {i:02d}", key=f"eng_input_{i}", placeholder="Write your sentence here...")
