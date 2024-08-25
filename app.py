import streamlit as st
from openai import OpenAI
import time

MODEL_LIST = ["gpt-4o-2024-08-06", "gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo", "gpt-4-turbo"]
assistant_id = "asst_9J6Vvl01IO9bL8J8FI6twfh2"

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
        st.code("""1. 최종목표: '종목명' 투자 아이디어 요약
2. 추가 데이터 제공 여부 : RAG 목적의 OpenAI Assistant API Vector DB
3. 참고할 데이터 범위 : 먼저 최종목표와 가장 연관도가 높은 데이터를 Vector DB에서 찾고, 현재 날짜로부터 가장 가까운 작성일자를 가진 내용에 더욱 가중치를 두어 참조. 특정 게시물 또는 게시물을 지정하였다면 해당 게시물의 Chunk 내용만을 참고하고, 나머지는 사전 학습된 내용을 참고
4. 역할부여 : 매우 똑똑하고 전문적인 금융 전문가 애널리스트
5. 배경정보 : 배경지식이 없는 신규 고객에게 포트폴리오 내 주요 종목을 쉽게 설명하고 이해시키기 위함
6. 글의 종류 : 메모
7. 결과물의 형식 : Bullet Point From 4 Upto 7개, Sub-topic은 표시하지 말 것. 각 Bullet Point별 문장의 길이는 From 35 Upto 100글자 범위
8. 선호하는 결과물의 내용 구성 (해당 종목이 포함된 산업의 구조적 변화 및 방향성, 해당 종목의 개별적인 투자 아이디어, 중장기 전망)
9. 작성언어 : 한국어
10. 문체 : 개조식, 명사형종결어미
11. 제한사항 : 구체적인 수치는 가급적 제외할 것, 꼭 필요한 수치는 반드시 Vector DB 내에서만 직접적으로 인용, 숫자는 절대로 자의적으로 반올림/올림/버림 하지 말고 출처 내용에서 그대로 표시할 것, 목표주가 및 기대수익률에 대한 내용은 반드시 제외
12. 답변에 대한 해설 : 불필요
13. 출처표시 : 참고한 출처들은 결과물의 마지막 부분에 표시하고, '제목, 작성자, 작성일자'의 형태로 출력할 것
14. 결과물 : 총 2개의 결과물을 Version별로 제시해줘. 각 Version은 내용별 중요도의 가중치 변화, 구체적인 수치 유무의 차이, 결론 및 미래전망 포함 유무의 차이 등으로 차별화를 크게 하여 서로 겹치는 비율이 30% 미만이 되도록 해줘""", language="plaintext")

    with st.expander("2. 종목별 최근 주가 변동 원인 설명"):
        st.code("""1. 최종목표: '효성중공업'의 최근 주가 변동 이유 및 향후 전망에 대한 코멘트 작성
2. 추가 데이터 제공 여부 : RAG 목적의 OpenAI Assistant API Vector DB
3. 참고할 데이터 범위 : 먼저 최종목표와 가장 연관도가 높은 데이터를 Vector DB에서 찾고, 현재 날짜로부터 가장 가까운 작성일자를 가진 내용에 더욱 가중치를 두어 참조. 특정 보고서 또는 게시물을 지정하였다면 해당 게시물의 Chunk 내용만을 참고하고 나머지 Vector DB 및 사전 학습된 내용은 참고 범위에서 배제
4. 역할부여 : DB를 전체적으로 빠짐없이 뒤져서 요청한 정보를 자연어 유사어와 전문용어까지 고려하여 찾아올 수 있는 검색엔진이자, 체계적이고 깔끔하게 정리를 잘 해내는 애널리스트
5. 배경정보 : 주가 변동성 확대에 따라 펀드 판매 담당자 및 고객들의 우려 증가
6. 글의 종류 : 메모
7. 결과물의 형식 : Bullet Point From 3 Upto 6개, 각 Bullet Point별 문장의 길이는 From 35 Upto 120글자 범위, Sub-topic은 표시하지 말 것. 
8. 선호하는 결과물의 내용 구성 (해당 종목이 포함된 산업의 구조적 변화 및 방향성, 해당 종목의 개별적이고 구체적인 핵심 이슈, 중장기 전망)
9. 작성언어 : 한국어
10. 문체 : 개조식, 명사형종결어미
11. 제한사항 : 꼭 필요한 수치는 반드시 Vector DB 내에서만 직접적으로 인용, 숫자는 절대로 자의적으로 반올림/올림/버림 하지 말고 출처 내용에서 그대로 표시할 것
12. 답변에 대한 해설 : 불필요
13. 현재 날짜 및 시간 : [2024년 월 일]
14. 출처표시 : No In-context source, 결과물의 마지막 부분에만 표시하고, '제목, 작성자, 작성일자'의 형태로 출력할 것
15. 결과물 : 총 2개의 결과물을 Version별로 제시해줘. 각 Version은 내용별 중요도의 가중치 변화, 구체적인 수치 유무의 차이, 결론 및 미래전망 포함 유무의 차이 등으로 차별화를 크게 하여 서로 겹치는 비율이 30% 미만이 되도록 해줘""", language="plaintext")

    with st.expander("3. VIS 보고서 내용 요약(개조식)"):
        st.code("""0. 사전질문 : 가장 최근에 작성된 '한양이엔지' 관련 게시물는 뭐지? (현재 날짜는 2024년 8월 25일) 

1. 최종목표 : 2024년 6월 20일자 '한양이엔지' 관련 게시물 내용 요약 및 정리
2. 추가 데이터 제공 여부 : RAG 목적의 OpenAI Assistant API Vector DB
3. 참고할 데이터 범위 : 먼저 최종목표와 가장 연관도가 높은 데이터를 Vector DB에서 찾고, 현재 날짜로부터 가장 가까운 작성일자를 가진 내용에 더욱 가중치를 두어 참조. 특정 보고서 또는 게시물을 지정하였다면 해당 보고서의 Chunk 내용만을 참고하고 나머지 Vector DB 및 사전 학습된 내용은 참고 범위에서 배제
4. 역할부여 : DB를 전체적으로 빠짐없이 뒤져서 요청한 정보를 자연어 유사어와 전문용어까지 고려하여 찾아올 수 있는 검색엔진이자, 체계적이고 깔끔하게 정리를 잘 해내는 애널리스트
5. 글의 종류 : 메모
6. 결과물의 형식 : 최종목표에서 지정된 게시물의 내용을 서술식으로 요약정리. 수치적인 내용 보다는, 핵심 개념과 논리 위주로 작성. 내용이 복잡하고 길 경우에는 Sub-topic별로 구분.
7. 결과물의 분량 : From 900 Upto 1500 글자 범위 내
8. 필수 포함 내용 : 종목명, 작성자, 작성일, 목표주가, 투자의견 / 필수 포함 내용은 결과물의 가장 처음에 표시
9. 결과물의 구성 : 주요 수치가 포함된 내용은 전체 내용의 30% 이내로 제한하고, 나머지 Bullet Point는 수치를 제외한 주요 내용 중 중요한 내용 위주로 요약 정리할 것. 또한, 긍정적(기회)인 부분과 부정적(리스크)인 부분의 분량을 균형있게 다룰 것. "결론, 의견, 추천, 판단, 계획" 등 결론과 행동을 촉구하는 내용은 가급적 마지막 Bullet Point에 포함할 것
9. 문체 : 개조식, 명사형종결어미
10. 작성언어 : 한국어
11. 제한사항 : 꼭 필요한 수치는 반드시 Vector DB 내에서만 직접적으로 인용, 숫자는 절대로 자의적으로 반올림/올림/버림 하지 말고 출처 내용에서 그대로 표시할 것
12. 출처표시 : No In-context source, 결과물의 마지막 부분에만 표시하고, '제목, 작성자, 작성일자'의 형태로 출력할 것
13. 결과물 : 총 2개의 결과물을 Version별로 제시해줘. 각 Version은 내용별 중요도의 가중치 변화, 구체적인 수치 유무의 차이, 결론 및 미래전망 포함 유무의 차이 등으로 차별화를 크게 하여 서로 겹치는 비율이 30% 미만이 되도록 해줘""", language="plaintext")

    with st.expander("4. 분기 실적 요약(서술식)"):
        st.code("""1. 최종목표 : '1Q24' '종목명' 실적 요약 및 정리
2. 추가 데이터 제공 여부 : RAG 목적의 OpenAI Assistant API Vector DB
3. 참고할 데이터 범위 : 먼저 최종목표와 가장 연관도가 높은 데이터를 Vector DB에서 찾고, 특정 보고서 또는 게시물을 지정하였다면 해당 보고서의 Chunk 내용만을 참고하고 나머지 Vector DB 및 사전 학습된 내용은 참고 범위에서 배제
4. 역할부여 : DB를 전체적으로 빠짐없이 뒤져서 요청한 정보를 자연어 유사어와 전문용어까지 고려하여 찾아올 수 있는 검색엔진이자, 체계적이고 깔끔하게 정리를 잘 해내는 애널리스트
5. 글의 종류 : 메모
6. 결과물의 형식 : 최종목표에 부합하는 내용을 서술형 방식으로 From 3 Upto 5개 문단으로 요약정리. 전체 결과물의 분량이 1500글자 이내라면, Sub-topic으로 내용을 분류하지 말 것.
7. 결과물의 분량 : From 500 Upto 1000 글자 범위 내
8. 결과물의 구성 : 주요 수치가 포함된 내용은 전체 내용의 30% 이내로 제한하고, 나머지 Bullet Point는 수치를 제외한 주요 내용 중 중요한 내용 위주로 요약 정리할 것. 또한, 긍정적(기회)인 부분과 부정적(리스크)인 부분의 분량을 균형있게 다룰 것. "결론, 의견, 추천, 판단, 계획" 등 결론과 행동을 촉구하는 내용은 가급적 마지막 Bullet Point에 포함할 것
9. 문체 : 서술식, 명사형종결어미
10. 작성언어 : 한국어
11. 제한사항 : 꼭 필요한 수치는 반드시 Vector DB 내에서만 직접적으로 인용, 숫자는 절대로 자의적으로 반올림/올림/버림 하지 말고 출처 내용에서 그대로 표시할 것
12. 출처표시 : 결과물의 마지막 부분에 표시하고, '제목, 작성자, 작성일자'의 형태로 출력할 것
13. 결과물 : 총 2개의 결과물을 Version별로 제시해줘. 각 Version은 내용별 중요도의 가중치 변화, 구체적인 수치 유무의 차이, 결론 및 미래전망 포함 유무의 차이 등으로 차별화를 크게 하여 서로 겹치는 비율이 30% 미만이 되도록 해줘""", language="plaintext")

    with st.expander("5. 분기 실적 요약(개조식)"):
        st.code("""1. 최종목표 : '1Q24' '동원F&B' 실적 요약 및 정리
2. 추가 데이터 제공 여부 : RAG 목적의 OpenAI Assistant API Vector DB
3. 참고할 데이터 범위 : 먼저 최종목표와 가장 연관도가 높은 데이터를 Vector DB에서 찾고, 특정 보고서 또는 게시물을 지정하였다면 해당 보고서의 Chunk 내용만을 참고하고 나머지 Vector DB 및 사전 학습된 내용은 참고 범위에서 배제
4. 역할부여 : DB를 전체적으로 빠짐없이 뒤져서 요청한 정보를 자연어 유사어와 전문용어까지 고려하여 찾아올 수 있는 검색엔진이자, 체계적이고 깔끔하게 정리를 잘 해내는 애널리스트
5. 글의 종류 : 메모
6. 결과물의 형식 : 최종목표에 부합하는 내용을 Bullet Point방식으로 요약정리. 
7. 결과물의 분량 : Bullet Point From 5 upto 10개 범위 내, 각 Bullet Point별 문장의 길이는 30~120글자 범위
8. 결과물의 구성 : 주요 수치가 포함된 내용은 전체 Bullet Point의 50% 이내로 제한하고, 나머지 Bullet Point는 수치를 제외한 주요 내용 중 중요한 내용 위주로 요약 정리할 것. 또한, 긍정적(기회)인 부분과 부정적(리스크)인 부분의 분량을 균형있게 다룰 것. "결론, 의견, 추천, 판단, 계획" 등 결론과 행동을 촉구하는 내용은 가급적 마지막 Bullet Point에 포함할 것
9. 문체 : 개조식, 명사형종결어미
10. 작성언어 : 한국어
11. 제한사항 : 꼭 필요한 수치는 반드시 Vector DB 내에서만 직접적으로 인용, 숫자는 절대로 자의적으로 반올림/올림/버림 하지 말고 출처 내용에서 그대로 표시할 것
12. 출처표시 : 결과물의 마지막 부분에 표시하고, '제목, 작성자, 작성일자'의 형태로 출력할 것
13. 결과물 : 총 2개의 결과물을 Version별로 제시해줘. 각 Version은 내용별 중요도의 가중치 변화, 구체적인 수치 유무의 차이, 결론 및 미래전망 포함 유무의 차이 등으로 차별화를 크게 하여 서로 겹치는 비율이 30% 미만이 되도록 해줘""", language="plaintext")

    with st.expander("Feedback Prompt Templates"):
        st.code("""- 각 문장별 길이가 너무 짧으니, 직전 결과물 대비 2배의 분량으로 늘려서 다시 작성해주세요.
- 각 Bullet Point의 출처는 제거하고, 출처는 결과물의 가장 마지막에만 한번에 표시해주세요.
- 수치를 포함한 내용은 제거하고, 내용의 배경과 설명을 보충해서 다시 작성해주세요.
- 투자의견, 핵심논리, 목표주가, 밸류에이션, 기대수익률, 결론 등을 한 문장으로 요약해주세요.""", language="plaintext")
	    
st.title("💬 AI for VIP Information System")
initial_message = (
    "저는 VIP AI(Latest Update 2024/08/25) 입니다. VIS DB의 내용을 구석구석 뒤져서 최선을 다해 답변드리겠습니다. "
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
