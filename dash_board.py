import streamlit as st
import pandas as pd
import time
from firebase_admin import credentials, initialize_app, db
import firebase_admin

# Firebase 초기화
cred = credentials.Certificate("path/to/firebase-key.json")
if not firebase_admin._apps:
    initialize_app(cred, {
        'databaseURL': 'https://<your-firebase-project>.firebaseio.com/'
    })

# Firebase 데이터 가져오기
def get_environment_data():
    environment_ref = db.reference('/environment')
    environment = environment_ref.get() or {}
    return {
        "temperature": environment.get("temperature", None),
        "humidity": environment.get("humidity", None)
    }

def get_attendees():
    attendees_ref = db.reference('/attendees')
    return attendees_ref.get() or {}

def get_summary():
    summary_ref = db.reference('/meeting')
    return summary_ref.get() or {}

# Streamlit 대시보드
def main():
    st.title("스마트 회의실 대시보드")

    # 참석자 목록
    st.subheader("참석자 목록")
    attendees = get_attendees()
    if attendees:
        for key, value in attendees.items():
            st.write(f"- UID: {value}")
    else:
        st.write("참석자가 없습니다.")

    # 실시간 온습도 그래프
    st.subheader("실시간 온습도 그래프")
    df = pd.DataFrame(columns=["Time", "Temperature", "Humidity"])
    graph_placeholder = st.empty()

    while True:
        environment = get_environment_data()
        current_time = time.strftime("%H:%M:%S")
        new_data = {"Time": current_time, "Temperature": environment["temperature"], "Humidity": environment["humidity"]}
        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
        graph_placeholder.line_chart(df.set_index("Time"))
        time.sleep(5)

if __name__ == "__main__":
    main()
