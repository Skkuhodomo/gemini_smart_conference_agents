import os
import time
import subprocess
import firebase_admin
from firebase_admin import credentials, db
import google.generativeai as genai
import speech_recognition as sr

# Google Gemini API 및 Firebase 초기화
GOOGLE_GEMINI_API_KEY = os.environ['GOOGLE_GEMINI_API_KEY']
genai.configure(api_key=GOOGLE_GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

cred = credentials.Certificate("path/to/firebase-key.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://<your-firebase-project>.firebaseio.com/'
})

# 참석자 정보 기반 난이도 계산
def calculate_difficulty(attendees):
    """참석자 정보를 기반으로 발표 난이도를 계산"""
    difficulty = 0
    for key, value in attendees.items():
        if "매니저" in value:  # 매니저 이상일 경우 난이도 증가
            difficulty += 2
        if "전문가" in value:  # 전문가가 많을 경우 난이도 증가
            difficulty += 1
        if "초보자" in value:  # 초보자가 많을 경우 난이도 감소
            difficulty -= 1
    return max(1, min(10, difficulty))  # 난이도는 1~10 사이로 제한

def get_attendees():
    """Firebase에서 참석자 정보 가져오기"""
    attendees_ref = db.reference('/attendees')
    return attendees_ref.get() or {}

def save_difficulty_to_firebase(difficulty):
    """Firebase에 발표 난이도 저장"""
    ref = db.reference('/presentation')
    ref.set({
        "difficulty": difficulty,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    })

def summarize_text_with_gemini(text):
    """Google Gemini API를 사용해 텍스트 요약"""
    response = model.generate_content(text)
    return response.text

def process_audio_and_summarize():
    """마이크로 음성 입력 받아 텍스트 변환 후 요약"""
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        print("Speak now...")
        audio = recognizer.listen(source)
    try:
        # 음성을 텍스트로 변환 (한국어 지원)
        text = recognizer.recognize_google(audio, language="ko-KR")
        print(f"Recognized Text: {text}")

        # Google Gemini로 요약 생성
        summary = summarize_text_with_gemini(text)
        print(f"Generated Summary: {summary}")

        return text, summary
    except sr.UnknownValueError:
        print("음성을 인식할 수 없습니다.")
        return None, None
    except sr.RequestError as e:
        print(f"STT 서비스 오류: {e}")
        return None, None

def save_to_firebase(text, summary):
    """Firebase에 텍스트 및 요약 저장"""
    ref = db.reference('/meeting')
    ref.set({
        "speech_text": text,
        "summary": summary,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    })

if __name__ == "__main__":
    try:
        # 참석자 데이터 가져오기
        attendees = get_attendees()
        if not attendees:
            print("참석자 데이터가 없습니다.")
            exit()

        # 난이도 계산
        difficulty = calculate_difficulty(attendees)
        print(f"발표 난이도: {difficulty}")

        # Firebase에 난이도 저장
        save_difficulty_to_firebase(difficulty)

        # 음성 입력 처리 및 요약 생성
        while True:
            text, summary = process_audio_and_summarize()
            if text and summary:
                # Firebase에 저장
                save_to_firebase(text, summary)
                print("데이터가 Firebase에 저장되었습니다.")
            time.sleep(5)

    except Exception as e:
        print(f"오류 발생: {e}")
