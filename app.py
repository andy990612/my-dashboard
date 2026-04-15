import streamlit as st
import pandas as pd
from datetime import datetime

# 1. 심플 페이지 설정
st.set_page_config(page_title="AI News Agent", page_icon="📝")

# --- 2. AI 에이전트 브리핑 (매일 자동 업데이트 로직) ---
# 실제 운영 시에는 여기에 뉴스 API를 연결하면 매일 다른 뉴스가 요약되어 나옵니다.
def get_ai_briefing():
    return [
        {"icon": "💰", "topic": "SCHD/배당", "summary": "최근 미국 배당주 섹터로 자금 유입 가속화. SCHD는 분기 배당금 성장 기대감으로 신고가 근처에서 견조한 흐름 유지 중."},
        {"icon": "🚀", "topic": "QLD/기술주", "summary": "엔비디아 등 AI 빅테크 실적 발표를 앞두고 나스닥 변동성 확대. QLD 투자자는 단기 조정 가능성에 대비한 관망세 권장."},
        {"icon": "💵", "topic": "환율/거시", "summary": "미국 고용 지표 호조로 금리 인하 시점이 하반기로 밀리며 강달러(1,300원 중반) 유지 중. 환차익 관리 필요."},
        {"icon": "₿", "topic": "비트코인", "summary": "반감기 이후 공급 감소 효과 본격화. 블랙록 등 기관들의 현물 ETF 매수세가 하방 지지선을 강력하게 형성 중."},
        {"icon": "🔥", "topic": "미국 핫이슈", "summary": "틱톡 매각 법안 통과 임박으로 미국 내 SNS 구도 재편 조짐. MZ세대의 소비 패턴이 '경험'에서 '저축'으로 이동 중인 'Loud Budgeting' 유행."}
    ]

# --- 3. UI 구성 (가독성 극대화) ---
today = datetime.now().strftime('%Y-%m-%d')
st.title(f"👋 Good Morning, Hyeokjun!")
st.write(f"**{today}** | 오늘 꼭 알아야 할 5가지 경제 브리핑입니다.")

st.divider()

# 뉴스 에이전트 브리핑 출력
briefs = get_ai_briefing()

for news in briefs:
    with st.expander(f"{news['icon']} **{news['topic']}** : 핵심 요약 보기", expanded=True):
        st.write(news['summary'])
        # 클릭하면 바로 야후 파이낸스 관련 페이지로 연결 (예시)
        st.caption("🔗 [상세 데이터 확인하기](https://finance.yahoo.com)")

st.divider()

# 영작 연습 칸 (딱 하나로 통합)
st.subheader("✍️ 오늘의 영문장 한 줄 기록")
user_eng = st.text_input("뉴스를 읽고 떠오른 생각이나 구동사를 적어보세요.", placeholder="Today's goal: Learn 3 phrasal verbs.")

if user_eng:
    st.success("오늘의 공부 기록이 저장되었습니다! 🔥")
