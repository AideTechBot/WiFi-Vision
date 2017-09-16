void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  delay(1000);
}

void loop() {
  // put your main code here, to run repeatedly:
  float y = random(1, 101) / 100.0;
  Serial.print(y);
  Serial.print(",");
  delay(10);
}
