'''
This file contains the vibration patterns. Each vibration is formatted as a list of lists. 
Each list contains two values: [duration_in_ms, intensity]. 
Both should be a single byte ranging from 0 to 255.

For 5v applied to motor, pwm of 100 seems to be barely detectable. Use range 100-255

'''

# iPhone = {
#     "iMessage": [[255, 255], [75, 0], [150, 225], [100, 200], [0, 0]],
#     "Email": [[255,255], [0,0]],
#     "WhatsApp": [[150,255], [0,0]],
#     "None": [[0,0]]
# }

# Android = {
#     "Text" : [[255,100], [0, 0]],
#     "Email" : [[255,150], [0, 0]],
#     "WhatsApp" : [[255,200], [0, 0]],
#     "SnapChat" : [[255,255], [0, 0]]
# }

PWM_Ranges = {
    "100" : [[255,100],[255,100],[255,100],[255,100], [0, 0]],
    "150" : [[255,150],[255,150],[255,150],[255,150], [0, 0]],
    "200" : [[255,200],[255,200],[255,200],[255,200], [0, 0]],
    "255" : [[255,255],[255,255],[255,255],[255,255], [0, 0]]
}

Final = {
    "Stocatto": [[255, 255], [75, 0], [150, 225], [100, 200], [0, 0]],
    "Accent": [[60,255], [175, 0],[255,255], [100,255], [0,0] ],
    "Heartbeat": [[100,255], [255,0], [100,255],[0,0]],
    "None": [[0,0]]
}

# Gwilym = {
#     "Tick-Tock": [[50, 150], [150, 180], [0,0]],
#     "Zig-Zig-Zig": [[50, 180], [50, 180], [50, 180], [0,0]],
#     "Heartbeat": [[200,150], [100,0], [200,150], [100,0], [200,150], [0,0]],
#     "Basic": [[300, 100], [0,0]],
#     "Waltz": [[150, 130], [100, 180], [150, 130], [0,0]],
#     "Short": [[100,120], [0,0]],
#     "Medium": [[200,150], [0,0]] 
# }