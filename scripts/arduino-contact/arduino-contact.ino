#include <Mouse.h>
#include <hiduniversal.h>
#include <SPI.h>
#include "hidmouserptparser.h"
#include <Wire.h>
#include <usbhub.h>

USB Usb;
HIDUniversal Hid(&Usb);
HIDMouseEvents MouEvents;
HIDMouseReportParser Mou(&MouEvents);
int dx;
int dy;
int dxn;
int dyn;
int index = 0;
int num_size = 0;
int length;


void setup()
{
    Mouse.begin();
    Serial.begin(115200);
    Serial.setTimeout(1);
    Serial.println("Start");

    if (Usb.Init() == -1)
        Serial.println("OSC did not start.");
    delay(50);

    if (!Hid.SetReportParser(0, &Mou))
        ErrorMessage<uint8_t>(PSTR("SetReportParser"), 1);
}

void loop()
{
    if (Serial.available())
    {

        String data = Serial.readString();
        if (data == "shoot")
        {
            Mouse.click();
        }

        else if (data.substring(0, 6) == "silent")
        {
            data.remove(0, 6);
            index = 0;
            num_size = data.indexOf(":", index);
            dx = data.substring(index, num_size).toInt();
            data.remove(0, num_size + 1);
            dy = data.toInt();
            dxn = dx * -1;
            dyn = dy * -1;

            if (dx > 0)
            {
                while (dx > 127)
                {
                    dx -= 127;
                    Mouse.move(127, 0);
                }
                Mouse.move(dx, 0);
            }
            else if (dx < 0)
            {
                while (dx < -127)
                {
                    dx += 127;
                    Mouse.move(-127, 0);
                }
                Mouse.move(dx, 0);
            }
            if (dy >= 0)
            {
                while (dy > 127)
                {
                    dy -= 127;
                    Mouse.move(0, 127);
                }
                Mouse.move(0, dy);
            }
            else if (dy <= 0)
            {
                while (dy < -127)
                {
                    dy += 127;
                    Mouse.move(0, -127);
                }
                Mouse.move(0, dy);
            }
            Mouse.click();
            if (dxn > 0)
            {
                while (dxn > 127)
                {
                    dxn -= 127;
                    Mouse.move(127, 0);
                }
                Mouse.move(dxn, 0);
            }
            else if (dxn < 0)
            {
                while (dxn < -127)
                {
                    dxn += 127;
                    Mouse.move(-127, 0);
                }
                Mouse.move(dxn, 0);
            }
            if (dyn > 0)
            {
                while (dyn > 127)
                {
                    dyn -= 127;
                    Mouse.move(0, 127);
                }
                Mouse.move(0, dyn);
            }
            else if (dyn < 0)
            {
                while (dyn < -127)
                {
                    dyn += 127;
                    Mouse.move(0, -127);
                }
                Mouse.move(0, dyn);
            }
        }

        else
        {
            index = 0;
            num_size = data.indexOf(":", index);
            dx = data.substring(index, num_size).toInt();
            data.remove(0, num_size + 1);
            dy = data.toInt();
            // Serial.println(dx+":"+dy);
            if (dx > 0)
            {
                while (dx > 20)
                {
                    dx -= 20;
                    Mouse.move(20, 0);
                }
                Mouse.move(dx, 0);
            }
            else if (dx < 0)
            {
                while (dx < -20)
                {
                    dx += 20;
                    Mouse.move(-20, 0);
                }
                Mouse.move(dx, 0);
            }
            if (dy >= 0)
            {
                while (dy > 20)
                {
                    dy -= 20;
                    Mouse.move(0, 20);
                }
                Mouse.move(0, dy);
            }
            else if (dy <= 0)
            {
                while (dy < -20)
                {
                    dy += 20;
                    Mouse.move(0, -20);
                }
                Mouse.move(0, dy);
            }
        
        }
    }
    else{
        Usb.Task();
    }
    
}