#include <Adafruit_GFX.h>
#include <MCUFRIEND_kbv.h> 
#include <TouchScreen.h>

#define BLACK       0x0000
#define BLUE        0x001F
#define CYAN        0x07FF
#define DARKGREEN   0x03E0
#define DARKCYAN    0x03EF
#define DARKGREY    0x7BEF
#define GREEN       0x07E0
#define GREENYELLOW 0xB7E0
#define LIGHTGREY   0xC618
#define MAGENTA     0xF81F
#define MAROON      0x7800
#define NAVY        0x000F
#define OLIVE       0x7BE0
#define ORANGE      0xFDA0
#define PINK        0xFC9F
#define PURPLE      0x780F
#define RED         0xF800
#define WHITE       0xFFFF
#define YELLOW      0xFFE0
#define LIGHTBLUE       0x02D2
#define LIGHTYELLOW     0xFEAD

#define MINPRESSURE 200
#define MAXPRESSURE 1000

MCUFRIEND_kbv tft;

const int XP = 6;
const int XM = A2; 
const int YP = A1; 
const int YM = 7; 
const int TS_LEFT = 170, TS_RT = 940, TS_TOP = 923, TS_BOT = 181;
TouchScreen ts = TouchScreen(XP, YP, XM, YM, 300);
int mainscreen =1, manualscreen=0, runscreen=0, mappingscreen=0, dummyscreen=0, mapp=0;
int pixel_x, pixel_y;    
bool down = false;
Adafruit_GFX_Button runsystem, stopsystem, startmapping, manual, stop, insert, add, removepoint, back_btn, start, cancel, dummy, startmap, maju, mundur, kanan, kiri, d_kanan_a, d_kiri_a, d_kanan_b, d_kiri_b, cw, ccw, addk, removek;

String donemap="";
String koor[4]={"","","",""};
int koorcounter=0;
bool maxkoor=false;

bool Touch_getXY()
{
    TSPoint p = ts.getPoint();
    pinMode(YP, OUTPUT);      
    pinMode(XM, OUTPUT);
    digitalWrite(YP, HIGH);  
    digitalWrite(XM, HIGH);
    bool pressed = (p.z > MINPRESSURE && p.z < MAXPRESSURE);
    if (pressed) {
        pixel_x = map(p.y, TS_LEFT, TS_RT, 0, tft.width());
        pixel_y = map(p.x, TS_TOP, TS_BOT, 0, tft.height());
    }
    return pressed;
}

void border(){
  tft.drawLine(0, 0, 480, 0, RED);
  tft.drawLine(0, 0, 0, 320, RED);
  tft.drawLine(479, 0, 479, 319, RED);
  tft.drawLine(0, 319, 479, 319, RED);
}

void bordertest(){
  tft.drawLine(0, 0, 480, 0, RED);
  tft.drawLine(0, 0, 0, 320, RED);
  tft.drawLine(479, 0, 479, 319, RED);
  tft.drawLine(0, 319, 479, 319, RED);
  tft.drawLine(0, 30, 480, 30, MAGENTA);
  tft.drawLine(340, 30, 340, 318, MAGENTA);
}

void borderrun(){
  tft.drawLine(0, 0, 480, 0, RED);
  tft.drawLine(0, 0, 0, 320, RED);
  tft.drawLine(479, 0, 479, 319, RED);
  tft.drawLine(0, 319, 479, 319, RED);
  tft.drawLine(0, 30, 480, 30, RED);
  //tft.drawLine(170, 30, 170, 318, RED);
  tft.drawLine(340, 30, 340, 318, RED);
}

