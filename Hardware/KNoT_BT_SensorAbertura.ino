#include <KNoTThing.h>
#include <SoftwareSerial.h>

#define OPENING_SENSOR_PIN    2
#define OPENING_SENSOR_NAME   "Opening Sensor"
#define OPENING_SENSOR_ID     69

#define BLUETOOTH_SENSOR_PIN  3
#define BLUETOOTH_POWER_PIN   4
#define BLUETOOTH_AT_PIN      5
#define BLUETOOTH_TX_PIN      A0
#define BLUETOOTH_RX_PIN      A1
#define BLUETOOTH_SENSOR_NAME "Bluetooth Sensor"
#define BLUETOOTH_SENSOR_ID   96

bool BTConnectionStatus;
bool previousBTConnectionStatus;
bool BTATStatus;
/*
String SerialString;
SoftwareSerial BTSerial(BLUETOOTH_TX_PIN, BLUETOOTH_RX_PIN); //Arduino (RX, TX) - Bluetooth (TX, RX)
*/
KNoTThing thing;

static int open_sensor_read(uint8_t *val)
{
  *val = digitalRead(OPENING_SENSOR_PIN);
  
  Serial.print("Sensor Status: ");
  if(*val)
    Serial.println(F("Closed"));
  else
    Serial.println(F("Open"));
  return 0;
}

static int bluetooth_sensor_read(uint8_t *val)
{
  *val = !digitalRead(BLUETOOTH_SENSOR_PIN);
  
  Serial.print("Bluetooth Status: ");
  if(*val)
    Serial.println(F("Connected"));
  else
    Serial.println(F("Disconnected"));
  return 0;
}

/*
String getStringFromSerial()
{
  String str;

  if(Serial.available() > 0)
  {
    str = Serial.readStringUntil('\n');
    Serial.println(str);
  }

  str.trim();

  return str;
}

void enterATMode(){
  BTSerial.begin(38400);
  delay(250);
  
  digitalWrite(BLUETOOTH_SENSOR_PIN, LOW);
  delay(250);

  digitalWrite(BLUETOOTH_AT_PIN, HIGH);
  delay(250);

  digitalWrite(BLUETOOTH_SENSOR_PIN, HIGH);
  delay(250);

  Serial.println("BT on AT Mode");
  BTATStatus = true;
}

void exitATMode(){
  BTSerial.end();
  delay(250);
  
  digitalWrite(BLUETOOTH_SENSOR_PIN, LOW);
  delay(250);

  digitalWrite(BLUETOOTH_AT_PIN, LOW);
  delay(250);

  digitalWrite(BLUETOOTH_SENSOR_PIN, HIGH);
  delay(250);

  Serial.println("BT out of AT Mode");
  BTATStatus = false;
}

void BTConnectionCheck(){
  BTConnectionStatus = !digitalRead(BLUETOOTH_SENSOR_PIN);

  if(BTConnectionStatus == !previousBTConnectionStatus){
    if(BTConnectionStatus == HIGH){
      Serial.println("Container conectado");
    }
    else{
      Serial.println("Container desconectado");
    }
  }
  
  previousBTConnectionStatus = BTConnectionStatus;

  delay(250);
}
*/

void setup(){
  Serial.begin(9600);

  while(!Serial);
  
  pinMode(OPENING_SENSOR_PIN,   INPUT);
  pinMode(BLUETOOTH_SENSOR_PIN, INPUT);  
  pinMode(BLUETOOTH_POWER_PIN, OUTPUT);
  pinMode(BLUETOOTH_AT_PIN, OUTPUT);

  digitalWrite(BLUETOOTH_POWER_PIN, HIGH);
  digitalWrite(BLUETOOTH_AT_PIN, LOW);  

  //BTConnectionStatus = digitalRead(BLUETOOTH_SENSOR_PIN);
  //previousBTConnectionStatus = BTConnectionStatus;

  BTATStatus = false;

  Serial.println("Bluetooth ready!"); 
   
  thing.init("Container");
  thing.registerBoolData(OPENING_SENSOR_NAME, OPENING_SENSOR_ID, KNOT_TYPE_ID_SWITCH,
    KNOT_UNIT_NOT_APPLICABLE, open_sensor_read, NULL);
  thing.registerBoolData(BLUETOOTH_SENSOR_NAME, BLUETOOTH_SENSOR_ID, KNOT_TYPE_ID_SWITCH,
    KNOT_UNIT_NOT_APPLICABLE, bluetooth_sensor_read, NULL);

  thing.registerDefaultConfig(OPENING_SENSOR_ID, KNOT_EVT_FLAG_TIME, 1, 0, 0, 0, 0);
  thing.registerDefaultConfig(BLUETOOTH_SENSOR_ID, KNOT_EVT_FLAG_TIME, 1, 0, 0, 0, 0);

  Serial.println(F("Remote Opening Sensor KNoT"));
}

void loop(){
  thing.run();

  /*if(BTSerial.available()){
    Serial.write(BTSerial.read());
  }

  SerialString = getStringFromSerial();

  if(SerialString == "ATMode"){
    enterATMode();
  }

  if(BTATStatus == true){
    if(SerialString == "exitATMode"){
      exitATMode();
    }
    
    if(SerialString != ""){
      BTSerial.println(SerialString);
    }
  }
  else{
    digitalWrite(BLUETOOTH_RX_PIN, LOW);
   
    BTConnectionCheck();
  }*/
}
