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

Map the rooms structure into the image frame and hit Enter to begin processing the video frames





##### The code is now fully up and running
