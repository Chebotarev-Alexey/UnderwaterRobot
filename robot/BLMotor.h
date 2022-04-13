#define MOTORS_MIN 800
#define MOTORS_MAX 2100
#define MOTORS_CENTER 1480
class BLMotor {
  private:
  public:
    Servo motor;
    int _min;
    int _max;
    int center;
    byte pin;
    bool reverse;
    void init(const byte pin, bool reverse = 0, int _min = MOTORS_MIN, int _max = MOTORS_MAX, int center = MOTORS_CENTER) {
      this->motor.attach(pin);
      this->_min = _min;
      this->_max = _max;
      this->center = center;
      this->pin = pin;
      this->reverse = reverse;
      }
    void init1(int init_value = MOTORS_CENTER) {
     this->motor.writeMicroseconds(init_value);
      }

    void run(char speed) {
      Serial.print("  motor");
      Serial.print(pin);
      Serial.print("  ");
      int speed_raw;
      if (speed <= 0){
        speed_raw = map(speed, -10, 0, _min, center);
        }
      else {
        speed_raw = map(speed, 0, 10, center, _max);
        }
      Serial.print(speed_raw);
      this->motor.writeMicroseconds(speed_raw*(this->reverse*2-1));
      }
    
  };
