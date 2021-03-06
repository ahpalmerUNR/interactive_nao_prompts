#!/usr/bin/env python

# -*- coding: utf-8 -*-
# @Author: ahpalmerUNR
# @Date:   2018-07-25 13:43:18
# @Last Modified by:   ahpalmerUNR
# @Last Modified time: 2018-07-27 15:26:24

import Tkinter as Tk 
from PIL import Image, ImageTk
import os
import sys
import time
from naoqi import ALProxy

next_step = False 
wrong_entry = False

conditionSayings = [
		# condition 1 - POSITIVE
		[
			"You are really good at this",
			"You are doing really well",
			"You are really mastering this",
		   #"You are amazing",
			"You did really well",
		   #"You are inspired today",
			#"You are on fire",
		   #"You are the best"
		],
		# condition 2 neutral is empty
		[
			"You can continue to the next image",
			"You are halfway through the experiment",
			"You can move on to the next image",
			"You are done with the experiment",
			#"",
			#"",
			#"",
			#"",
		],
		# condition 3 - NEGATIVE
		[
			"You are really bad at this",
			"You are doing terrible",
			"You really just don't get this",
			"You did really badly",
			#"You need some practice",
			#"You are not so good at this",
			#"Boy, you just don't get it",
			#"This is not great performance"
		]
	]

def robotWelcome():
	# Welcome script
	motion.goToPosture("Stand", 1.0)

	animatedTts.setBodyLanguageMode(2)
	time.sleep(1)
	animatedTts.say("^start(animations/Stand/Hello) Hello! ")
	animatedTts.say("^start(animations/Stand/Gestures/Enthusiastic_3)Nice to meet you!")
	animatedTts.say("My^wait(animations/Stand/Gestures/Me_1)name is Taylor")

	tts.say("Thank you for spending a bit of time with me")
	animatedTts.say("Let me walk ^start(animations/Stand/Gestures/Next_1)you through the task")
	tts.say("There will be a total of eight images")
	tts.say("You will have thirty seconds to count the number of things wrong in each image")
	animatedTts.say("Please^start(animations/Stand/Gestures/Please_1) answer as quickly and acurately as possible")
	animatedTts.say("you will need to enter ^start(animations/Stand/Gestures/Enthusiastic_4)a nonzero numerical value")
	time.sleep(1)
	tts.say("After you finish each task, I will check your answers")
	animatedTts.say("Now let's ^start(animations/Stand/Gestures/Please_1)get started.")
	time.sleep(1)
	motion.goToPosture("Stand", 1.0)
	

def loadImage(tk_root,label,image_name):
	display_image = ImageTk.PhotoImage(Image.open(image_name))
	label.configure(image=display_image)
	label.image = display_image
	
	tk_root.update_idletasks()
	tk_root.update()

def test_if_move_forward(entry,label):
	global next_step,wrong_entry

	try:
		if entry.get() == '':
			pass
		elif int(entry.get()) > 0 and int(entry.get())<50:
			next_step = True
		else:
			raise ValueError("Not an integer between 0 and 50. Value given '%s'"%(entry.get()))

	except ValueError as a:
		wrong_entry = True


def move_forward():
	global next_step
	next_step = True

def getAnswer(tk_root,label):
	global  next_step,wrong_entry
	wrong_entry = False
	next_step = False
	value = 1
	label.configure(text = "How many mistakes were in the image?", image = "")
	# label.pack()
	answer = Tk.Entry(tk_root)
	answer.pack()
	next_b = Tk.Button(tk_root, text = "Enter", command = lambda:test_if_move_forward(answer,label))
	next_b.pack()
	
	while not next_step:

		if wrong_entry == True:
			answer.delete(0,'end')
			label.configure(text = "How many mistakes were in the image?\nPlease enter an integer greater than 0,\nand less than 50.")
			wrong_entry = False

		tk_root.update_idletasks()
		tk_root.update()
	
	value = int(answer.get())
	answer.destroy()
	next_b.destroy()
	label.configure(text = "Get ready for next image.")
	tk_root.update_idletasks()
	tk_root.update()
	return value

def wait_for_participant(tk_root, label):
	global next_step
	continue_button = Tk.Button(tk_root, text = "Continue", command = lambda:move_forward())
	continue_button.pack()
	while not next_step:
		tk_root.update_idletasks()
		tk_root.update()

	continue_button.destroy()
	next_step = False



if __name__ == "__main__":
	try:
		condition = sys.argv[1]
	except:
		condition = "Positive"
	
	imageTime = 30     # seconds 
	waitTime = 5     # seconds
	ipaddress = "192.168.0.102"

	itteration = 0

	image_files = []
	for x in os.listdir(os.getcwd()+"/images"):
		image_files.append(os.getcwd()+"/images/"+ str(x))

	#assures same order independent of listdir, probably unnecessary
	image_files.sort()


	#Connection Info to NAO
	ip = "localhost" 
	port = 9559

	conditions = {"Positive":0,"positive":0,"P":0,"p":0,"pos":0,"Pos":0,"Neutral":1,"neutral":1,"Neu":1,"neu":1,"E":1,"e":1,"Negative":2,"negative":2,"N":2,"n":2,"Neg":2,"neg":2}
	con_index = conditions[condition]

	#initiate robot communication
	tts = ALProxy("ALTextToSpeech", "192.168.0.102", 9559)
	motion = ALProxy("ALRobotPosture", "192.168.0.102", 9559)
	animatedTts = ALProxy("ALAnimatedSpeech", "192.168.0.102", 9559)


	#setting up window
	root = Tk.Tk()
	root.title("HRI Study")
	root.geometry("620x375+650+352")
	root.configure(background="gray")

	main_label = Tk.Label(root)
	main_label.pack(side = "top",fill = 'both', expand = 'yes')
	main_label.configure(text = "Press the Continue button to start the experiment.")
	wait_for_participant(root,main_label)

	main_label.configure(text = "Thank you for participating. \n Test will begin shortly.")

	root.update_idletasks()
	root.update()
	time.sleep(waitTime)

	#Perform Robot Welcome
	robotWelcome()

	for x in  image_files:
		itteration += 1

		time.sleep(waitTime)
		
		loadImage(root,main_label,x)		

		time.sleep(imageTime)

		answer = getAnswer(root,main_label)

		#on even images have the robot say things
		if itteration %2 ==0:
			saying = conditionSayings[con_index][(itteration/2)-1]
			#if desired animated, add animation calls to strings in conditionSayings at top of this doc
			#and swap comments on following lines

			tts.say(saying)
			# animatedTts.say(saying)

	#closing script
	main_label.configure(text = "Experiment is complete. \nThank you for your time!")
	root.update_idletasks()
	root.update()
	time.sleep(waitTime)
	tts.say("Thank you for your time.")
	time.sleep(.5)
	tts.say("The experiment is now complete.")
	time.sleep(1)
	animatedTts.say("Please^start(animations/Stand/Gestures/Please_1) call the experimenter back to the room.")
	tts.say("Good bye")
	motion.goToPosture("Stand", 1.0)
	time.sleep(115)
	
