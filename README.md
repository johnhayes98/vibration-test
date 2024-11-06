This was generated for a project for ISEN 635 at Texas A&M. The goal of the project was to use information theory to evaluate the effectiveness of different vibrotactile notifications on iPhone and Android devices.

Python GUI:
- Takes subject info
- Initializes study with specified parameters
- Communicates with arduino Nano over serial USB to send vibration patterns
- Prompts user to select which type of notifications

Arduino Nano:
- Receives serial input from Python GUI
- Turns on and off vibration motor as commanded by serial data