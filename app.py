import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px

# 1. 자산 데이터 설정 (티커와 보유 수량 입력)
# 여기에 본인이 실제 보유한 수량을 입력하세요.
portfolio_data = {
    "Ticker": ["SCHD", "JEPQ", "QLD", "TSLA", "BTC-USD"],
    "Quantity": [100, 50, 30, 10, 0.1]  # 예시 수량
}

def get_current_prices(tickers):
    prices = {}
    for ticker in tickers:
        try:
            data = yf.Ticker(ticker)
            # 실시간에 가까운 최신 종가 가져오기
            price = data.history(period="1d")['Close'].iloc[-1]
            prices[ticker] = price
        except:
            prices[ticker] = 0
    return prices

st.subheader("📊 Real-time Portfolio Monitor")

# 시세 불러오기 버튼
if st.button('Refresh Market Data'):
    with st.spinner('Fetching latest prices...'):
        current_prices = get_current_prices(portfolio_data["Ticker"])
        
        # 데이터프레임 구성
        df = pd.DataFrame(portfolio_data)
        df['Current Price'] = df['Ticker'].map(current_prices)
        df['Total Value ($)'] = df['Quantity'] * df['Current Price']
        
        # 2. 결과 출력 및 시각화
        total_portfolio_value = df['Total Value ($)'].sum()
        st.metric("Total Asset Value", f"${total_portfolio_value:,.2f}")
        
        col1_1, col1_2 = st.columns(2)
        
        with col1_1:
            st.dataframe(df.style.format({"Current Price": "{:.2f}", "Total Value ($)": "{:,.2f}"}))
            
        with col1_2:
            fig = px.pie(df, values='Total Value ($)', names='Ticker', 
                         title='Asset Distribution', hole=0.5)
            st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Click the button to load real-time market data.")
