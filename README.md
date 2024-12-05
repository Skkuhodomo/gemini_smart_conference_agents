아래는 프로젝트를 설명하는 **README.md** 파일의 영어 버전입니다. 이 파일은 프로젝트 구조와 실행 방법을 간결하게 설명하며, 깃허브에 올릴 때 유용합니다.

---

### **`README.md`**

```markdown
# Smart Meeting Room System

## Overview
The Smart Meeting Room System integrates multiple IoT devices and APIs to create an intelligent and automated environment for meetings. It includes features such as attendee tracking, real-time environmental monitoring, and speech-to-text summarization.

## Features
1. **Attendee Tracking**:
   - Uses RFID to track attendees and log their information to Firebase.
2. **Speech-to-Text and Summarization**:
   - Converts spoken words into text and generates summaries using Google Gemini API.
3. **Environmental Monitoring**:
   - Monitors temperature, humidity, and sound levels in real time.
4. **Difficulty Level Analysis**:
   - Calculates presentation difficulty based on attendee roles and interests.

## Project Structure
- **Board 1 (ESP32)**: Tracks attendees using RFID and logs data to Firebase.
- **Board 2 (Raspberry Pi 4)**: 
  - Processes audio input, converts speech to text, and generates summaries using Google Gemini API.
  - Analyzes attendee data to calculate presentation difficulty.
- **Board 3 (ESP32)**: Monitors environmental conditions (temperature, humidity, sound levels) and logs them to Firebase.
- **Streamlit Dashboard**: Visualizes real-time data including attendees, environmental conditions, and summaries.

## Requirements
### Hardware
- ESP32 (x2)
- RFID Reader (RC522)
- Raspberry Pi 4
- DHT22 Temperature and Humidity Sensor
- LM393 Sound Sensor
- Microphone

### Software
- Python 3.8+
- Firebase Realtime Database
- Google Gemini API

### Python Dependencies
Install the required Python packages using:
```bash
pip install -r requirements.txt
```

## How to Run
### ESP32 Boards
1. Flash the provided ESP32 code (`Board1`, `Board3`) using the Arduino IDE.
2. Configure Wi-Fi credentials and Firebase settings in the code.

### Raspberry Pi
1. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the Python script for Raspberry Pi:
   ```bash
   python raspberry_pi_main.py
   ```

### Streamlit Dashboard
1. Navigate to the Streamlit dashboard directory.
2. Run the Streamlit app:
   ```bash
   streamlit run dashboard.py
   ```

## Firebase Configuration
1. Set up a Firebase project and enable Realtime Database.
2. Download the service account key file and place it in the project directory.
3. Update the Firebase credentials in the Python and ESP32 scripts.

## Environment Variables
Set up the following environment variables for secure API integration:
- `GOOGLE_GEMINI_API_KEY`: Your Google Gemini API key.

## Example Data Flow
1. **Attendee Tracking**:
   - RFID data is logged to `/attendees`.
2. **Environmental Monitoring**:
   - Temperature, humidity, and sound levels are logged to `/environment`.
3. **Speech-to-Text and Summarization**:
   - Speech text and summaries are logged to `/meeting`.
4. **Presentation Difficulty**:
   - Difficulty scores are logged to `/presentation`.

## Sample Firebase Data Structure
```json
{
  "attendees": {
    "1": "Manager",
    "2": "Beginner",
    "3": "Specialist"
  },
  "environment": {
    "temperature": 24.5,
    "humidity": 45,
    "sound_level": 300
  },
  "meeting": {
    "speech_text": "The presenter discussed AI applications.",
    "summary": "AI applications discussion.",
    "timestamp": "2024-12-05 14:05:00"
  },
  "presentation": {
    "difficulty": 7,
    "timestamp": "2024-12-05 14:00:00"
  }
}
```

