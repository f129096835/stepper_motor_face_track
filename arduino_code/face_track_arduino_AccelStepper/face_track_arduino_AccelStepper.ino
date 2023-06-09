//Face Tracker using TensorRT and PID by Ed
#include <MultiStepper.h>
#include <AccelStepper.h>

#define DRIVER_TYPE     1
#define MOTOR_PUL_PIN   4
#define MOTOR_DIR_PIN   5
#define MOTOR_SPEED 600
#define MOTOR_POS HIGH
#define MOTOR_NEG LOW
#define width  640
#define height  480
int x_stop_range = width*0.04;
int y_stop_range = height*0.04;
int x_mid = 0; 
int y_mid = 0;


AccelStepper motor(DRIVER_TYPE, MOTOR_PUL_PIN, MOTOR_DIR_PIN); // Define the motor object

void setup() {
Serial.begin(9600);
motor.setMaxSpeed(1000); //Speed = steps/second
motor.setAcceleration(1000);
}

void loop() {
 if (Serial.available() > 0)
   Mod2_move();
}
void Mod2_move(){
if (Serial.read() == 'X')
    {
      x_mid = Serial.parseInt();// read center x-coordinate
      if (Serial.read() == 'Y')
        y_mid = Serial.parseInt(); // read center y-coordinate
    }
    if (x_mid > width / 2 && abs((x_mid - width / 2))>=x_stop_range)
      move_stepper(MOTOR_SPEED, MOTOR_POS);
    if (x_mid < width / 2 && abs((x_mid - width / 2))>=x_stop_range)
      move_stepper(MOTOR_SPEED, MOTOR_NEG);
}
      
void move_stepper(int stepper, int dir){
   for(int x=0; x<stepper; x++ ){
    if(dir==LOW){
      motor.setSpeed(1000);
      motor.move(1);
      motor.runSpeed();
    }
    if(dir==HIGH){
      motor.setSpeed(-1000);
      motor.move(-1);
      motor.runSpeed();
    }
   }
  }
