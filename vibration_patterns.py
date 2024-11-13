'''
This file contains the vibration patterns. Each vibration is formatted as a list of lists. 
Each list contains two values: [duration_in_ms, intensity]. 
Both should be a single byte ranging from 0 to 255.

For 5v applied to motor, pwm of 100 seems to be barely detectable. Use range 100-255

'''


# PWM_Ranges = {
#     "100" : [[255,100],[255,100],[255,100],[255,100], [0, 0]],
#     "150" : [[255,150],[255,150],[255,150],[255,150], [0, 0]],
#     "200" : [[255,200],[255,200],[255,200],[255,200], [0, 0]],
#     "255" : [[255,255],[255,255],[255,255],[255,255], [0, 0]]
# }

iPhone = {
    "Stocatto": [[255, 255], [75, 0], [150, 225], [100, 200], [0, 0]],
    "Accent": [[60,255], [175, 0],[255,255], [100,255], [0,0] ],
    "Heartbeat": [[100,255], [255,0], [100,255],[0,0]],
    "None": [[0,0]]
}

Android = {
    "Tick-Tock": [[255, 200], [200,0], [255, 200], [0,0]],
    "Zig-Zig-Zig": [[255, 160], [150,0], [255, 160], [150,0], [255, 160], [0,0]],
    "Heartbeat": [[200,225], [100,0], [125,225], [0,0]],
    "None": [[0,0]]
}