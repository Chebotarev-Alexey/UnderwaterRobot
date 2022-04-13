class Button{
  private:
  public:
    byte pin;
    void init (byte _pin) {
      pin = _pin;
      pinMode(pin, INPUT);
      }
    bool read (){
      return !digitalRead(pin);
      }
};
