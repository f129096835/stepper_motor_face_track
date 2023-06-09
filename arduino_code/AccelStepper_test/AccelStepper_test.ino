#include <AccelStepper.h>

//stepper pin
#define DRIVER_TYPE     1
#define MOTOR_STP_PIN   2
#define MOTOR_DIR_PIN   3

// 定义步进电机对象
AccelStepper motor(DRIVER_TYPE, MOTOR_STP_PIN, MOTOR_DIR_PIN);

void setup() {
  motor.setMaxSpeed(1000);
  motor.setAcceleration(1000);
}

void loop() {
  //正轉
  //motor.setSpeed(1000);
  motor.move(-1000);
  motor.run();
  

  //反轉
  //motor.setSpeed(-1000);
  //motor.move(-1000);
  //motor.runSpeed();

}
