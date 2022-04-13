class Gamepad {
  private:
  #include "Button.h"
  #include "Joystick.h"
  public:
    Button buttons[10];
    Joystick joystick;
    int buttons_number;
    bool buttons_results[10];
    
    void init (const byte buttons_pins[], byte _buttons_number, const byte joystick_pins[], int joystick_middle[]) {
      buttons_number = _buttons_number;
      for (byte button_index = 0; button_index<buttons_number; button_index++) {
        buttons[button_index].init(buttons_pins[button_index]);
        }
      joystick.init(joystick_pins, joystick_middle);
    }
    bool* get_buttons() {
      return buttons_results;
      };
    int* get_joystick() {
      return joystick.get();
      };
    void read (){
      for (byte button_index = 0; button_index<buttons_number; button_index++) {
        buttons_results[button_index] = buttons[button_index].read();
        }
      joystick.read();
    }
      
  };
