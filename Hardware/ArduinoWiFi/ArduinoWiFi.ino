#include <SoftwareSerial.h>

#define CH_PD 5 // EN
#define RST 6
#define GPIO0 7
#define buttonPin 4

SoftwareSerial ESPSerial(2, 3); //RX, TX
int buttonState = 0;
int previousButtonState = 0;
String ssid = "GVT-501F";
String password = "CP1211RMHRE";
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

  digitalWrite(CH_PD, HIGH);
  //digitalWrite(RST, HIGH);
  //digitalWrite(GPIO0, HIGH);
  digitalWrite(13, LOW);

  Serial.begin(9600);
  ESPSerial.begin(9600);
  delay(200);
  Serial.println("ESP8266 ready to take AT commands!");

  //wifiConnect("GVT-501F", "CP1211RMHRE");
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
    wifiConnect(ssid, password);
    
    delay(100);
  }
  
  previousButtonState = buttonState;
}
