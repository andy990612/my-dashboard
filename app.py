import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px

# 1. 페이지 설정 (앱 상단 탭 이름과 레이아웃)
st.set_page_config(page_title="My Growth App", layout="wide")

st.title("🚀 My Smart Dashboard")

# 2. 사이드바 - 데일리 루틴 (사용자님 맞춤형)
st.sidebar.header("🗓️ Daily Routine")
r1 = st.sidebar.checkbox("오늘의 운동 (수영/야구)")
r2 = st.sidebar.checkbox("영어 문장 1개 외우기")
r3 = st.sidebar.checkbox("투자 일지 쓰기")
r4 = st.sidebar.checkbox("식단/영양제 체크")

if all([r1, r2, r3, r4]):
    st.sidebar.success("오늘의 루틴 완료! 고생하셨어요! 🏆")

# 3. 메인 화면 레이아웃
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("💰 실시간 자산 현황")
    
    # 내 포트폴리오 설정 (여기 종목과 수량을 본인 것에 맞게 수정하세요!)
    my_assets = {
        "Ticker": ["SCHD", "JEPQ", "QLD", "TSLA", "BTC-USD"],
        "Qty": [1, 1, 1, 1, 1] # 일단 1개씩으로 설정해두었습니다.
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
    st.subheader("📚 자기계발 & 영어")
    
    # 영어 공부 섹션
    st.info("💡 **Today's English**\n\n'Consistency is the key.' (꾸준함이 핵심이다.)")
    
    # 메모장
    st.subheader("📝 콘텐츠/공부 노트")
    note = st.text_area("블로그나 영상 아이디어를 적어보세요.", height=200)
    if st.button("저장하기"):
        st.success("내용이 임시 저장되었습니다.")
