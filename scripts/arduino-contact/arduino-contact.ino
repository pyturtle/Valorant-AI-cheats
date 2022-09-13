#include <Mouse.h>
#include <hiduniversal.h>
#include <SPI.h>
#include "hidmouserptparser.h"

USB Usb;
HIDUniversal Hid(&Usb);
HIDMouseEvents MouEvents;
HIDMouseReportParser Mou(&MouEvents);

int dx;
int dy;
int dxn;
int dyn;
int index;
int num_size;
int jump = 127;


void setup() {
    Mouse.begin();
    Serial.begin(115200);
    Serial.println("Start");
    Serial.setTimeout(1);
    if (Usb.Init() == -1)
        Serial.println("OSC did not start.");
        delay(200);

    if (!Hid.SetReportParser(0, &Mou))
       ErrorMessage<uint8_t > (PSTR("SetReportParser"), 1);
}

void loop() {

    if (Serial.available())
    {

        

        String data = Serial.readString();
        if (data =="shoot"){
            Mouse.click();
        }
        else if (data.substring(0,6) == "silent")
        {
            data.remove(0,6);
            index = 0;
            num_size = data.indexOf(":", index);
            dx = data.substring(index,num_size).toInt();
            data.remove(0,num_size+1);
            dy = data.toInt();
            dxn = dx *-1;
            dyn = dy *-1;

            if (dx > 0){
                while (dx > 127)
                {
                    dx -= 127;
                    Mouse.move(127,0);
                }
                Mouse.move(dx,0);
            }
            else if (dx < 0){
                while (dx < -127)
                {
                    dx += 127;
                    Mouse.move(-127,0);
                }
                Mouse.move(dx,0);
            }
            if (dy > 0){
                while (dy > 127)
                {
                    dy -= 127;
                    Mouse.move(0,127);
                }
                Mouse.move(0,dy);
            }
            else if (dy < 0){
                while (dy < -127)
                {
                    dy += 127;
                    Mouse.move(0,-127);
                }
                Mouse.move(0,dy);
            }
            Mouse.click();
            if (dxn > 0){
                while (dxn > 127)
                {
                    dxn -= 127;
                    Mouse.move(127,0);
                }
                Mouse.move(dxn,0);
            }
            else if (dxn < 0){
                while (dxn < -127)
                {
                    dxn += 127;
                    Mouse.move(-127,0);
                }
                Mouse.move(dxn,0);
            }
            if (dyn > 0){
                while (dyn > 127)
                {
                    dyn -= 127;
                    Mouse.move(0,127);
                }
                Mouse.move(0,dyn);
            }
            else if (dyn < 0){
                while (dyn < -127)
                {
                    dyn += 127;
                    Mouse.move(0,-127);
                }
                Mouse.move(0,dyn);
            }
        }

        else{
            index = 0;
            num_size = data.indexOf(":", index);
            dx = data.substring(index,num_size).toInt();
            data.remove(0,num_size+1);
            dy = data.toInt();

            if (dx > 0){
                while (dx > jump)
                {
                    dx -= jump;
                    Mouse.move(jump,0);
                }
                Mouse.move(dx,0);
            }
            else if (dx < 0){
                while (dx < -jump)
                {
                    dx += jump;
                    Mouse.move(-jump,0);
                }
                Mouse.move(dx,0);
            }
            if (dy > 0){
                while (dy > jump)
                {
                    dy -= jump;
                    Mouse.move(0,jump);
                }
                Mouse.move(0,dy);
            }
            else if (dy < 0){
                while (dy < -jump)
                {
                    dy += jump;
                    Mouse.move(0,-jump);
                }
                Mouse.move(0,dy);
            }
        }



    }
    Usb.Task();
}