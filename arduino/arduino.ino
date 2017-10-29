#include <SoftwareSerial.h>
#define SOFT_RX 2
#define SOFT_TX 3
SoftwareSerial my_serial(SOFT_RX,SOFT_TX);

#include <TinyGPS++.h>
TinyGPSPlus gps;

void setup() {
  Serial.begin(9600);
  my_serial.begin(9600);
}

void loop() {
  if (my_serial.available()) {
    gps.encode(my_serial.read());
    if (gps.location.isUpdated()) {
      Serial.print("LAT="); Serial.print(gps.location.lat(), 6);
      Serial.print("LNG="); Serial.println(gps.location.lng(), 6);

      Serial.print("lat="); Serial.println(gps.location.lat(), 6); // Latitude in degrees (double)
      Serial.print("lng="); Serial.println(gps.location.lng(), 6); // Longitude in degrees (double)
      Serial.print("raw lat negative="); Serial.print(gps.location.rawLat().negative ? "-" : "+");
      Serial.print("raw lat deg="); Serial.println(gps.location.rawLat().deg); // Raw latitude in whole degrees
      Serial.print("billionths="); Serial.println(gps.location.rawLat().billionths);// ... and billionths (u16/u32)
      Serial.print(gps.location.rawLng().negative ? "-" : "+");
      Serial.println(gps.location.rawLng().deg); // Raw longitude in whole degrees
      Serial.println(gps.location.rawLng().billionths);// ... and billionths (u16/u32)
      Serial.println(gps.date.value()); // Raw date in DDMMYY format (u32)
      Serial.println(gps.date.year()); // Year (2000+) (u16)
      Serial.println(gps.date.month()); // Month (1-12) (u8)
      Serial.println(gps.date.day()); // Day (1-31) (u8)
      Serial.println(gps.time.value()); // Raw time in HHMMSSCC format (u32)
      Serial.println(gps.time.hour()); // Hour (0-23) (u8)
      Serial.println(gps.time.minute()); // Minute (0-59) (u8)
      Serial.println(gps.time.second()); // Second (0-59) (u8)
      Serial.println(gps.time.centisecond()); // 100ths of a second (0-99) (u8)
      Serial.print("speed raw="); Serial.println(gps.speed.value()); // Raw speed in 100ths of a knot (i32)
      Serial.print("speed mps="); Serial.println(gps.speed.mps()); // Speed in meters per second (double)
      Serial.println(gps.speed.kmph()); // Speed in kilometers per hour (double)
      Serial.print("course="); Serial.println(gps.course.value()); // Raw course in 100ths of a degree (i32)
      Serial.println(gps.course.deg()); // Course in degrees (double)
      Serial.print("altitude="); Serial.println(gps.altitude.value()); // Raw altitude in centimeters (i32)
      Serial.println(gps.altitude.meters()); // Altitude in meters (double)
      Serial.println(gps.altitude.kilometers()); // Altitude in kilometers (double)
      Serial.print("nb sat="); Serial.println(gps.satellites.value()); // Number of satellites in use (u32)
      Serial.print("horiz dim of precision="); Serial.println(gps.hdop.value()); // Horizontal Dim. of Precision (100ths-i32)
    }
  }
}
