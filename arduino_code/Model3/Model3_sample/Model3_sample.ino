#define LED_OUTPUT 4
#define DELAY_TIME 500
unsigned long time_now = 0; 
int period = DELAY_TIME;//計時的時間
bool state = LOW;

void setup() {
    time_now = millis();
    pinMode(LED_OUTPUT, OUTPUT);
    digitalWrite(LED_OUTPUT, state);  
}
 
void loop() {
    if(millis() - time_now >= DELAY_TIME){
        state = !state;
        digitalWrite(LED_OUTPUT, state);
        time_now = millis();
    }

  //Run other code


}
