void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  delay(1000);
}

void loop() {
  // put your main code here, to run repeatedly:
  float y = random(-80, -20);
  Serial.print(y);
  Serial.print(",");
  delay(10);
}
