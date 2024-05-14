void setup() {
  Serial.begin(115200);  //開始輸出訊息到監控視窗
}

void loop() {
  int sensorValue = analogRead(25);  //讀取A0的值
  int sensorValue = analogRead(26);  //讀取A0的值

  if(sensorValue>300){
  Serial.println(sensorValue);
  }       //在監控視窗顯示讀取的值
  delay(10);
}