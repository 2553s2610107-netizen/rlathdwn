# app.py

import streamlit as st
import random

st.set_page_config(
    page_title="수행평가 1인1역 뽑기",
    page_icon="🎲",
    layout="centered"
)

st.title("🎲 수행평가 1인1역 뽑기 앱")

st.write("학생 이름과 역할을 입력한 뒤 자동으로 랜덤 배정하세요.")

# 학생 입력
students_input = st.text_area(
    "학생 이름 입력 (한 줄에 한 명)",
    height=200,
    placeholder="김민수\n이서연\n박준호"
)

# 역할 입력
roles_input = st.text_area(
    "역할 입력 (한 줄에 하나)",
    height=200,
    placeholder="발표자\n자료조사\nPPT 제작"
)

# 버튼
if st.button("🎯 역할 뽑기"):

    students = [
        s.strip()
        for s in students_input.split("\n")
        if s.strip()
    ]

    roles = [
        r.strip()
        for r in roles_input.split("\n")
        if r.strip()
    ]

    # 예외 처리
    if len(students) == 0:
        st.error("학생 이름을 입력하세요.")
    elif len(roles) == 0:
        st.error("역할을 입력하세요.")
    elif len(students) != len(roles):
        st.error("학생 수와 역할 수를 같게 맞춰주세요.")
    else:
        random.shuffle(roles)

        st.success("배정 완료!")

        st.subheader("📋 역할 배정 결과")

        for student, role in zip(students, roles):
            st.write(f"✅ {student} → {role}")
