import streamlit as st
from openai import OpenAI
import time

MODEL_LIST = ["gpt-4o", "gpt-3.5-turbo", "gpt-4-turbo"]
assistant_id = "asst_Dlr6YRJen7llwFxT393E5noC"

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
	
    with st.expander("1. 종목별 투자 아이디어 요약"):
        st.code("""1. 최종목표: '종목명'의 투자 아이디어 요약
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
13. 현재 날짜 및 시간 : [2024년 7월 15일]
14. 출처표시 : 하지 말 것""", language="plaintext")

    with st.expander("2. 종목별 최근 주가 변동 원인 설명"):
        st.code("""1. 최종목표: '종목명'의 최근 주가 변동 원인 및 전망에 대한 코멘트 작성
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
13. 현재 날짜 및 시간 : [2024년 7월 15일]
14. 출처표시 : 하지 말 것""", language="plaintext")

    with st.expander("3. VIS 보고서 내용 요약"):
        st.code("""1. 최종목표 : 가장 최근 '종목명' 보고서 내용 요약 및 정리
2. 추가 데이터 제공 여부 : RAG 목적의 OpenAI Assistant API Vector DB
3. 역할부여 : DB를 전체적으로 빠짐없이 뒤져서 요청한 정보를 자연어 유사어와 전문용어까지 고려하여 찾아올 수 있는 검색엔진이자, 체계적이고 깔끔하게 정리를 잘 해내는 애널리스트
4. 글의 종류 : 코멘트
5. 결과물의 형식 : 가장 최근에 작성된 보고서의 내용을 Bullet Point로 요약정리, 내용이 복잡하고 길 경우에는 Sub-topic별로 구분 (Sub-topic을 구분할 경우에는 그 직전에 줄바꿈 하여 가독성을 높일 것)
6. 필수 포함 내용 : 종목명, 담당 애널리스트 이름, 작성일자, 목표주가, 과거에 작성된 동일 종목에 대한 보고서 목록이 있을 경우 작성일자, 제목, 담당 애널리스트 이름, 목표주가를 추가하여 표 형식으로 작성하고 작성일자를 기준으로 내림차순 정렬 할 것 / 필수 포함 내용은 결과물의 가장 처음에 표시
7. 문체 : 개조식
8. 작성언어 : 한국어
9. 제한사항 : 구체적인 수치는 반드시 Vector DB 내에서만 직접적으로 인용, 숫자는 절대로 자의적으로 반올림/올림/버림 하지 말고 그대로 표시할 것
10. 출처표시 : 결과물의 마지막 부분에만 표시
11. 현재날짜 : [2024년 7월 14일]""", language="plaintext")
	
    with st.expander("4. 시황/전망 코멘트 작성"):
        st.code("""1. 최종목표: '국내 증시에 대한 단기 및 중기 전망, 그리고 펀드의 대응 계획에 관한 코멘트 작성'
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
13. 현재 날짜 및 시간 : [2024년 7월 15일]
14. 출처표시 : 하지 말 것""", language="plaintext")


st.title("💬 AI for VIP Information System")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "저는 VIP AI 입니다. VIS DB의 내용을 구석구석 뒤져서 최선을 다해 답변드리겠습니다. VIS DB에 관련된 내용만 질문해주세요."}]

model: str = st.selectbox("Model", options=MODEL_LIST)  # type: ignore

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    if not thread_id:
        st.info("Please add your Thread ID to continue.")
        st.stop()
        
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    response = client.beta.threads.messages.create(
        thread_id,
        role="user",
        content=prompt
        )
    
    run = client.beta.threads.runs.create(
        thread_id = thread_id,
        assistant_id = assistant_id,
        model = model
        )

    run_id = run.id

    while True:
        run = client.beta.threads.runs.retrieve(
            thread_id = thread_id,
            run_id = run_id
            )
        if run.status == "completed":
            break
        else:
            time.sleep(1)

    thread_messages = client.beta.threads.messages.list(thread_id)
    msg = thread_messages.data[0].content[0].text.value

    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
