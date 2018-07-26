# interactive_nao_prompts
This package runs a simple program that displays images with errors in them and asks the user for how many errors exist. Starting with the first image and continuing every other image, the robot will say a prescripted prompt based on passed in argument to script call. These prescripted prompts are either Positive, Negative, or Neutral. Intended to cause the participant to be unsure in their answer and allow the robot to influence the participants emotions. 

## Getting Started
This program is designed to be run on an Aldebaran NAO robot.

### Prerequisites
This program has been tested on Ubuntu 14.04 using Python 2.7. Please install the following dependencies. Not all commands will need to be run with sudo if run as root, but to avoid possible permission errors, code below run with sudo.

```
 sudo apt-get install python-tk python-pip python-imaging-tk
```

### Installing
Run the following commands to install interactive_nao_prompts.
```
cd ~/Documents
git clone https://github.com/ahpalmerUNR/interactive_nao_prompts.git
cd interactive_nao_prompts
sudo mkdir -p /opt/nao/
sudo tar -xvzf pynaoqi-python2.7-2.1.4.13-linux64.tar.gz -C /opt/nao/
```

open the interact.py file and edit the lines
```
#Connection Info to NAO
ip = "localhost" 
port = 9559
```
and
```
#initiate robot communication
tts = ALProxy("ALTextToSpeech", "192.168.1.138", 9559)
motion = ALProxy("ALRobotPosture", "192.168.1.138", 9559)
animatedTts = ALProxy("ALAnimatedSpeech", "192.168.1.138", 9559)
```
to match your setup.

## Running the code
To run the code you must update the PYTHONPATH to include the pynaoqi-python2.7-2.1.4.13-linux64 folder we made.

If you don't want to perminently alter your PYTHONPATH, just run the following lines to run the program. *note:* Edit the argument Positive to either Negative or Neutral as needed. Without an argument the default is Positive.
```
export PYTHONPATH=${PYTHONPATH}:/opt/nao/pynaoqi-python2.7-2.1.4.13-linux64
cd ~/Documents/interactive_nao_prompts
python interact.py Positive 
```

**Alternatively**,

You could perminently alter your PYTHONPATH using
```
echo "export PYTHONPATH=${PYTHONPATH}:/opt/nao/pynaoqi-python2.7-2.1.4.13-linux64" >> ~/.bashrc
source ~/.bashrc
```

Then to run you only need to do:
```
cd ~/Documents/interactive_nao_prompts
python interact.py Positive 
```

