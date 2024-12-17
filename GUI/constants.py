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
SQUARE = "GUI/assets/square.png"
CIRCLE = "GUI/assets/circle.png"
TRIANGLE = "GUI/assets/triangle.png"
CIRCLE_PATTERN = "GUI/assets/circlePattern.png"
HEXAGON = "GUI/assets/hexagon.png"
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

# All text in SV and EN
translation = {
    "en": {
        "create_pattern": "Create Patterns",
        "create_your_pattern": "Create a Pattern",
        "premade_patterns": "Premade Patterns",
        "control": "Take Control",
        "back": "Back",
        "undo": "Undo",
        "welcome": "Welcome \nto try my work!\n",
        "instructions": "Here you can try balancing the ball yourself. \nUse the joystick in the bottom right corner to take control \n\nGood luck!",
        "text_info": [
            {
                "heading": "Hello! ", 
                "subheading": "\nI am the balance master Axis. I am a robot specialized in balancing balls. Even though you and I don’t look very similar, there are many similarities between a robot and a human.\n\nPress the arrow, and I will tell you more!",
                "body": "",
                "lightButtonText": ""
            },
            {
                "heading": "My Eyes",
                "subheading": "\nI have eyes like you! But my eyes are a bit different, they are a camera. With the help of the camera, I can accurately see where the ball is located on the plate.",
                "body": "\nThe camera takes pictures of the plate at a high speed, 90 images per second. You experience this as a video, while each image can be processed individually by, for example, a computer. By using a computer to process the images, I can locate the ball and quickly display the images in the box you see. What you see in the box is exactly what I see when balancing the ball. There I have found the ball and marked it with a green circle."
            },
            {
                "heading": "My Arms",
                "subheading": "\nI also have muscles and arms. Unlike you my arms are made of plastic and my muscles are electric motors. I use these to move the plate.",  
                "body": "\nMy arms are made of plastic and printed by a 3D printer. They are attached to electric motors. The motors used are stepper motors. These motors have a fixed number of steps per revolution. By keeping track of how many steps I have taken. I can also determine the direction in which the arms are pointing. With this information I can also decide how the plate should tilt and thereby roll the ball."
            },
            {
                "heading": "My Brain",
                "subheading": "\nI also have a brain just like you. Unlike you my brain is a small computer. Using mathematics and information about the ball's position I can calculate how the motors should tilt the plate to avoid losing the ball.",  
                "body": "\nIn my computer image processing is performed to determine the ball's position. The ball's position is then compared to a target position located at the center of the plate. If the difference is large I need to tilt the plate significantly and if the difference is small I can tilt the plate less to roll the ball toward the target position. To determine how the plate tilts I use mathematical formulas that convert a specific tilt of the plate into a certain number of steps for my motors. This in turn moves the ball toward the target position. When the ball moves the camera detects a new ball position and the entire process repeats. That's how I maintain balance!"
            }
        ]
    },
    "sv": {
        "create_pattern": "Skapa mönster",
        "create_your_pattern": "Skapa ett mönster",
        "premade_patterns": "Färdiga mönster",
        "control": "Balansera Själv",
        "back": "Bakåt",
        "undo": "Ångra",
        "welcome": "Välkommen\n att testa mitt jobb!\n ",
        "instructions": "Här kan du testa att balansera bollen själv. \nAnvänd joysticken nere i högra hörnet och kontrollen blir din \n\nLycka till!",
        "text_info": [
            {
                "heading": "Hej! ", 
                "subheading": "\nJag är balansmästaren Axis. Jag är en robot specialiserad på att balansera bollar. Även om du och jag inte ser så lika ut så finns många likheter mellan en robot och en människa. \n\nTryck på pilen så berättar jag mer!",
                "body": "",
                "lightButtonText": ""
            },
            {
                "heading": "Mina ögon",
                "subheading": "\nJag har ögon likt dig! Men mina ögon är lite annorlunda, de är en kamera. Med hjälp av kameran kan jag noggrant se var bollen befinner sig på plattan.",
                "body": "\nKameran tar kort på plattan i snabb hastighet, 90 bilder i sekunden. Detta upplever du som en video samtidigt som varje bild kan behandlas separat av till exempel en dator. Genom att använda en dator för att behandla bilderna kan jag hitta bollen och spela upp bilderna snabbt i den ruta du ser. Det du ser i rutan är alltså samma sak som jag ser när jag balanserar bollen. Där har jag hittat bollen och markerat den i en grön cirkel. "
            },
            {
                "heading": "Mina armar",
                "subheading": "\nJag har även muskler och armar. Men till skillnad från dig är mina armar gjorda i plast och mina muskler är elektriska motorer. Dessa använder jag till att flytta plattan. ",  
                "body": "\nMina armar är utskrivna i plast av en 3d-skrivare. Dessa är fästa i elektriska motorer. De motorer som används är stegmotorer. Dessa motorer har ett bestämt antal steg per rotationsvarv Genom att hålla koll på hur många steg jag tagit kan jag även veta i vilken riktning armarna pekar. Med denna information kan jag även bestämma hur plattan ska luta och därmed rulla bollen. "
            },
            {
                "heading": "Min Hjärna",
                "subheading": "\nJag har också en hjärna precis som du. Men till skillnad från dig är min hjärna en liten dator.  Med hjälp av matematik och information om bollens position kan jag beräkna hur motorerna ska luta plattan för att inte tappa bollen.",  
                "body": "\nI min dator sker den bildbehandling som hittar bollens position. Bollens position jämförs sedan med en målposition som befinner sig mitt på plattan, om skillnaden är stor måste jag luta plattan mycket och om skillnaden är liten kan jag luta plattan mindre för att rulla bollen mot målpositionen.  För att veta hur plattan lutar använder jag matematiska formler som omvandlar en bestämd lutning på plattan till ett bestämt antal steg som mina motorer tar. Detta gör i sin tur att bollen flyttas mot målpositionen.  När bollen flyttas hittar kameran en ny bollposition och hela processen upprepas. Det är så jag håller balansen! "
            }
        ]
    }
}
