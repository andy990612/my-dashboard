import streamlit as st
import pandas as pd
from datetime import datetime

# 1. 페이지 설정 (심플하게)
st.set_page_config(page_title="Alpha News Agent", page_icon="📰")

# --- 2. 뉴스 에이전트 로직 (매일 업데이트될 뉴스 데이터) ---
# 실제 운영 시에는 뉴스 API나 크롤링 기능을 연결할 수 있습니다.
today = datetime.now().strftime('%Y년 %m월 %d일')

news_data = [
    {
        "category": "My Assets",
        "title": "SCHD 배당 성장률 발표: 고배당주 포트폴리오의 안정적 흐름",
        "summary": "금리 인하 기대감 속에 배당 성장주인 SCHD로의 자금 유입이 지속되고 있으며, 주요 구성 종목의 실적이 안정세를 보이고 있습니다.",
        "link": "https://finance.yahoo.com/quote/SCHD"
    },
    {
        "category": "US Market",
        "title": "나스닥 100(QLD 관련) 변동성 확대: 기술주 실적 발표 대기 중",
        "summary": "AI 관련 대형주들의 실적 발표를 앞두고 시장이 관망세를 유지 중입니다. QLD 등 레버리지 상품 투자 시 변동성에 주의가 필요합니다.",
        "link": "https://www.wsj.com/market-data/quotes/QLD"
    },
    {
        "category": "Economy",
        "title": "미 연준 금리 동결 가능성 시사... 환율 변동성 주목",
        "summary": "최신 고용 지표가 예상보다 견조하게 나오면서 조기 금리 인하 기대가 다소 꺾였습니다. 달러 강세 압력이 커질 수 있습니다.",
        "link": "https://www.cnbc.com/economy/"
    },
    {
        "category": "Crypto",
        "title": "비트코인(BTC) 반감기 이후 기관 매수세 유입 가속화",
        "summary": "현물 ETF 승인 이후 블랙록 등 거대 자산운용사의 매입이 계속되며 장기 지지선을 형성하고 있다는 분석입니다.",
        "link": "https://finance.yahoo.com/quote/BTC-USD"
    },
    {
        "category": "Hot Issue",
        "title": "미국 내 틱톡 금리 법안 통과 여부와 MZ세대 소비 트렌드",
        "summary": "SNS 관련 규제 소식과 더불어 최근 미국 젊은 층 사이에서 '저축 챌린지'가 유행하며 새로운 소비 문화가 형성되고 있습니다.",
        "link": "https://www.theverge.com/culture"
    }
]

# --- 3. UI 레이아웃 ---
st.header(f"🤖 AI News Agent: {today}")
st.write("사용자님의 포트폴리오와 시장 상황을 분석해 선별한 오늘의 5가지 소식입니다.")

st.divider()

# 뉴스 카드 형태로 출력
for i, news in enumerate(news_data):
    with st.container():
        col1, col2 = st.columns([1, 4])
        with col1:
            st.caption(f"TOP {i+1}")
            st.markdown(f"`{news['category']}`")
        with col2:
            st.subheader(news['title'])
            st.write(news['summary'])
            st.markdown(f"[기사 원문 보기]({news['link']})")
        st.divider()

# 사이드바: 간단한 영작 연습
st.sidebar.subheader("✍️ 오늘의 영작 1문장")
st.sidebar.info("오늘 본 뉴스 중 인상 깊은 내용을 영어로 정리해 보세요.")
st.sidebar.text_area("Your sentence:", placeholder="Ex: SCHD is a great dividend growth ETF.")
if st.sidebar.button("오늘 공부 완료"):
    st.sidebar.success("체크 완료! 🔵")
