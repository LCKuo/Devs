#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

const char* ssid = "SndaKaohsiung";
const char* password = "0929633965";

void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();

  while (!Serial);

  // Wait for WiFi connection
  WiFi.begin(ssid, password);
  Serial.print("Connecting to ");
  Serial.println(ssid);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }

  Serial.println("Connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  Serial.print("Ask your Question : ");

  while (!Serial.available()) {
    delay(100); // Wait for input
  }

  String Question = Serial.readStringUntil('\n'); // Read the input from Serial monitor
  Question.trim(); // Remove any leading/trailing white spaces

  Serial.println("Question: " + Question);

  HTTPClient https;

  if (https.begin("http://192.168.68.69:1234/v1/chat/completions")) {  // Use HTTP
    https.addHeader("Content-Type", "application/json");

    String payload = String("{ \"model\": \"microsoft/Phi-3-mini-4k-instruct-gguf\", \"messages\": [ { \"role\": \"system\", \"content\": \"Always answer in Chinese.\" }, { \"role\": \"user\", \"content\": \"") + Question + "\" } ], \"temperature\": 0.7, \"max_tokens\": -1, \"stream\": false }";

    int httpCode = https.POST(payload);

    if (httpCode == HTTP_CODE_OK || httpCode == HTTP_CODE_MOVED_PERMANENTLY) {
      String payload = https.getString();
      Serial.println("Response: " + payload);

      // 解析 JSON
      DynamicJsonDocument doc(1024);
      deserializeJson(doc, payload);

      // 從 JSON 中提取 content 部分
      String content = doc["choices"][0]["message"]["content"].as<String>();
      Serial.println("Content: " + content);
    } else {
      Serial.printf("[HTTP] POST... failed, error: %s\n", https.errorToString(httpCode).c_str());
    }

    https.end();
  } else {
    Serial.printf("[HTTP] Unable to connect\n");
  }
}
