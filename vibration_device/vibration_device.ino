const int motorPin = 3;  //use a pwm pin
uint8_t motor_intensity = 0;


void setup() {
  Serial.begin(9600);
  pinMode(motorPin, OUTPUT);

}

void loop() {
  if (Serial.available() >= 1) {

    motor_intensity = Serial.read();

    if(motor_intensity>0){
      analogWrite(motorPin, motor_intensity);
      // digitalWrite(motorPin, HIGH);

    } else {
      digitalWrite(motorPin, LOW);
    }
    
  }

}
