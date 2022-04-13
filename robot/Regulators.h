class Regulator {
  public:
    const static int standart_map_values[4];
    byte k;
    int *map_values;
    void init (byte _k, int _map_values[4] = standart_map_values){
      k = _k;
      map_values = _map_values;
      }
    int p(int tagret);
    };
class AngularRegulator : public Regulator {
  public:
    int _min; 
    int _max;
    void init (byte _k, int __min = -180, int __max = 180, int _map_values[4] = standart_map_values) {
      k = _k;
      map_values = _map_values;
      _min = __min;
      _max = __max;
      }
    int p (int target, int feedback_value) {
      int errors[3] = {target - feedback_value, (target - _max) + (_min - feedback_value), (target - _min) + (_max - feedback_value)};
      int min_error = _max-_min;
      for (byte error_index = 0; error_index<3; error_index++) {
        if(abs(errors[error_index])<abs(min_error)){
          min_error = errors[error_index];
          }
        }
      int velocity = map(min_error, map_values[0], map_values[1], map_values[2], map_values[3])*k;
      return velocity;
    }
  };
class LinearRegulator : public Regulator {
  public:
    int p (int target, int feedback_value) {
      int error = target - feedback_value;
      int velocity = map(error, map_values[0], map_values[1], map_values[2], map_values[3])*k;
      return velocity;
    }
};
