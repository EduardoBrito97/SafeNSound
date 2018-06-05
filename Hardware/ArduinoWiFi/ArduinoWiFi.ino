#include <SoftwareSerial.h>

#define CH_PD 5 // EN
#define RST 6
#define GPIO0 7
#define buttonPin 4
#define sensorPinOut 6
#define sensorPinIn 7

SoftwareSerial ESPSerial(2, 3); //RX, TX
int buttonState = 0;
int sensorState = 1;
int previousButtonState = 0;
int previousSensorState = 0;
String ssid = "CIn-GUESTS2";
String password = "acessocin";
String command;
String strSerial;
bool wifiStatus = false;

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

void stopAndGo(String str)
{
  if(str == "stop")
  {
    Serial.println("System stopped");  
  
    while(getStringFromSerial() != "go")
    {
    }
  
    Serial.println("System running");
  }
}

void reset()
{
  ESPSerial.println("AT+RST\r");
  delay(200);

  wifiStatus = false;

  if(ESPSerial.find("OK"))
  {
    Serial.println("ESP8266 Reset");
  }
}

void wifiConnect(String ssid, String password)
{
  Serial.println("Connecting to " + ssid+"...");
  ESPSerial.println("AT+CWMODE=1\r");\
  delay(150);
  ESPSerial.println("AT+CWJAP=\"" +ssid+"\",\"" + password + "\"");

  digitalWrite(13, HIGH);
}

void getLocalIP()
{
  ESPSerial.println("AT+CIFSR\r");
}

void getStationsIP()
{
  ESPSerial.println("AT+CWLIF\r");
}

void setup() {
  pinMode(CH_PD, OUTPUT);
  pinMode(RST, OUTPUT);
  pinMode(GPIO0, OUTPUT);
  pinMode(13, OUTPUT);
  pinMode(buttonPin, INPUT);
  pinMode(sensorPinOut, OUTPUT);
  pinMode(sensorPinIn, INPUT);

  digitalWrite(CH_PD, HIGH);
  digitalWrite(sensorPinOut, HIGH);
  //digitalWrite(RST, HIGH);
  //digitalWrite(GPIO0, HIGH);
  digitalWrite(13, LOW);

  sensorState = digitalRead(sensorPinIn);
  previousSensorState = sensorState;

  Serial.begin(9600);
  ESPSerial.begin(9600);
  delay(200);
  Serial.println("ESP8266 ready to take AT commands!");
}

void loop() {
  if(ESPSerial.available())
  {
    Serial.write(ESPSerial.read());
  }

  /*if(Serial.available())
  {
    ESPSerial.write(Serial.read());
  }*/

  strSerial = getStringFromSerial();

  stopAndGo(strSerial);
  
  if(strSerial == "connect")
  {
    wifiConnect(ssid, password);
  }
  if(strSerial == "disconnect")
  {
    ESPSerial.println("AT+CWQAP\r");
  }
  else if(strSerial == "reset")
  {
    ESPSerial.println("AT+RST\r");
  }
  else if(strSerial == "getLocalIP")
  {
    getLocalIP();
  }
  else if(strSerial == "getStatus")
  {
    ESPSerial.println("AT+CIPSTATUS\r");
  }
  else if(strSerial == "getStationsIP")
  {
    getStationsIP();
  }
  
  buttonState = digitalRead(buttonPin);
  
  if(buttonState == HIGH && previousButtonState == LOW)
  {
    Serial.println("Botão Pressionado");    
    delay(100);
  }
  
  previousButtonState = buttonState;

  sensorState = digitalRead(sensorPinIn);

  //Serial.println(digitalRead(sensorPinIn));
  
  if(sensorState == HIGH && previousSensorState == LOW)
  {
    Serial.println("Bolsa fechou");    
    delay(100);
  }
  else if(sensorState == LOW && previousSensorState == HIGH)
  {
    Serial.println("Bolsa abriu");
    delay(100);
  }
  
  previousSensorState = sensorState;
}
