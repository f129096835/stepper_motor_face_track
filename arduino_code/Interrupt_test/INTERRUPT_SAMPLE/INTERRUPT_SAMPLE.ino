#define LED_OUTPUT 4

void setup()
{
  pinMode(LED_OUTPUT, OUTPUT);
  digitalWrite(LED_OUTPUT, LOW);
}

void loop() {
  digitalWrite(LED_OUTPUT, HIGH);
  delay(500);
  digitalWrite(LED_OUTPUT, LOW);
  delay(500);
}
