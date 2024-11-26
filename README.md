This was generated for a project for ISEN 635 at Texas A&M. The goal of the project was to use information theory to evaluate the effectiveness of different vibrotactile notifications on iPhone and Android devices.

Python GUI:
- Takes subject info
- Initializes study with specified parameters
- Communicates with arduino Nano over serial USB to send vibration patterns
- Prompts user to select which type of notifications

Arduino Nano:
- Receives serial input from Python GUI
- Turns on and off vibration motor as commanded by serial data

Features:
- Vibration patterns can be set within vibration_patterns.py
    - Each dictionary contains a set of vibrations
    - Each vibration is formatted as a list of lists. 
    - Each list contains two values: [duration_in_ms, intensity]. 
    - Both should be a single byte ranging from 0 to 255.
- gui.py imports all dictionaries in vibration_patterns.py
    - Vibrations can be manually triggered within "Vibration Demo" menu
    - Vibrations can be plotted using "Plot Vibration Patterns" button within "Vibration Demo" menu
- Set number of trials and directory for results file in Settings Menu


Hardware:
- Arduino Nano
- 5v Vibration Motor Module (https://www.amazon.com/dp/B091TV6RTT?ref=ppx_yo2ov_dt_b_fed_asin_title)

Hardware Connections:

- Arduino Nano USB > Computer USB port
- Arduino Nano 5v > Vibration Motor Module VCC
- Arduino Nano GND > Vibration Motor Module GND
- Arduino Nano I/O Digital Pin 3 > Vibration Motor Module IN