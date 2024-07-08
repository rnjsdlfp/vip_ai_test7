import streamlit as st
from openai import OpenAI
import time

MODEL_LIST = ["gpt-4o", "gpt-3.5-turbo", "gpt-4-turbo"]
assistant_id = "asst_Dlr6YRJen7llwFxT393E5noC"

# JavaScript 함수 정의
js = """
<script>
function copyToPrompt(text) {
    const textarea = document.querySelector('.stTextInput textarea');
    if (textarea) {
        textarea.value = text;
        textarea.dispatchEvent(new Event('input', { bubbles: true }));
    }
}
</script>
"""

# JavaScript를 페이지에 삽입
st.components.v1.html(js, height=0)

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")

    client = OpenAI(api_key=openai_api_key)

    thread_id = st.text_input("Thread ID")
    thread_btn = st.button("Create a new thread")

    if thread_btn:
        thread = client.beta.threads.create()
        thread_id = thread.id
    
        st.subheader(f"{thread_id}")
        st.info("Thread created!")

    st.markdown("---")  # 구분선 추가
    st.subheader("Pre-written Prompt Templates")
	
    for i, (title, content) in enumerate([
        ("1. 종목별 투자 아이디어 요약", """1. 최종목표: '종목명' 투자 아이디어 요약
2. 추가 데이터 제공 여부 : RAG 목적의 OpenAI Assistant API Vector DB
3. 참고할 데이터 범위 : RAG 용도의 Vector DB 전체를 우선적으로 참고하고, 나머지는 이미 학습된 데이터 및 실시간 검색 결과 참고
4. 역할부여 : 매우 똑똑하고 전문적인 금융 전문가 애널리스트, 가치투자자 성향 보유
5. 배경정보 : 시장 변동성 확대에 따라 펀드 판매사 담당자 및 고객들의 우려 증가
6. 글의 종류 : 코멘트
7. 결과물의 형식 : Bullet Point 3~5개, Sub-topic은 표시하지 말 것. 
8. 선호하는 결과물의 내용 구성 (해당 종목이 포함된 산업의 구조적 변화 및 방향성, 해당 종목의 개별적인 투자 아이디어, 중장기 전망)
9. 작성언어 : 한국어
10. 문체 : 개조식
11. 제한사항 : 구체적인 수치는 가급적 피할 것, 필요시 반드시 첨부된 DB 내에서만 참고, 목표주가 및 기대수익률에 대한 내용 제외할 것
12. 답변에 대한 해설 : 불필요
13. 현재 날짜 및 시간 : 2024년 7월 7일
14. 출처표시 : 하지 말 것"""),
        ("2. 종목별 최근 주가 변동 원인 설명", """1. 최종목표: '종목명' 최근 주가 하락 원인 및 전망에 대한 코멘트 작성
2. 추가 데이터 제공 여부 : RAG 목적의 OpenAI Assistant API Vector DB
3. 참고할 데이터 범위 : RAG 용도의 Vector DB 전체를 우선적으로 참고하고, 나머지는 이미 학습된 데이터 및 실시간 검색 결과 참고
4. 역할부여 : 매우 똑똑하고 전문적인 금융 전문가 애널리스트, 가치투자자 성향 보유
5. 배경정보 : 주가 변동성 확대에 따라 펀드 판매사 담당자 및 고객들의 우려 증가
6. 글의 종류 : 코멘트
7. 결과물의 형식 : Bullet Point 3~5개, Sub-topic은 표시하지 말 것. 
8. 선호하는 결과물의 내용 구성 (해당 종목이 포함된 산업의 구조적 변화 및 방향성, 해당 종목의 개별적이고 구체적인 핵심 이슈, 중장기 전망)
9. 작성언어 : 한국어
10. 문체 : 개조식
11. 제한사항 : 구체적인 수치는 가급적 피할 것, 필요시 반드시 첨부된 DB 내에서만 참고
12. 답변에 대한 해설 : 불필요
13. 현재 날짜 및 시간 : 2024년 7월 7일
14. 출처표시 : 하지 말 것"""),
        ("3. 시황/전망 코멘트 작성", """1. 최종목표: '국내 증시에 대한 단기 및 중기 전망, 그리고 펀드의 대응 계획에 관한 코멘트 작성'
2. 추가 데이터 제공 여부 : RAG 목적의 OpenAI Assistant API Vector DB
3. 참고할 데이터 범위 : RAG 용도의 Vector DB 전체를 우선적으로 참고하고, 나머지는 이미 학습된 데이터 및 실시간 검색 결과 참고
4. 역할부여 : 매우 똑똑하고 전문적인 금융 전문가 애널리스트, 가치투자자 성향 보유
5. 배경정보 : 시장 변동성 확대에 따라 펀드 판매사 담당자 및 고객들의 우려 증가
6. 글의 종류 : 코멘트
7. 문단 구성 : 총 3개의 문단
	- 문단1 : 글로벌 매크로 상황, 국내 경제 상황, 주식시장 전반적인 시황 관련 내용
	- 문단2 : 최근 분기 특이사항 관련 내용
	- 문단3 : 현재의 이슈, 단기적 전망 관련 내용
8. 총 길이 : 600~1000 글자
9. 작성언어 : 한국어
10. 문체 : 개조식, 명사형 종결어미 사용
11. 제한사항 : 구체적인 수치는 가급적 피할 것, 필요시 반드시 첨부된 DB 내에서만 참고, Prompt의 내용을 그대로 결과물의 내용에 포함하지 말 것
12. 답변에 대한 해설 : 불필요
13. 현재 날짜 및 시간 : 2024년 7월 7일
14. 출처표시 : 하지 말 것""")
    ]):
        with st.expander(title):
            st.markdown(f"""
            <div onclick="copyToPrompt(`{content}`)" style="cursor: pointer;">
            <pre><code>{content}</code></pre>
            </div>
            """, unsafe_allow_html=True)

# 나머지 코드는 그대로 유지
