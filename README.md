# Electra - Automation System for Electricity Management

Electra is an arduino based automation system that develops a framework for interconnecting the electronic appliances in a room, that can detect the presence of an individual in the functional range of a device using a computer vision algorithm and accordingly switch it on and off. This in turn helps in saving a huge proportion of electricity consumption, and takes away the hassle of switching the devices on and off, from the user.


### Installation of required packages

The implentation of the program requires the installation of the darkflow-yolov2 tool 

This,can be done following the instructions in the youtube video
https://youtu.be/PyjBd7IDYZs
or clone the following repository
https://github.com/thtrieu/darkflow

Now,move to Darkflow-master folder then

```
git clone https://github.com/RishinathhKS/Electra

cd Electra

pip install -r requirements.txt

cd ..
```

After successfully installing all of the above requirements

### Running the code

Open a terminal in this folder (darkflow) 

and now run the code

```
python maincode.py
```

Now that the code is running

#### Set up screen

There are two options to choose from
1)Setup
2)Run existing setup


Enter the path to the camera feed, here we are using a surveillance camera video using the Real Time Streaming Protocol (RTSP).


Map the room's structure into the image frame and hit Enter to begin processing the video frames


##### The code is now fully up and running.


### Hardware Implementation

The system is set up to serially communicate with an Arduino microcontroller. It does this by saving the output of the program into a file that can be read by an application called **Processing IDE** that sends the data over to the Arduino serial port. 

Set up the Arduino board wiring by taking the positive terminal of every appliance from the switch board in the room and connecting it to the correspoding Digital IO (PWM) pins. Make sure the devices are connected to its respective ports, according to the indexing done in the room mapping. The negative terminals can be connected to the Ground pin in Arduino. A relay module can be used as an intermediary agent to prevent damage of the microcontroller due to the high power output from AC mains. 

The wiring is now completed. Flash the arduino program and run the Processing IDE code to start transmitting serial data.

##### The electrical appliances will now behave according to the realtime output of the camera.
