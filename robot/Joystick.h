//#include <AlignedJoy.h>
class Joystick{
  private:
  public:
//  AlignedJoy joystick;
  byte xPin;
  byte yPin;
  int result[2];
  int *middle;
  void init (const byte pins[], int middle[]) {
    xPin = pins[0];
    yPin = pins[1];
    this->middle = middle;
    pinMode(xPin,INPUT);
    pinMode(yPin,INPUT);
//    joystick.middleCalibration(1000);
    }
  int* get(){
    return result;
    }
  byte* read () {
    int yValue = analogRead(yPin);
    int xValue = analogRead(xPin);
    int yResult;
    int xResult;  
    if (yValue<middle[1]-3) yResult = map(yValue, 0, middle[1], -9,0);
    else if (yValue>middle[1]+3) yResult = map(yValue, middle[1], 1023, 0,9);
    else yResult = 0;
    
    if (xValue<middle[0]-3) xResult = map(xValue, 0, middle[0], -9,0);
    else if (xValue>middle[0]+3) xResult = map(xValue, middle[0], 1023, 0,9);
    else xResult = 0;
    
    result[0] = -xResult;
    result[1] = yResult;
    }
  };
