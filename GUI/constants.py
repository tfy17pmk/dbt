# Colors
background_color = "#00263E" #dark blue
text_color = "#B9D9EB" #light blue, almost white

# Fonts
heading = ("Helvetica Neue", 42, "bold")
sub_heading = ("Helvetica Neue", 32, "bold")
body_text = ("Helvetica Neue", 20)

# Image paths
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

# Communication
serial_port = "/dev/tty.usbserial-0199B457"  # Use 'ls /dev/tty.*' to find the correct port AND you cant have serial monitor on in Arduino IDE!
baud_rate = 115200  # Same baud rate as in Arduino IDE


# Flags
show_speaker = False

# Information pages text
info_text = [
    {
        "heading": "Hej! \nJag är balansmästaren Axis. Jag är en robot specialiserad på att balansera bollar. Även om du och jag inte ser så lika ut så finns det många likheter mellan en robot och en människa. ", 
        "subheading": "\nTryck på pilen så berättar jag mer!",
        "body": "",
        "lightButtonText": ""
    },
    {
        "heading": "Mina ögon",
        "subheading": "\nJag har ögon precis som du. Till skillnad från dig är mina ögon en kamera. Kameran använder jag för att se var bollen är på plattan.",
        "body": "\nKameran tar flera kort på plattan i följd, hela 90 bilder i sekunden. Detta upplever du som en video. Samtidigt kan varje bild behandlas separat av till exempel en dator. Genom att behandla bilderna kan jag hitta var bollen är i varje bild, och markera den platsen med en grön cirkel. Sedan kan jag spela upp bilderna i snabbt följd, som en video. Det du ser i den lilla rutan är samma sak som jag ser när jag balanserar bollen.",
    },
    {
        "heading": "Mina armar",
        "subheading": "\nJag har även muskler och armar. Till skillnad från dig är mina armar gjorda i plast och mina muskler är elektriska motorer. Dessa använder jag till att röra på plattan. ",  
        "body": "\nMina armar är utskrivna i plast av en 3d-skrivare. Armarna är fästa i elektriska stegmotorer. Denna typ av motorer tar ett bestämt antal steg per varv de roterar. Genom att hålla koll på hur många steg mina motorer tar vet jag därför i vilken riktning mina armar pekar. Med denna information kan jag kontrollera hur plattan ska luta och därmed rulla bollen. ",
    },
    {
        "heading": "Min Hjärna",
        "subheading": "\nJag har också en hjärna. Till skillnad från dig är min hjärna en liten dator.  Med hjälp av matematik och kunskap om bollens position kan datorn beräkna hur mina motorerna ska luta plattan för att inte tappa bollen.",  
        "body": "\nI min dator sker den bildbehandling som hittar var bollen befinner sig. Bollens position jämförs med en målposition i mitten av plattan. Avståndet mellan dem bestämmer hur mycket jag måste luta plattan för att nå målet. Ifall skillnaden är stor måste jag luta plattan mycket och tvärt om ifall skillnaden är liten. För att veta hur många steg motorerna ska ta för att luta plattan korrekt använder jag matematiska formler. När bollen flyttas hittar kameran bollens nya position och hela processen upprepas. Det är så jag håller balansen! ",
    }
]