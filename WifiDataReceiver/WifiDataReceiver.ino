void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  delay(1000);
}

void loop() {
  // put your main code here, to run repeatedly:
  float y = random(-80, -20);
  Serial.print("0:");
  Serial.print(y);
  Serial.print(",");
  delay(10);
  y = random(-80, -20);
  Serial.print("1:");
  Serial.print(y);
  Serial.print(",");
  delay(10);
  y = random(-80, -20);
  Serial.print("2:");
  Serial.print(y);
  Serial.print(",");
  delay(10);
  y = random(-80, -20);
  Serial.print("3:");
  Serial.print(y);
  Serial.print(",");
  delay(10);
}
