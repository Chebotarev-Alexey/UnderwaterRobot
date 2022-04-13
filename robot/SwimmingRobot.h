#define D_NUM 2
#define X_NUM 2
#define Y_NUM 2
class SwimmingRobot {
  private:
  #include "BLMotor.h"
  public:


    BLMotor d_motors[D_NUM];
    BLMotor x_motors[X_NUM];
    BLMotor y_motors[Y_NUM];

    bool up_direction;
    bool linear_direction;

    byte linear_motors_number;
    byte up_motors_number;
    void init (const byte d_pins[D_NUM], const byte x_pins[X_NUM], const byte y_pins[Y_NUM], bool d_reverse[D_NUM], bool x_reverse[X_NUM], bool y_reverse[Y_NUM]) {
      for (byte i = 0; i < D_NUM; i++) {
        this->d_motors[i].init(d_pins[i], d_reverse[i], 1000, 2000, 1500);
        this->d_motors[i].init1(2000);
      }
      for (byte i = 0; i < X_NUM; i++) {
        if (x_pins[i] == 5){
          this->x_motors[i].init(x_pins[i], x_reverse[i], 800, 2000, 1470);
        }
        else {
          this->x_motors[i].init(x_pins[i], x_reverse[i], 800, 2000, 1480);
        }
        this->x_motors[i].init1(2000);
      }
      for (byte i = 0; i < Y_NUM; i++) {
        if (y_pins[i] == 5){
          this->x_motors[i].init(x_pins[i], x_reverse[i], 800, 2000, 1470);
        }
        else {
          this->y_motors[i].init(y_pins[i], y_reverse[i], 800, 2000, 1480);
        }
        this->y_motors[i].init1(2000);
      }
    }

    void init1 () {
      for (byte i = 0; i < D_NUM; i++) {
        this->d_motors[i].init1(1000);
      }
      for (byte i = 0; i < X_NUM; i++) {
        this->x_motors[i].init1(800);
      }
      for (byte i = 0; i < Y_NUM; i++) {
        this->y_motors[i].init1(800);
      }
    }
    void init2(){
      for (byte i = 0; i < D_NUM; i++) {
        this->d_motors[i].init1(1500);
      }
      for (byte i = 0; i < X_NUM; i++) {
        this->x_motors[i].init1(1400);
      }
      for (byte i = 0; i < Y_NUM; i++) {
        this->y_motors[i].init1(1400);
      }
    }
    void init3(){
      for (byte i = 0; i < D_NUM; i++) {
        this->d_motors[i].init1(0);
      }
      for (byte i = 0; i < X_NUM; i++) {
        this->x_motors[i].init1(0);
      }
      for (byte i = 0; i < Y_NUM; i++) {
        this->y_motors[i].init1(0);
      }
    }
    void swim (char x, char y, char r, char d) {
      for (byte i = 0; i < D_NUM; i++) {
        this->d_motors[i].run(d);
      }
      x_motors[0].run(x + r);
      x_motors[1].run(x - r);
      y_motors[0].run(y - r);
      y_motors[1].run(y + r);
    }
};
