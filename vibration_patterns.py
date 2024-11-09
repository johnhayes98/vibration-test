'''
This file contains the vibration patterns. Each vibration is formatted as a list of lists. 
Each list contains two values: [duration_in_ms, intensity]. 
Both should be a single byte ranging from 0 to 255.

'''

iPhone = {
    "iMessage": [[255, 255], [50, 0], [255, 255], [0, 0]],
    "Email": [[135,200], [0,0]],
    "WhatsApp": [[100,200], [0,0]],
    "None": [[0,0]]
}

Android = {
    "Text" : [],
    "Email" : [],
    "WhatsApp" : [],
    "SnapChat" : []
}

test = {

}

test2 = {

}