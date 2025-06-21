import streamlit as st
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
    st.session_state.messages.append({"role": "assistant", "content": response})
    
