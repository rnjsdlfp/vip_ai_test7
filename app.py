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

    with st.expander("3. VIS 보고서 내용 요약(서술식)"):
        st.code("""1. 최종목표 : 가장 최근 '종목명' 보고서 내용 요약 및 정리
2. 추가 데이터 제공 여부 : RAG 목적의 OpenAI Assistant API Vector DB
3. 참고할 데이터 범위 : 먼저 최종목표에 부합하는 데이터를 Vector DB에서 찾고, 특정 보고서를 지정하였다면 해당 보고서의 Chunk 내용만을 참고하고 나머지 Vector DB 및 사전 학습된 내용은 참고 범위에서 배제
4. 역할부여 : DB를 전체적으로 빠짐없이 뒤져서 요청한 정보를 자연어 유사어와 전문용어까지 고려하여 찾아올 수 있는 검색엔진이자, 체계적이고 깔끔하게 정리를 잘 해내는 애널리스트
5. 글의 종류 : 코멘트
6. 결과물의 형식 : 가장 최근에 작성된 보고서의 내용을 서술식으로 요약정리. 수치적인 내용 보다는, 핵심 개념과 논리 위주로 작성. 내용이 복잡하고 길 경우에는 Sub-topic별로 구분 (Sub-topic을 구분할 경우에는 그 직전에 줄바꿈 하여 가독성을 높일 것)
7. 결과물의 분량 : 700~1200 글자 범위 내
8. 필수 포함 내용 : 종목명, 작성자, 작성일, 목표가, 기대수익률, 투자의견 / 필수 포함 내용은 결과물의 가장 처음에 표시
9. 문체 : 개조식, 명사형종결어미
10. 작성언어 : 한국어
11. 제한사항 : 가급적 수치는 내용에 포함하지 않도록 하고, 꼭 필요한 수치는 반드시 Vector DB 내에서만 직접적으로 인용, 숫자는 절대로 자의적으로 반올림/올림/버림 하지 말고 그대로 표시할 것
12. 출처표시 : 결과물의 마지막 부분에만 표시
13. 현재날짜 : 2024년 7월 14일""", language="plaintext")

    with st.expander("4. VIS 보고서 내용 요약(Bullet Point)"):
        st.code("""1. 최종목표 : 가장 최근 '종목명' 보고서 내용 요약 및 정리
2. 추가 데이터 제공 여부 : RAG 목적의 OpenAI Assistant API Vector DB
3. 참고할 데이터 범위 : 먼저 최종목표에 부합하는 데이터를 Vector DB에서 찾고, 특정 보고서를 지정하였다면 해당 보고서의 Chunk 내용만을 참고하고 나머지 Vector DB 및 사전 학습된 내용은 참고 범위에서 배제
4. 역할부여 : DB를 전체적으로 빠짐없이 뒤져서 요청한 정보를 자연어 유사어와 전문용어까지 고려하여 찾아올 수 있는 검색엔진이자, 체계적이고 깔끔하게 정리를 잘 해내는 애널리스트
5. 글의 종류 : 코멘트
6. 결과물의 형식 : 가장 최근에 작성된 보고서의 내용을 Bullet Point 방식으로 요약정리. 수치적인 내용 보다는, 핵심 개념과 논리 위주로 작성. 내용이 복잡하고 길 경우에는 Sub-topic별로 구분 (Sub-topic을 구분할 경우에는 그 직전에 줄바꿈 하여 가독성을 높일 것)
7. 결과물의 분량 : 900~1500 글자 범위 내
8. 필수 포함 내용 : 종목명, 작성자, 작성일, 목표가, 기대수익률, 투자의견 / 필수 포함 내용은 결과물의 가장 처음에 표시
9. 문체 : 개조식, 명사형종결어미
10. 작성언어 : 한국어
11. 제한사항 : 가급적 수치는 내용에 포함하지 않도록 하고, 꼭 필요한 수치는 반드시 Vector DB 내에서만 직접적으로 인용, 숫자는 절대로 자의적으로 반올림/올림/버림 하지 말고 그대로 표시할 것
12. 출처표시 : 결과물의 마지막 부분에만 표시
13. 현재날짜 : 2024년 7월 14일""", language="plaintext")

    with st.expander("5. 시황/전망 코멘트 작성"):
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
13. 현재 날짜 및 시간 : 2024년 7월 15일
14. 출처표시 : 하지 말 것""", language="plaintext")

st.title("💬 AI for VIP Information System")
initial_message = (
    "저는 VIP AI 입니다. VIS DB의 내용을 구석구석 뒤져서 최선을 다해 답변드리겠습니다. "
    "VIS DB에 관련된 내용만 질문해주세요.\n"
    "\n<VIP AI 사용법>\n"
    " 1. 전달 받은 OpenAI API Key를 복사 & 붙여넣기 하여 입력합니다.\n"
    " 2. 'Create a new thread' 버튼을 누르고, 아래에 생선된 thread ID (thread_XXXXXXXXXXXXXXXXXXX 형식)를 복사한 후 Thread ID 란에 붙여넣습니다.\n"
    " 3. 궁금한 사항(Prompt)을 Prompt창에 입력합니다.\n"
    " 4. VIP AI와 나누는 대화의 주제가 바뀌거나(이전의 내용과 연속성이 없는 경우), 대답을 제대로 하지 못할 때에는 새로운 Thread를 생성하여 적용하는 것이 좋습니다. 새로운 Thread로도 문제가 해결되지 않을 경우에는, 웹페이지 새로고침을 통해 완전히 Reset 하고 다시 시작하는 것이 필요합니다.\n"	
    "\n※ 더 나은 결과물을 얻고 싶거나, Prompt를 직접 작성하기 어렵다면, 화면 좌측에 위치한 'Pre-written Prompt Templates'의 Drop-down을 열고 해당 내용을 Prompt 창에 복사&붙여넣기 한 후에 필요한 내용만 수정한 후에 Enter를 입력합니다."
)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": initial_message}]

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
