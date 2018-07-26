#!/usr/bin/env python

# -*- coding: utf-8 -*-
# @Author: ahpalmerUNR
# @Date:   2018-07-25 13:43:18
# @Last Modified by:   ahpalmerUNR
# @Last Modified time: 2018-07-26 16:07:27

import Tkinter as Tk 
from PIL import Image, ImageTk
import os
import sys
import time
from naoqi import ALProxy

next_step = False 

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
			"You are halfway through",
			"You can move on now",
			"You are done now",
			#"",
			#"",
			#"",
			#"",
		],
		# condition 3 - NEGATIVE
		[
			"You are really bad at this",
			"You are doing terrible",
			"You just dont get this",
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
	animatedTts.say("Let me walk ^start(animations/Stand/Gestures/You_1)you through the task")
	tts.say("There will be a total of eight images")
	tts.say("You will have thirty seconds to count the number of things wrong in each image")
	animatedTts.say("Please^start(animations/Stand/Gestures/Please_1) answer as quickly and acurately as possible")
	animatedTts.say("you will need to enter ^start(animations/Stand/Gestures/Enthusiastic_4)a nonzero numerical value")
	time.sleep(3)
	tts.say("After you finish each task, I will check your answers")
	tts.say("Now let's get started.")
	time.sleep(1)
	

def loadImage(tk_root,label,image_name):
	display_image = ImageTk.PhotoImage(Image.open(image_name))
	label.configure(image=display_image)
	label.image = display_image
	
	tk_root.update_idletasks()
	tk_root.update()

def test_if_move_forward(entry,label):
	global next_step
	print(entry.get())
	try:
		if entry.get() == '':
			pass
		elif int(entry.get()) > 0 and int(entry.get())<50:
			next_step = True
		else:
			raise ValueError("Not an integer between 0 and 50. Value given '%s'"%(entry.get()))
	except ValueError() as a:
		print(a)
		entry.delete(0,END)
		entry.insert(0,"Not good value.")
		label.configure(text = "How many mistakes were in the image?\nPlease enter an integer greater than 0,\nand less than 50.")
		label.text = "How many mistakes were in the image?\nPlease enter an integer greater than 0,\nand less than 50."

def getAnswer(tk_root,label):
	global  next_step
	next_step = False
	value = 1
	label.configure(text = "How many mistakes were in the image?", image = "")
	label.pack()
	answer = Tk.Entry(tk_root, textvariable = '1')
	answer.pack()
	next_b = Tk.Button(tk_root, text = "Enter", command = lambda:test_if_move_forward(answer,label))
	next_b.pack()
	
	while not next_step:
		
		tk_root.update_idletasks()
		tk_root.update()
	
	value = int(answer.get())
	answer.destroy()
	next_b.destroy()
	return value


if __name__ == "__main__":
	try:
		condition = sys.argv[1]
	except:
		condition = "Positive"
	
	imageTime = 10     # seconds 
	waitTime = 5     # seconds
	ipaddress = "192.168.0.109"

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
	tts = ALProxy("ALTextToSpeech", ipaddress, 9559)
	motion = ALProxy("ALRobotPosture", ipaddress, 9559)
	animatedTts = ALProxy("ALAnimatedSpeech", ipaddress, 9559)


	#setting up window
	root = Tk.Tk()
	root.title("HRI Study")
	root.geometry("620x375+650+352")
	root.configure(background="gray")
	waitTillPersonReady = raw_input("Press Enter to Start.")
	main_label = Tk.Label(root)
	main_label.pack(side = "top",fill = 'both', expand = 'yes')
	main_label.configure(text = "Thank you for participating. \n Test will begin shortly.")
	# main_label.text = "Thank you for participating. \n Test will begin shortly."
	root.update_idletasks()
	root.update()
	time.sleep(waitTime)
	#Perform Robot Welcome
	
	# robotWelcome()
	time_start = time.time()
	for x in  image_files:
		itteration += 1
		print(x)
		loadImage(root,main_label,x)		

		time.sleep(imageTime)#Time to display image in seconds

		answer = getAnswer(root,main_label)


		# print(answer,itteration)

		#putting saying stuff here
		if itteration %2 ==1:
			saying = conditionSayings[con_index][(itteration-1)/2]
			#if desired animated, add animation calls to strings in conditionSayings at top of this doc
			#and swap comments on following lines
			tts.say(saying)
			# animatedTts.say(saying)
		
		# time.sleep(waitTime)


	time.sleep(waitTime)
	

	#closing script
	main_label.configure(text = "Experiment is complete. \nThank you for your time!")
	tts.say("Thank you for your time.")
	time.sleep(.5)
	tts.say("The experiment is now complete.")
	time.sleep(1)
	animatedTts.say("Please^start(animations/Sit/Gestures/Please_1) call the experimenter back to the room.")
	tts.say("Good bye")
	time.sleep(115)