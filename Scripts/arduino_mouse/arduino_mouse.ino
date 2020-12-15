#include<MouseTo.h>
#include<Mouse.h>

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
    while(!move_mouse(&x_int, &y_int));
  }
}

bool move_mouse(int *x, int *y) {
  int jump_distance = 10;
  int x_val = *x;
  int y_val = *y;

  if (x_val != 0 && y_val == 0) {
    int x_move = x_val > 0 ? min(jump_distance, x_val) : max(-jump_distance, x_val);
    *x -= x_move;
    Mouse.move(x_move,0);
    return false; 
  }
  else if (x_val == 0 && y_val != 0) {
    int y_move = y_val > 0 ? min(jump_distance, y_val) : max(-jump_distance, y_val);
    *y -= y_move;
    Mouse.move(0, y_move);
    return false;
  }
  else if (x_val != 0 && y_val != 0) {
    int x_move = x_val > 0 ? min(jump_distance, x_val) : max(-jump_distance, x_val);
    *x -= x_move;
    int y_move = y_val > 0 ? min(jump_distance, y_val) : max(-jump_distance, y_val);
    *y -= y_move;
    Mouse.move(x_move, y_move);
    return false;
  }
  return true;
}

//bool move_mouse(int *x, int *y) {
//  int jump_distance = 10;
//  int x_val = *x;
//  int y_val = *y;
//
//  if (x_val != 0 && y_val == 0) {
//    int x_move = x_val > 0 ? min(jump_distance, x_val) : max(-jump_distance, x_val);
//    x_val -= x_move;
//    Mouse.move(x_move,0);
//    return false; 
//  }
//  else if (x_val == 0 && y_val != 0) {
//    int y_move = y_val > 0 ? min(jump_distance, y_val) : max(-jump_distance, y_val);
//    y_val -= y_move;
//    Mouse.move(0, y_move);
//    return false;
//  }
//  else if (x_val != 0 && y_val != 0) {
//    int x_move = x_val > 0 ? min(jump_distance, x_val) : max(-jump_distance, x_val);
//    x_val -= x_move;
//    int y_move = y_val > 0 ? min(jump_distance, y_val) : max(-jump_distance, y_val);
//    y_val -= y_move;
//    Mouse.move(x_move, y_move);
//    return false;
//  }
//  return true;
//}
