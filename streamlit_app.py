'''import streamlit as st
from openai import OpenAI

# ──────────────────────────────────────────────────────────────
# 📚 BookSoul – Your Bookmate, Your Soulmate
# ──────────────────────────────────────────────────────────────
st.title("📚 BookSoul – Your Bookmate, Your Soulmate 💛")
st.write(
    "혼자 있는 마음에 따뜻한 한 권을 건네줄게요.\n"
    "당신의 감정, 상황, 고민을 들려주면 딱 맞는 책을 추천해줄게요.\n\n"
    "예: *'지치고 무기력할 때 읽을 책 추천해줘'*, *'창의력이 샘솟는 책 있을까?'*"
)

# 🔐 OpenAI API Key 입력
openai_api_key = st.text_input("🔑 OpenAI API Key를 입력하세요:", type="password")
if not openai_api_key:
    st.info("API 키를 입력하면 챗봇이 작동합니다.", icon="💡")
    st.stop()

# OpenAI 클라이언트 생성
client = OpenAI(api_key=openai_api_key)

# 세션 상태에 메시지 저장
if "messages" not in st.session_state:
    st.session_state.messages = []

# 이전 대화 메시지 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 받기
if prompt := st.chat_input("당신의 감정이나 상황을 들려주세요. 예: ‘위로가 되는 책’"):
    # ① 사용자 메시지 저장 및 화면에 표시
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # ② OpenAI API 호출 (gpt-4o‑mini)
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            # 시스템 프롬프트: 책 추천 전문 큐레이터 역할
            {
                "role": "system",
                "content": (
                    "당신은 감정과 상황에 맞는 책을 큐레이션해주는 따뜻한 도서 추천 전문가입니다. "
                    "추천 시 책 제목(한글+원제), 저자, 간단한 줄거리, 추천 이유를 2~3문장으로 정리해 주세요. "
                    "가능하면 비슷한 느낌의 추가 도서 1권도 ‘함께 읽으면 좋아요’ 형식으로 제안하세요."
                ),
            },
            # 대화 히스토리
            *[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
        ],
        stream=True,
        temperature=1.1,  # 감성+창의성
    )

    # ③ 챗봇 응답 스트리밍 출력
    with st.chat_message("assistant"):
        response = st.write_stream(stream)

    # ④ 응답 저장
    st.session_state.messages.append({"role": "assistant", "content": response})'''

import streamlit as st
from openai import OpenAI

# ──────────────────────────────────────────────
# 🤖 T-BOT for Advice, F-BOT for Warmth
# ──────────────────────────────────────────────
st.title("🤖 T-BOT for Advice, F-BOT for Warmth")
st.write(
    "고민이 있으신가요?\n\n"
    "**T-BOT**은 명확한 조언을,\n"
    "**F-BOT**은 따뜻한 위로를 건네줄 거예요.\n\n"
    "아래에서 어떤 도움이 필요한지 선택해 주세요."
)

# 🔐 OpenAI API 키 입력
openai_api_key = st.text_input("🔑 OpenAI API Key를 입력하세요:", type="password")
if not openai_api_key:
    st.info("API 키를 입력하면 챗봇이 작동합니다.", icon="💡")
    st.stop()

# 🤖 T-BOT or F-BOT 선택
bot_type = st.radio(
    "누구에게 말 걸고 싶으신가요?",
    ["🧠 T-BOT (조언이 필요해요)", "💖 F-BOT (위로가 필요해요)"],
    index=0,
)

# 시스템 역할 정의
if "T-BOT" in bot_type:
    system_prompt = (
        "당신은 이성적이고 논리적인 조언을 제공하는 T-BOT입니다. "
        "사용자의 문제를 분석하고, 실용적이며 구체적인 조언을 2~3문장으로 제공하세요."
    )
else:
    system_prompt = (
        "당신은 공감과 위로를 건네는 감성적인 F-BOT입니다. "
        "사용자의 감정을 이해하고, 따뜻한 말과 위로의 메시지를 2~3문장으로 전달하세요."
    )

# OpenAI 클라이언트 생성
client = OpenAI(api_key=openai_api_key)

# 세션 상태에 메시지 저장
if "messages" not in st.session_state:
    st.session_state.messages = []

# 이전 대화 메시지 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 받기
if prompt := st.chat_input("지금 어떤 이야기를 나누고 싶으신가요?"):
    # 사용자 메시지 저장
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # OpenAI API 호출
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            *[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
        ],
        stream=True,
        temperature=1.1,
    )

    # 응답 출력 및 저장
    with st.chat_message("assistant"):
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})

