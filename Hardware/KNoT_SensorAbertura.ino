#include <KNoTThing.h>

#define OPENING_SENSOR_PIN    2
#define OPENING_SENSOR_NAME   "Opening Sensor"
#define OPENING_SENSOR_ID     69

KNoTThing thing;

static int sensor_read(uint8_t *val)
{
  *val = digitalRead(OPENING_SENSOR_PIN);
  
  Serial.print("Sensor Status: ");
  if(*val)
    Serial.println(F("Closed"));
  else
    Serial.println(F("Open"));
  return 0;
}

static int sensor_write(uint8_t *val)
{
    digitalWrite(OPENING_SENSOR_PIN, *val);
    
    Serial.print(F("Sensor Status: "));
    if (*val)
      Serial.println(F("Closed"));
    else
      Serial.println(F("Open"));
      /* TODO: Save light status in EEMPROM in to handle when reboot */
    return 0;
}

void setup(){
  Serial.begin(9600);
  
  pinMode(OPENING_SENSOR_PIN,   INPUT);
  
  thing.init("Bag");
  thing.registerBoolData(OPENING_SENSOR_NAME, OPENING_SENSOR_ID, KNOT_TYPE_ID_SWITCH,
    KNOT_UNIT_NOT_APPLICABLE, sensor_read, sensor_write);

  thing.registerDefaultConfig(OPENING_SENSOR_ID, KNOT_EVT_FLAG_TIME, 1, 0, 0, 0, 0);

  Serial.println(F("Remote Opening Sensor KNoT"));
}

void loop(){
  thing.run();
}
