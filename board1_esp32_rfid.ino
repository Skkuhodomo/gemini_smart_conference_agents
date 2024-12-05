#include <WiFi.h>
#include <FirebaseESP32.h>
#include <MFRC522.h>

// Wi-Fi 설정
#define WIFI_SSID "Your_SSID"
#define WIFI_PASSWORD "Your_PASSWORD"

// Firebase 설정
#define FIREBASE_HOST "your-firebase-database.firebaseio.com"
#define FIREBASE_AUTH "your-firebase-auth-key"

// RFID 핀 설정
#define RST_PIN 4
#define SS_PIN 5

MFRC522 rfid(SS_PIN, RST_PIN); // RFID 객체 생성
FirebaseData firebaseData;

void setup() {
  Serial.begin(115200);

  // Wi-Fi 연결
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("\nWi-Fi connected");

  // Firebase 초기화
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
  Firebase.reconnectWiFi(true);

  // RFID 초기화
  SPI.begin();
  rfid.PCD_Init();
  Serial.println("Place your RFID card near the reader...");
}

void loop() {
  if (!rfid.PICC_IsNewCardPresent() || !rfid.PICC_ReadCardSerial()) {
    delay(50);
    return;
  }

  // UID 읽기
  String uid = "";
  for (byte i = 0; i < rfid.uid.size; i++) {
    uid += String(rfid.uid.uidByte[i], HEX);
  }
  uid.toUpperCase();
  Serial.println("UID: " + uid);

  // Firebase로 데이터 전송
  if (Firebase.pushString(firebaseData, "/attendees", uid)) {
    Serial.println("Data sent to Firebase: " + uid);
  } else {
    Serial.println("Firebase push failed: " + firebaseData.errorReason());
  }

  // 카드 제거 대기
  delay(1000);
  rfid.PICC_HaltA();
}
