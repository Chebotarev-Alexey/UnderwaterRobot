class RS485Server {
  public:
    RS485Server (Stream &serial, int speed1, char* (*handler)(char*), byte rspin) : serial(serial) {
      this->serial = serial;
      this->speed = speed;
      this->handler = handler;
      this->rspin = rspin;
      pinMode(this->rspin, OUTPUT);
      digitalWrite(this->rspin, LOW);
    }
    void run() {
      while (this->serial.available() > 0) {
        char symb = this->serial.read();
        if ((byte) symb == 10) {
          digitalWrite(this->rspin, HIGH);
          char* ans = this->handler(this->buffer);
          this->serial.write(ans);
          this->serial.write(10);
          delay(40);
          digitalWrite(this->rspin, LOW);
          memset(this->buffer, 0, sizeof this->buffer);
        }
        else {
          strncat(buffer, &symb, 1);
        }
      }
    }
  private:
    Stream &serial;
    int speed;
    char* (*handler)(char*);
    char buffer[255];
    byte rspin;
};
