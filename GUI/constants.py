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
                "heading": "Hello! \nI am the balance master Axis. I am a robot specialized in balancing balls. Even though you and I don’t look very similar, there are many similarities between a robot and a human.", 
                "subheading": "\nPress the arrow, and I will tell you more!",
                "body": "",
                "lightButtonText": ""
            },
            {
                "heading": "My Eyes",
                "subheading": "\nI have eyes just like you. Unlike you, my eyes come in the form of a camera. I use the camera to see where the ball is located on the plate.",
                "body": "\nThe camera takes several pictures of the plate one after the other. A full 90 images per second. You experience this as a video. Meanwhile, each image can be processed individually by for example a computer. By processing the images, I can locate the ball in each image and mark its position with a green circle. I then display the images in sequence, like a video. What you see in the box is what I see when balancing the ball."
            },
            {
                "heading": "My Arms",
                "subheading": "\nI also have muscles and arms. Unlike you, my arms are made of plastic and my muscles are electric motors. I use these to move the plate.",  
                "body": "\nMy arms are made of plastic and printed on a 3D printer. They are attached to electric steppermotors. These kinds of motors take a fixed number of steps for every revolution. By keeping track of how many steps my motors have taken, I know the direction in which my arms are pointing. With this information, I can decide how the plate should tilt and thereby roll the ball."
            },
            {
                "heading": "My Brain",
                "subheading": "\nI also have a brain. Unlike you, my brain is a small computer. Using mathematics and knowledge about the ball's position, my computer can calculate how my motors should tilt the plate to avoid dropping the ball.",  
                "body": "\nIn my computer, image processing is performed to determine where the ball is located. The ball's position is compared to a target position, located at the center of the plate. The distance between them determines how much the plate should be tilted to reach the goal. If the difference is large, I need to tilt the plate more, and the opposite if the difference is small. To determine how many steps my motors should take to tilt the plate correctly, I use mathematical formulas. When the ball moves the camera, detects a new ball position, and the entire process repeats. That's how I maintain balance!"
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
                "heading": "Hej! \nJag är balansmästaren Axis. Jag är en robot specialiserad på att balansera bollar. Även om du och jag inte ser så lika ut så finns det många likheter mellan en robot och en människa. ", 
                "subheading": "\nTryck på pilen så berättar jag mer!",
                "body": "",
                "lightButtonText": ""
            },
            {
                "heading": "Mina ögon",
                "subheading": "\nJag har ögon precis som du. Till skillnad från dig är mina ögon en kamera. Kameran använder jag för att se var bollen är på plattan.",
                "body": "\nKameran tar flera kort på plattan i följd. Hela 90 bilder i sekunden. Detta upplever du som en video. Samtidigt kan varje bild behandlas separat av till exempel en dator. Genom att behandla bilderna kan jag hitta var bollen är i varje bild, och markera den platsen med en grön cirkel. Sedan kan jag spela upp bilderna i snabbt följd, som en video. Det du ser i rutan är samma sak som jag ser när jag balanserar bollen."
            },
            {
                "heading": "Mina armar",
                "subheading": "\nJag har även muskler och armar. Till skillnad från dig är mina armar gjorda i plast och mina muskler är elektriska motorer. Dessa använder jag till att röra på plattan. ",  
                "body": "\nMina armar är utskrivna i plast av en 3d-skrivare. Armarna är fästa i elektriska stegmotorer. Denna typ av motorer tar ett bestämt antal steg per varv de roterar. Genom att hålla koll på hur många steg mina motorer tar vet jag därför i vilken riktning mina armar pekar. Med denna information kan jag kontrollera hur plattan ska luta och därmed rulla bollen. "
            },
            {
                "heading": "Min Hjärna",
                "subheading": "\nJag har också en hjärna. Till skillnad från dig är min hjärna en liten dator.  Med hjälp av matematik och kunskap om bollens position kan min dator beräkna hur mina motorerna ska luta plattan för att inte tappa bollen.",  
                "body": "\nI min dator sker den bildbehandling som hittar var bollen befinner sig. Bollens position jämförs med en målposition i mitten av plattan. Avståndet mellan dem bestämmer hur mycket jag måste luta plattan för att nå målet. Ifall skillnaden är stor måste jag luta plattan mycket och tvärt om ifall skillnaden är liten. För att veta hur många steg motorerna ska ta för att luta plattan korrekt använder jag matematiska formler. När bollen flyttas hittar kameran bollens nya position och hela processen upprepas. Det är så jag håller balansen! "
            }
        ]
    }
}
