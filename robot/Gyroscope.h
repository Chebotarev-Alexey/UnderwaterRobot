#include <SoftwareSerial.h>
class GyroscopeSoftwareSerial {
  public:
    GyroscopeSoftwareSerial (byte RXPin, byte TXPin) : _serial(RXPin, TXPin) {};
    SoftwareSerial _serial;
    
    float yaw;
    unsigned char Re_buf[8], counter = 0;

    void init () {
      _serial.begin(9600);
    }
    void init1 () {
      _serial.write(0XA5);
      _serial.write(0X54);//correction mode
    }
    void init2 () {
      _serial.write(0XA5);
      _serial.write(0X51);//0X51:query mode, return directly to the angle value, to be sent each read, 0X52:Automatic mode,send a direct return angle, only initialization
    }
    float read () {
      _serial.write(0XA5);
      _serial.write(0X51); //send it for each read
      while (_serial.available()) {
        Re_buf[counter] = (unsigned char)_serial.read();
        if (counter == 0 && Re_buf[0] != 0xAA) return yaw;
        counter++;
        if (counter == 8) //package is complete
        {
          counter = 0;
          if (Re_buf[0] == 0xAA && Re_buf[7] == 0x55) // data package is correct
          {
            yaw = (int16_t)(Re_buf[1] << 8 | Re_buf[2]) / 100.00;
            return yaw;
          }
        }
      }
      return yaw;
    }
};
