import streamlit as st
from google import genai

# 페이지 설정
st.set_page_config(
    page_title="연애상담 챗봇",
    page_icon="💖"
)

st.title("💖 연애상담 챗봇")
st.caption("Gemini 2.5 Flash Lite 기반")

# API 키 확인
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("GEMINI_API_KEY가 Secrets에 설정되지 않았습니다.")
    st.stop()

# Gemini 클라이언트 생성
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"Gemini 초기화 오류: {e}")
    st.stop()

# 채팅 기록 저장
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "안녕하세요! 연애 고민을 편하게 이야기해 주세요 😊"
        }
    ]

# 이전 대화 출력
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 사용자 입력
prompt = st.chat_input("메시지를 입력하세요")

if prompt:
    # 사용자 메시지 저장
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Gemini용 대화 변환
        history_text = ""

        for msg in st.session_state.messages:
            role = "사용자" if msg["role"] == "user" else "상담사"
            history_text += f"{role}: {msg['content']}\n"

        full_prompt = f"""
당신은 공감 능력이 뛰어난 연애상담 전문가입니다.

규칙:
- 따뜻하고 친절하게 답변한다.
- 사용자를 비난하지 않는다.
- 현실적인 조언을 제공한다.
- 너무 길지 않게 답변한다.

대화 내용:
{history_text}

상담사:
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=full_prompt
        )

        answer = response.text

    except Exception as e:
        answer = f"⚠️ 오류가 발생했습니다.\n\n{str(e)}"

    # 응답 출력
    with st.chat_message("assistant"):
        st.markdown(answer)

    # 기록 저장
    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

# 사이드바
with st.sidebar:
    st.header("설정")

    if st.button("대화 초기화"):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "안녕하세요! 연애 고민을 편하게 이야기해 주세요 😊"
            }
        ]
        st.rerun()