void setup()
{
    Serial.begin(9600);
    uint16_t ID = tft.readID();
    if (ID == 0x0000) ID = 0x9329;  
    if (ID == 0xD3D3) ID = 0x9486; 
    tft.begin(ID);

    tft.setRotation(3);            // LANDSCAPE
    tft.fillScreen(BLACK);
    tft.setTextSize(2);
    tft.setCursor(200, 150);
    tft.setTextColor(GREEN,BLACK);
    tft.print("WELCOME");
    delay(1000);
    tft.fillScreen(BLACK);

    runsystem.initButton(&tft, 125, 100, 200, 50, WHITE, GREEN, BLACK, "RUN", 2);
    runsystem.drawButton(false);
    stopsystem.initButton(&tft, 350, 100, 200, 50, WHITE, RED, BLACK, "STOP", 2);
    stopsystem.drawButton(false);
    startmapping.initButton(&tft, 125, 250, 200, 50, WHITE, MAGENTA, BLACK, "MAPPING", 2);
    startmapping.drawButton(false);
    manual.initButton(&tft, 350, 250, 200, 50, WHITE, PINK, BLACK, "MANUAL", 2);
    manual.drawButton(false);
}

void loop()
{
  down = Touch_getXY();
  runsystem.press(down && runsystem.contains(pixel_x, pixel_y));
  stopsystem.press(down && stopsystem.contains(pixel_x, pixel_y));
  startmapping.press(down && startmapping.contains(pixel_x, pixel_y));
  back_btn.press(down && back_btn.contains(pixel_x, pixel_y));
  manual.press(down && manual.contains(pixel_x, pixel_y));
  maju.press(down && maju.contains(pixel_x, pixel_y));
  mundur.press(down && mundur.contains(pixel_x, pixel_y));
  kiri.press(down && kiri.contains(pixel_x, pixel_y));
  kanan.press(down && kanan.contains(pixel_x, pixel_y));
  d_kanan_a.press(down && d_kanan_a.contains(pixel_x, pixel_y));
  d_kiri_a.press(down && d_kiri_a.contains(pixel_x, pixel_y));
  d_kanan_b.press(down && d_kanan_b.contains(pixel_x, pixel_y));
  d_kiri_b.press(down && d_kiri_b.contains(pixel_x, pixel_y));
  cw.press(down && cw.contains(pixel_x, pixel_y));
  ccw.press(down && ccw.contains(pixel_x, pixel_y));
  start.press(down && start.contains(pixel_x, pixel_y));
  cancel.press(down && cancel.contains(pixel_x, pixel_y));
  //add.press(down && add.contains(pixel_x, pixel_y));
  //removepoint.press(down&& removepoint.contains(pixel_x, pixel_y));
  startmap.press(down && startmap.contains(pixel_x, pixel_y));
  addk.press(down && addk.contains(pixel_x, pixel_y));
  //removek.press(down && removek.contains(pixel_x, pixel_y));

  if (mainscreen == 1){
    border();
    tft.setTextSize(2);
    tft.setCursor(180, 8);
    tft.setTextColor(GREEN,BLACK);
    tft.print("MAIN MENU");

    if (runsystem.justPressed()){
      runsystem.drawButton(true);
      mainscreen = 0;
      runscreen = 1;
      tft.fillScreen(BLACK);
      tft.setTextSize(2);
      tft.setCursor(150, 75);
      tft.setTextColor(GREEN,BLACK);
      tft.print(koor[0]);
      tft.setTextSize(2);
      tft.setCursor(150, 100);
      tft.setTextColor(GREEN,BLACK);
      tft.print(koor[1]);
      tft.setTextSize(2);
      tft.setCursor(150, 125);
      tft.setTextColor(GREEN,BLACK);
      tft.print(koor[2]);
      tft.setTextSize(2);
      tft.setCursor(150, 150);
      tft.setTextColor(GREEN,BLACK);
      tft.print(koor[3]);
      start.initButton(&tft,  400, 200, 80, 40, WHITE, CYAN, MAGENTA, "START", 2);
      cancel.initButton(&tft, 400, 250, 80, 40, WHITE, CYAN, MAGENTA, "CANCEL", 2);
      //add.initButton(&tft,  400, 100, 70, 40, WHITE, CYAN, MAGENTA, "ADD", 2);
      //removepoint.initButton(&tft, 400, 150, 70, 40, WHITE, CYAN, MAGENTA, "REMOVE", 2);
      start.drawButton(false);
      cancel.drawButton(false);
      //add.drawButton(false);
      //removepoint.drawButton(false);
    }

    if (stopsystem.justPressed()){
      stopsystem.drawButton(true);
      Serial.println("stop");
      stopsystem.press(false);
      delay(300);
      stopsystem.drawButton(false);
    }

    if (startmapping.justPressed()){
      startmapping.drawButton(true);
      mainscreen = 0;
      mappingscreen= 1;
      tft.fillScreen(BLACK);
      startmap.initButton(&tft,  400, 200, 70, 40, WHITE, CYAN, MAGENTA, "START", 2);
      cancel.initButton(&tft, 400, 250, 70, 40, WHITE, CYAN, MAGENTA, "CANCEL", 2);
      startmap.drawButton(false);
      cancel.drawButton(false);
      delay(300);
    }

    if (manual.justPressed()){
      manual.drawButton(true);
      mainscreen = 0;
      manualscreen = 1;
      tft.fillScreen(BLACK);
      maju.initButton(&tft,  170, 100, 90, 40, WHITE, CYAN, MAGENTA, "MAJU", 2);
      mundur.initButton(&tft, 170, 200, 90, 40, WHITE, CYAN, MAGENTA, "MUNDUR", 2);
      kiri.initButton(&tft,  60, 150, 90, 40, WHITE, CYAN, MAGENTA, "KIRI", 2);
      kanan.initButton(&tft, 280, 150, 90, 40, WHITE, CYAN, MAGENTA, "KANAN", 2);
      d_kanan_a.initButton(&tft,  280, 100, 90, 40, WHITE, CYAN, MAGENTA, "D.KANAN", 2);
      d_kiri_a.initButton(&tft, 60, 100, 90, 40, WHITE, CYAN, MAGENTA, "D.KIRI", 2);
      d_kanan_b.initButton(&tft,  60, 200, 90, 40, WHITE, CYAN, MAGENTA, "B.KANAN", 2);
      d_kiri_b.initButton(&tft, 280, 200, 90, 40, WHITE, CYAN, MAGENTA, "B.KIRI", 2);
      cw.initButton(&tft,  60, 250, 90, 40, WHITE, CYAN, MAGENTA, "CW", 2);
      ccw.initButton(&tft, 280, 250, 90, 40, WHITE, CYAN, MAGENTA, "CCW", 2);
      back_btn.initButton(&tft, 450, 44, 40, 20, WHITE, MAGENTA, WHITE, "BACK", 1.5);
      addk.initButton(&tft, 410, 130, 100, 40, WHITE, CYAN, MAGENTA, "INSERT", 2);
      maju.drawButton(false);
      mundur.drawButton(false);
      kiri.drawButton(false);
      kanan.drawButton(false);
      d_kanan_a.drawButton(false);
      d_kiri_a.drawButton(false);
      d_kanan_b.drawButton(false);
      d_kiri_b.drawButton(false);
      cw.drawButton(false);
      ccw.drawButton(false);
      back_btn.drawButton(false);
      addk.drawButton(false);
      delay(100);
    }
  }

  if (manualscreen == 1){
    bordertest();
    tft.setTextSize(2);
    tft.setCursor(200, 8);
    tft.setTextColor(GREEN,BLACK);
    tft.print("MANUAL");
    if (maju.justPressed()){
      maju.drawButton(true);
      Serial.println("maju");
      maju.press(false);
      delay(300);
      maju.drawButton(false);
    }

    if (mundur.justPressed()){
      mundur.drawButton(true);
      Serial.println("mundur");
      mundur.press(false);
      delay(300);
      mundur.drawButton(false);
    }

    if (kiri.justPressed()){
      kiri.drawButton(true);
      Serial.println("kiri");
      kiri.press(false);
      delay(300);
      kiri.drawButton(false);
    }

    if (kanan.justPressed()){
      kanan.drawButton(true);
      Serial.println("kanan");
      kanan.press(false);
      delay(300);
      kanan.drawButton(false);
    }

    if (d_kanan_a.justPressed()){
      d_kanan_a.drawButton(true);
      Serial.println("d_kanan_fr");
      d_kanan_a.press(false);
      delay(300);
      d_kanan_a.drawButton(false);
    }

    if (d_kiri_a.justPressed()){
      d_kiri_a.drawButton(true);
      Serial.println("d_kiri_fr");
      d_kiri_a.press(false);
      delay(300);
      d_kiri_a.drawButton(false);
    }

    if (d_kanan_b.justPressed()){
      d_kanan_b.drawButton(true);
      Serial.println("d_kanan_bw");
      d_kanan_b.press(false);
      delay(300);
      d_kanan_b.drawButton(false);
    }

    if (d_kiri_b.justPressed()){
      d_kiri_b.drawButton(true);
      Serial.println("d_kiri_bw");
      d_kiri_b.press(false);
      delay(300);
      d_kiri_b.drawButton(false);
    }

    if (cw.justPressed()){
      cw.drawButton(true);
      Serial.println("cw");
      cw.press(false);
      delay(300);
      cw.drawButton(false);
    }

    if (ccw.justPressed()){
      ccw.drawButton(true);
      Serial.println("ccw");
      ccw.press(false);
      delay(300);
      ccw.drawButton(false);
    }

    if (addk.justPressed()){
      addk.drawButton(true);
      addk.press(false);
      String temp_koor;
      if(Serial.available() > 0){
        temp_koor = Serial.readStringUntil('\n');
      }
      for (int i=0; i<=koorcounter; i++){
        if (i==koorcounter && temp_koor!=koor[i]){
          if(maxkoor==true){

            break;
          }
          else{
            koor[koorcounter] = temp_koor;
            koorcounter++;
            if(koorcounter>3){
              maxkoor = true;
              koorcounter=3;
            }
            break;
          }
        }
      }
    }

    if (back_btn.justPressed()){
      back_btn.drawButton(true);
      back_btn.press(false);
      tft.fillScreen(BLACK);
      mainscreen=1;
      manualscreen=0;
      runsystem.initButton(&tft, 125, 100, 200, 50, WHITE, GREEN, BLACK, "RUN", 2);
      runsystem.drawButton(false);
      stopsystem.initButton(&tft, 350, 100, 200, 50, WHITE, RED, BLACK, "STOP", 2);
      stopsystem.drawButton(false);
      startmapping.initButton(&tft, 125, 250, 200, 50, WHITE, MAGENTA, BLACK, "MAPPING", 2);
      startmapping.drawButton(false);
      manual.initButton(&tft, 350, 250, 200, 50, WHITE, PINK, BLACK, "MANUAL", 2);
      manual.drawButton(false);
      delay(300);
    }
  }

  if (runscreen == 1){
    borderrun();
    if (start.justPressed()){
      start.drawButton(true);
      tft.fillScreen(BLACK);
      Serial.println(koor[0]);
      delay(300);
      Serial.println(koor[1]);
      delay(300);
      Serial.println(koor[2]);
      delay(300);
      Serial.println(koor[3]);
      delay(300);
      dummyscreen=1;
      runscreen=0;
      dummy.initButton(&tft, 125, 100, 200, 50, WHITE, GREEN, BLACK, "RUN", 2);
      dummy.drawButton(false);
      stopsystem.initButton(&tft, 350, 100, 200, 50, WHITE, RED, BLACK, "STOP", 2);
      stopsystem.drawButton(false);
      dummy.initButton(&tft, 125, 250, 200, 50, WHITE, MAGENTA, BLACK, "MAPPING", 2);
      dummy.drawButton(false);
      dummy.initButton(&tft, 350, 250, 200, 50, WHITE, PINK, BLACK, "MANUAL", 2);
      dummy.drawButton(false);
      delay(300);
    }

    if (cancel.justPressed()){
      cancel.drawButton(true);
      Serial.println("cancel");
      tft.fillScreen(BLACK);
      mainscreen=1;
      runscreen=0;
      runsystem.initButton(&tft, 125, 100, 200, 50, WHITE, GREEN, BLACK, "RUN", 2);
      runsystem.drawButton(false);
      stopsystem.initButton(&tft, 350, 100, 200, 50, WHITE, RED, BLACK, "STOP", 2);
      stopsystem.drawButton(false);
      startmapping.initButton(&tft, 125, 250, 200, 50, WHITE, MAGENTA, BLACK, "MAPPING", 2);
      startmapping.drawButton(false);
      manual.initButton(&tft, 350, 250, 200, 50, WHITE, PINK, BLACK, "MANUAL", 2);
      manual.drawButton(false);
      delay(300);
    }
  }

  if (mapp== 1){
    tft.setTextSize(2);
    tft.setCursor(100, 150);
    tft.setTextColor(GREEN,BLACK);
    tft.print("Mapping in progress");
    if (Serial.available() > 0){
      donemap = Serial.readStringUntil('\n');
      if(donemap == "donemapping"){
        tft.setTextSize(2);
        tft.setCursor(100, 150);
        tft.setTextColor(BLACK,BLACK);
        tft.print("Mapping in progress");
        tft.setTextSize(2);
        tft.setCursor(100, 150);
        tft.setTextColor(GREEN,BLACK);
        tft.print("Mapping is complete");
        delay(2000);
        tft.fillScreen(BLACK);
        mainscreen=1;
        mapp=0;
        runsystem.initButton(&tft, 125, 100, 200, 50, WHITE, GREEN, BLACK, "RUN", 2);
        runsystem.drawButton(false);
        stopsystem.initButton(&tft, 350, 100, 200, 50, WHITE, RED, BLACK, "STOP", 2);
        stopsystem.drawButton(false);
        startmapping.initButton(&tft, 125, 250, 200, 50, WHITE, MAGENTA, BLACK, "MAPPING", 2);
        startmapping.drawButton(false);
        manual.initButton(&tft, 350, 250, 200, 50, WHITE, PINK, BLACK, "MANUAL", 2);
        manual.drawButton(false);
        delay(300);
      }
    }
  }

  if (dummyscreen == 1){
    border();
    if (dummy.justPressed()){
      dummy.drawButton(true);
      dummy.press(false);
      delay(300);
      dummy.drawButton(false);
    }

    if (stopsystem.justPressed()){
      stopsystem.drawButton(true);
      Serial.println("stop");
      tft.fillScreen(BLACK);
      mainscreen=1;
      dummyscreen=0;
      runsystem.initButton(&tft, 125, 100, 200, 50, WHITE, GREEN, BLACK, "RUN", 2);
      runsystem.drawButton(false);
      stopsystem.initButton(&tft, 350, 100, 200, 50, WHITE, RED, BLACK, "STOP", 2);
      stopsystem.drawButton(false);
      startmapping.initButton(&tft, 125, 250, 200, 50, WHITE, MAGENTA, BLACK, "MAPPING", 2);
      startmapping.drawButton(false);
      manual.initButton(&tft, 350, 250, 200, 50, WHITE, PINK, BLACK, "MANUAL", 2);
      manual.drawButton(false);
      delay(300);
    } 
  }

  if (mappingscreen == 1){
    border();
    if (startmap.justPressed()){
      startmap.drawButton(true);
      Serial.println("startmap");
      startmap.press(false);
      delay(300);
      startmap.drawButton(false);
      tft.fillScreen(BLACK);
      mappingscreen = 0;
      mapp = 1;
      }
    

    if (cancel.justPressed()){
      cancel.drawButton(true);
      tft.fillScreen(BLACK);
      mainscreen=1;
      mappingscreen=0;
      runsystem.initButton(&tft, 125, 100, 200, 50, WHITE, GREEN, BLACK, "RUN", 2);
      runsystem.drawButton(false);
      stopsystem.initButton(&tft, 350, 100, 200, 50, WHITE, RED, BLACK, "STOP", 2);
      stopsystem.drawButton(false);
      startmapping.initButton(&tft, 125, 250, 200, 50, WHITE, MAGENTA, BLACK, "MAPPING", 2);
      startmapping.drawButton(false);
      manual.initButton(&tft, 350, 250, 200, 50, WHITE, PINK, BLACK, "MANUAL", 2);
      manual.drawButton(false);
      delay(300);
    }
  }
}
