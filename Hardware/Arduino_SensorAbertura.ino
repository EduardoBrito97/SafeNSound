#define buttonPin 4
#define sensorPin 7
#define onboardLED 13 //Uno

bool buttonState = false;
bool sensorState = false;
bool previousButtonState = false;
bool previousSensorState = false;

void setup(){
  pinMode(onboardLED, OUTPUT);
  pinMode(buttonPin, INPUT);
  pinMode(sensorPin, INPUT);

  sensorState = digitalRead(sensorPin);
  digitalWrite(onboardLED, sensorState);
  previousSensorState = sensorState;
}

bool sensorAbertura(){
  sensorState = digitalRead(sensorPin);
  
  if(sensorState == HIGH && previousSensorState == LOW){
    previousSensorState = sensorState;
    digitalWrite(onboardLED, sensorState);
    
    return false;
  }
  else if(sensorState == LOW && previousSensorState == HIGH){
    previousSensorState = sensorState;
    digitalWrite(onboardLED, sensorState);

    return true;
  }
}

void loop(){
  bool containerState;
  
  containerState = sensorAbertura();
  delay(150);
}
