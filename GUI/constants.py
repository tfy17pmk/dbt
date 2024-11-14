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
EYES = "GUI/assets/eyes.png"
ARM = "GUI/assets/arm.png"
BRAIN = "GUI/assets/brain.png"
LIGHT_BULB = "GUI/assets/light_bulb.png"
SQUARE = "GUI/assets/square.png"
CIRCLE = "GUI/assets/circle.png"
TRIANGLE = "GUI/assets/triangle.png"
STAR = "GUI/assets/star.png"

#communication
serial_port = "/dev/tty.usbserial-0199B457"  # Use 'ls /dev/tty.*' to find the correct port AND you cant have serial monitor on in Arduino IDE!
baud_rate = 115200  # Same baud rate as in Arduino IDE


#Flags
show_speaker = False

#information pages text
info_text = [
    {
        "heading": "Hej! \nJag är Balansroboten. \nÄven fast jag är en robot så är du och jag ganska lika.", 
        "subheading": "\n\n\n\n\n\n\n\n\n\nTryck på pilen så berättar jag mer!",
        "body": "",
        "lightButtonText": ""
    },
    {
        "heading": "Mina Ögon",
        "subheading": "Jag har ögon precis som du. Men istället för ögon har jag en kamera. \nKameran använder jag för att se bollen.",
        "body": "\nKameran filmar balansplattan med 90 bilder i sekunder. Med hjälp av bilderna kan en datoralgoritm identifiera bollen från dess form och färg. Algoritmen räknar sedan ut bollens position på balansplattan. Du kan se vad kameran ser i rutan till vänster.",
        "lightButtonText": " \n\n\n\n\n\n\n\nTryck på knappen för att se vart mina ögon sitter!"
    },
    {
        "heading": "Mina muskler",
        "subheading": "Jag har även muskler för att kunna röra på plattan.",  
        "body": "\nTill skillnad från dig är mina muskler elektriska motorer. Mina motorer får mina armar att röra sig så att plattan lutar, vilket får bollen att rulla. Motorerna är stegmotorer som rör armarna genom att ta ett bestämt antal steg vilket an översättas till en vinkel. När armarna rör sig rör sig även balansplattan, vilket får plattan att luta så att bollen rör på sig. Genom att ta rätt antal steg kan balansplattan vinklas så att bollen rullar åt det håll man vill.",
        "lightButtonText": "\n\n\n\n\n\n\n\n\n\nTryck på knappen för att se vart mina muskler sitter!"
    },
    {
        "heading": "Min Hjärna",
        "subheading": "Jag har också en hjärna. Men till skillnad från dig är min hjärna en liten dator.",  
        "body": "\nMin datorn är det som styr resten av min kropp och ser till att motorerna vinklar plattan så att bollen rullar rätt. På datorn finns den datoralgoritm som kollar på bilderna från kameran och hittar bollens position. Positionen används för att beräkna hur balansplattan ska luta med hjälp av trigonometriska formler. Datorn listar sedan ut hur många steg motorerna måste ta för att uppnå den lutningen. Efter att motorerna har rört armarna kontrollerar datorn att bollen rullat rätt med hjälp av en PID-kontroller.",
        "lightButtonText": " \n\n\n\n\n\n\n\nTryck på knappen för att se vart Jag har min hjärna!"
    }
]

# Challenge page text
challenge_text = [
        {"heading": " \n\n  Utmana mig i att balansera bollen! \n\n         Jag rullar bollen till olika \n     ställen på bordet, sedan får du \n     använda spakarna för att ta dig \n         till samma ställen som mig."},
]