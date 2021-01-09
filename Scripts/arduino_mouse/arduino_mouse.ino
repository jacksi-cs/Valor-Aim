#include<MouseTo.h>
#include<Mouse.h>

boolean is_shooting = false;
float drag_value;

void setup() {
  // put your setup code here, to run once:
  Mouse.begin();
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  while (!Serial.available()) {}
  if (Serial.available() > 0) {
    byte y[2];
    y[1] = Serial.read();
    y[0] = Serial.read();
    
    delay(1);
    byte x[2];
    x[1] = Serial.read();
    x[0] = Serial.read();

    int x_int = int(x[0] << 8 | x[1]);
    int y_int = int(y[0] << 8 | y[1]);

    // Scripts has been turned off, clearing serial buffer
    if (x_int == 32767 || y_int == 32767) {  
      while (Serial.available() > 0) {
        char t = Serial.read();  
      } 
    }
    // Indicator that I am shooting
    else if (x_int == 32766 || y_int == 32766) {
        is_shooting = true;
        drag_value = 0;
    }
    // Indicator that I have stopped shooting
    else if (x_int == 32765 || y_int == 32765) {
      is_shooting = false;
      drag_value = 0;
    }
    else {
      while(!move_mouse(&x_int, &y_int));
    }
  }
}

bool move_mouse(int *x, int *y) {
  int jump_distance = 1; // Can be modified to change smoothness of the mouse movement
  int x_val = *x;
  int y_val = *y;

  if (is_shooting && drag_value >= 0) {
      drag_value = 0.7 + (0.1 * drag_value);
  }

  if (x_val != 0 && y_val == 0) {
    int x_move = x_val > 0 ? min(jump_distance, x_val) : max(-jump_distance, x_val);
    *x -= x_move;
    Mouse.move(x_move, drag_value);
    return false; 
  }
  else if (x_val == 0 && y_val != 0) {
    int y_move = y_val > 0 ? min(jump_distance, y_val) : max(-jump_distance, y_val);
    *y -= y_move;
    Mouse.move(0, y_move + drag_value);
    return false;
  }
  else if (x_val != 0 && y_val != 0) {
    int x_move = x_val > 0 ? min(jump_distance, x_val) : max(-jump_distance, x_val);
    *x -= x_move;
    int y_move = y_val > 0 ? min(jump_distance, y_val) : max(-jump_distance, y_val);
    *y -= y_move;
    Mouse.move(x_move, y_move + drag_value);
    return false;
  }
  return true;
}
