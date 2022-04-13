#include <Servo.h>
#include "SwimmingRobot.h"
#include <NeoSWSerial.h>

const byte X_PINS[2] = {4, 5};//заменить на {левый передний, правый задний} моторы
const byte Y_PINS[2] = {6, 7};//заменить на {правый передний, левый задний} моторы
const byte D_PINS[2] = {8, 9};//установить два моторов на всплытие/погружение

/* Установить реверсы следуя картике 
(чтобы горизонтальные моторы имели положительное направление со стороны звездочек,
а вертикальные - положительное направление на всплытие}

     *  *
    /    \
     
    *    *
     \  /
*/

const bool X_REVERSE[2] = {0,0};// опять же левый передний, правый задний
const bool Y_REVERSE[2] = {0,0};// правый передний, левый задний
const bool D_REVERSE[2] = {0,0};// всплытие/погружение
//
////скорости движения градусы/миллисекунды и границы камеры:
#define CAMERA_ROTATE_SPEED 0.05
#define CAMERA_ROTATE_TOP_LIMIT 135
#define CAMERA_ROTATE_BOTTOM_LIMIT 45
#define CAMERA_ROTATE_PIN 10
//
////скорости движения градусы/миллисекунды и границы манипулятора:
//
//#define MANIPULATOR_UP_SPEED 1 (пока отключено)
//#define MANIPULATOR_DOWN_SPEED -1 (пока отключено)
#define MANIPULATOR_OPEN 135
#define MANIPULATOR_CLOSE 45
#define MANIPULATOR_PIN 52

//Я не знаю, как будет на длинном проводе, поэтому вы можете увеличивать и уменьшать значение (вместе с конфигом в питоне):
#define SERIAL_SPEED 9600


//пин переключения направления rs:
#define RSPIN 11

NeoSWSerial mySerial(13, 12); //Здесь можете выбрать подходящий сериал

//Далее идет не конфиг

Servo manipulator, camera_rotate;
char x, y, d, r, cam_sign, cam_abs;
float camera_val;
SwimmingRobot swimming_robot;

#include "SerialServer.h"
#define DEC_LEN 4
#define BIN_LEN 3

long int prev_time = millis();
int delta;

void set_x(char val) {
  x = val;
}
void set_y(char val) {
  y = val;
}
void set_r(char val) {
  r = val;
}
void set_d(char val) {
  d = val;
}
void manipulator_set(bool val) {
//  Serial.print("man: ");
//  Serial.print(val);
//  Serial.print("  ");
  manipulator.write(val*MANIPULATOR_OPEN+(!val)*MANIPULATOR_CLOSE);
}
void camera_update() {
  camera_val = min(max(camera_val+cam_abs*(cam_sign*2-1)*CAMERA_ROTATE_SPEED*delta, CAMERA_ROTATE_BOTTOM_LIMIT), CAMERA_ROTATE_TOP_LIMIT);
  camera_rotate.write(camera_val);
  }
void camera_abs_set(bool val) {
//  Serial.print("cam_abs: ");
//  Serial.print(val);
//  Serial.print("  ");
  cam_abs = val;
}
void camera_sign_set(bool val) {
//  Serial.print("cam: ");
//  Serial.print(camera_val);
//  Serial.print("  ");
//
//  Serial.print("cam_sign: ");
//  Serial.print(val);
//  Serial.print("  ");
  cam_sign = val;
}

void (*functions[7]) (char) = {set_x, set_y, set_r, set_d, camera_sign_set, camera_abs_set, manipulator_set};//по техническим причинам, бинарные данные в обратном порядке

char* handler(char *msg) {
//  Serial.println();
//  Serial.print("msg:  ");
//  Serial.print(msg);
//  Serial.print("  ");
  if (strlen(msg) < 2) {
    return "1234";
  }
  for (byte i = 0; i < DEC_LEN; i++) {
    (*functions[i])(msg[i] - 44);
  }
  byte i = 0;
  byte bit_i = 0;
  byte symb_i = 0;
  while (i < BIN_LEN) {
    if (bit_i > 5) {
      bit_i = 0;
      symb_i += 1;
    }
    (*functions[i + DEC_LEN])((bool) bitRead(( (byte) msg[symb_i+DEC_LEN]) - 33, bit_i));
    i++;
    bit_i++;
  }
  return "9876";
}

RS485Server serial_server = RS485Server(mySerial, 9600, handler, RSPIN);

void setup() {
  swimming_robot.init(D_PINS, X_PINS, Y_PINS, D_REVERSE, X_REVERSE, Y_REVERSE);
  delay(2000);
  swimming_robot.init1();
  delay(2000);
  swimming_robot.init2();
  delay(2000);
  swimming_robot.init3();
  delay(2000);
  
Serial.begin(115200); //включать для отладки
  mySerial.begin(SERIAL_SPEED);
  manipulator.attach(MANIPULATOR_PIN);
  camera_rotate.attach(CAMERA_ROTATE_PIN);
}
void loop() {
  serial_server.run();
  delay(1);
}

void yield(){
  
  delta = millis()-prev_time;
  prev_time = millis();

  swimming_robot.swim(x, y, d, r);
  camera_update();
  Serial.println();
  }
