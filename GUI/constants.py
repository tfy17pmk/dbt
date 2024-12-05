#Colors
background_color = "#00263E" #dark blue
text_color = "#B9D9EB" #light blue, almost white

#Fonts
heading = ("Helvetica Neue", 42, "bold")
sub_heading = ("Helvetica Neue", 32, "bold")
body_text = ("Helvetica Neue", 20)

#Image paths
INFO_IMAGE = "GUI/assets/info.png"
COMPETITION_IMAGE = "GUI/assets/competition.png"
PATTERN_IMAGE = "GUI/assets/pattern.png"
RIGHT_ARROW = "GUI/assets/right_arrow.png"
FIRSTPAGE = "GUI/assets/InfoPageOne.png"
ARM = "GUI/assets/arm.png"
BRAIN = "GUI/assets/brain.png"
LIGHT_BULB = "GUI/assets/light_bulb.png"
SQUARE = "GUI/assets/square.png"
CIRCLE = "GUI/assets/circle.png"
TRIANGLE = "GUI/assets/triangle.png"
CIRCLE_PATTERN = "GUI/assets/circlePattern.png"
HEXAGON = "GUI/assets/hexagon.png"
BG = "GUI/assets/bluebg.png"
STAR_PATTERN = "GUI/assets/star.png"
HEART_PATTERN = "GUI/assets/heart.png"
JOYSTICK = "GUI/assets/joystick.png"
EN = "GUI/assets/ENFlag.png"
SV = "GUI/assets/SVFlag.png"

#communication
serial_port = "/dev/tty.usbserial-0199B457"  # Use 'ls /dev/tty.*' to find the correct port AND you cant have serial monitor on in Arduino IDE!
baud_rate = 115200  # Same baud rate as in Arduino IDE


#Flags
show_speaker = False

#information pages text
info_text = [
    {
        "heading": "Hej! \nJag är balansmästaren Axis. Jag är en robot specialiserad på att balansera bollar. Även om du och jag inte ser så lika ut så finns många likheter mellan en robot och en människa. ", 
        "subheading": "\nTryck på pilen så berättar jag mer!",
        "body": "",
        "lightButtonText": ""
    },
    {
        "heading": "Mina ögon",
        "subheading": "\nJag har ögon precis som du. Men istället för ögon har jag en kamera. Kameran använder jag för att se bollens position på plattan.",
        "body": "\nKameran tar kort på plattan i snabb hastighet, 90 bilder i sekunden. Detta upplever du som en video samtidigt som varje bild kan behandlas separat av till exempel en dator. Genom att använda en dator för att behandla bilderna kan jag hitta bollen och spela upp bilderna snabbt i den ruta du ser. Det du ser i rutan är alltså samma sak som jag ser när jag balanserar bollen. Där har jag hittat bollen och markerat den i en grön cirkel. ",
    },
    {
        "heading": "Mina armar",
        "subheading": "\nJag har även muskler och armar, men till skillnad från dig är mina armar gjorda i plast och mina muskler är elektriska motorer. Dessa använder jag till att flytta plattan. ",  
        "body": "\nMina armar är utskrivna i plast av en 3d-skrivare. Dessa är fästa i elektriska motorer. De motorer som används är stegmotorer. Dessa motorer har ett bestämt antal steg per rotationsvarv och genom att hålla koll på hur många steg jag tagit kan jag även veta i vilken riktning armarna pekar. Med denna information kan jag även bestämma hur plattan ska luta och därmed rulla bollen. ",
    },
    {
        "heading": "Min Hjärna",
        "subheading": "\nJag har också en hjärna precis som du. Men till skillnad från dig är min hjärna en liten dator.  Med hjälp av matematik och information om bollens position kan jag därför beräkna hur motorerna ska luta plattan för att inte tappa bollen.",  
        "body": "\nI min dator sker den bildbehandling som hittar bollens position. Bollens position jämförs sedan med en målposition som befinner sig mitt på plattan, om skillnaden är stor måste jag luta plattan mycket och om skillnaden är liten kan jag luta plattan mindre för att rulla bollen mot målpositionen.  För att veta hur plattan lutar använder jag matematiska formler som omvandlar en bestämd lutning på plattan till ett bestämt antal steg som mina motorer tar. Detta gör i sin tur att bollen flyttas mot målpositionen.  När bollen flyttas hittar kameran en ny bollposition och hela processen upprepas. Det är så jag håller balansen! ",
    }
]

# Challenge page text
challenge_text = [
        {"heading": "Utmana mig i att balansera bollen!",
         "body": "Jag rullar bollen till olika ställen på bordet, sedan får du använda spakarna för att ta dig till samma ställen som mig."},
]