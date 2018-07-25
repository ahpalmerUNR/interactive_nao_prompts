import Tkinter as Tk
from PIL import Image, ImageTk
from os import listdir
import time
import datetime
from threading import Timer
import csv
from naoqi import ALProxy

# Robot welcome and startup
def robotWelcome():
    # Welcome script

    '''
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
	'''
# Perform subtask
class HRISubtask(Tk.Frame):
    def __init__(self, parent, output_file, script_reader, task, time):
        Tk.Frame.__init__(self, parent)
        self.parent = parent
        self.currentTask = task
        self.subtaskTime = time
        self.outputFile = output_file
        self.scriptReader = script_reader
        self.initialize()

    def bcolorchange(self):
    	pass
    	'''
        currColor = self.but[x].config('bg')[-1]
        if currColor == "blue":
            self.but[x].configure(bg="red")
        else:
            self.but[x].configure(bg="blue")
        '''

    def do_buttons(self, files):
        self.but = [0 for x in range(1,10)]
        self.photo = [0 for x in range (1,10)]

        #changes image size
        self.imgName = files[0]
        self.photo[0] = ImageTk.PhotoImage(Image.open(self.imgName))
        self.but[0] = Tk.Button(self.frame, height=350, width=1000, borderwidth=0, image=self.photo[0], bg="gray85", command=lambda x=0: self.bcolorchange())
        self.but[0].grid(row=1,column=1)


    def stopProg(self,e):
        elapsedTime = int(time.time()) - int(self.startTime)
        # print(elapsedTime)
	
        #print ("Elapsed time " + str(elapsedTime) + " ")

        # #compute and write to file the percentage accuracy for this screen
        # correct = 0
        # incorrect = 0
        # # for x in range(0, 9):
        # answer = self.but[0].config('bg')[-1]
        # # number of correct answers minus a penalty for incorrect choices
        # if answer == "red":
        #     if (x + 1) in self.correctAnswers:
        #         correct += 1
        #     else:
        #         incorrect += 1

        # if (correct+incorrect > 0):
        #     maxCorrect = self.correctAnswers.__len__()
        #     self.outputFile.write("%d, %d, %d, %d, %d\n" % (self.currentTask,self.screen, correct, maxCorrect, incorrect))

        if elapsedTime > self.subtaskTime:
        	# print("not done yet")
        	self.screen += 1
        	self.typeselect()
        else:
        	# print("done")
        	self.parent.destroy()
   		

    def choosefiles(self):
        row = next(self.scriptReader)
        self.currType = row[0]

        chosenFiles = []
        correctAnswers = []

        for i in range(2,4,2):
            type = row[i]
            x = row[i+1]
            print (i, type, x)
            if type == self.currType:
                correctAnswers.append(int(i/2))
            imgfiles = listdir("/home/rrl/Downloads/images/"+type)
            chosenfile = imgfiles[int(x)]

            print ("choosing "+chosenfile)
            chosenFiles.append("/home/rrl/Downloads/images/"+type+"/"+chosenfile)
        print (correctAnswers)
        return chosenFiles,correctAnswers



		
    def typeselect(self):

        self.chosenFiles, self.correctAnswers = self.choosefiles()
        self.do_buttons(self.chosenFiles)
        
        vartext = "Select Images of: "
        self.label = Tk.Label(self.frame,text=vartext,width=20,font='Helvetica 8 bold')
        self.label.grid(row=50,column=2)

        self.labelType = Tk.Label(self.frame,text=self.currType.upper(),width=8, font='Helvetica 16 bold')
        self.labelType.grid(row=80,column=2)

        self.label2 = Tk.Label(self.frame,text="How many things are wrong with this image?", font = 'Helvetica 16 bold')
        self.label2.grid(row=200,column=1)


        # self.startTime = time.sleep(30)
       
       	t = Timer(5.0,self.parent.destroy)
       	t.start()
        # self.nextbut = Tk.Button(self.frame,text="NEXT",font = 'Helvetica 10 bold')
        # self.nextbut.grid(row=200, column=1)
        # self.nextbut.bind('<Button-1>', self.stopProg)

    def initialize(self):
        self.parent.title("SUBTASK %d" % self.currentTask)
        self.parent.grid_rowconfigure(1, pad=20, weight=1)
        self.parent.grid_columnconfigure(1, pad=20, weight=1)

        self.parent.geometry('1000x1000+300+100')
        self.parent.resizable(False,False)

        self.frame = Tk.Frame(self.parent)
        self.frame.pack(fill=Tk.X, padx=5, pady=5)

        #start sub-task time
       	self.startTime = time.time()


        #start first screenm m m<
        self.screen = 1
        self.typeselect()



# Behavior between subtasks: currently just waits
class HRIWait(Tk.Frame):
    def __init__(self, parent, waitTime):
        Tk.Frame.__init__(self, parent)
        self.parent = parent
        self.subtaskTime = waitTime
        self.initialize()


    def stopProg(self,e):
        elapsedTime = time.time() - self.startTime
        #print ("Elapsed time " + str(elapsedTime) + " ")

        if elapsedTime > self.subtaskTime:
            self.parent.destroy()

    def typeselect(self):
        #vartext = "Subtask End"
        #self.label = Tk.Label(self.frame, text=vartext, font='Helvetica 8 bold')
        #self.label.grid(row=1,column=0)

        #self.entry = entry("Input number")
        #self.entry.grid(row=1, column=0)

        self.label2 = Tk.Label(self.frame, width=35, text="Click NEXT when ready to continue",font='Helvetica 14 bold')
        self.label2.grid(row=2, column=0)

        self.nextbut = Tk.Button(self.frame,text="NEXT",font = 'Helvetica 16 bold')
        self.nextbut.grid(row=3, column=0)
        self.nextbut.bind('<Button-1>', self.stopProg)

    def show_entry_fields(self):
    	master=Tk()
    	self.label=Tk.Label(self.master, text="enter number")
    	e1= Entry(master)
    	e1.grid(row=0, column=1)

    	

        #this is the frame before the task starts
    def initialize(self):
        self.parent.title("PLEASE WAIT")
        self.parent.grid_rowconfigure(1, weight=1)
        self.parent.grid_columnconfigure(1, weight=1)

        self.parent.geometry('365x100+800+450')
        self.parent.resizable(False,False)

        self.frame = Tk.Frame(self.parent)
        self.frame.pack(fill=Tk.X, padx=5, pady=5)

        #start sub-task time
        self.startTime = time.time()

        #start first screen
        self.typeselect()

#TESTING OUT NOCALLBACK FRAME
'''
class HRICount(Tk.Frame):
	def __init__(self, parent,waitTime):
		Tk.Frame.__init__(self, parent)
		self.parent = parent
		self.subtaskTime = waitTime
		self.initilize()

	def typeselect(self):
		#artext = "please enter a number"
		#elf.label2 = Tk.label (self.frame, width=35, text=vartext, font='Helvetica 14 bold')
		#elf.label2.grid(row=2, column=0)

	def initilize(self):
		self.parent.title("End of task")
		self.parent.grid_rowconfigure(1, weight=1)
		self.parent.grid_columnconfigure(1, weight=1)

		self.parent.geometry('500x500+800+100')
		self.parent.resizable(False,False)

		self.frame = Tk.Frame(self.parent)
		self.frame.pack(fill=Tk.X, padx=5, pady=5)
		self.startTime = time.time()
		self.typeselect()
'''



# Task Evaluation METHOD
def taskEvaluation(condition,conditionSay,task, percent):

    time.sleep(1)
    #ayText = "You have finished the %s task" % task
   #tts.say(sayText)
    tts.say("I will now evaluate your answers")
    time.sleep(2)
    sayText = "I have evaluated your answers"
    tts.say(sayText)

    # POSITIVE CONDITION
    if condition == 1:
        #nimatedTts.say("^start(animations/Sit/Gestures/YouKnowWhat_1) you know what")
        #ime.sleep(.5)
        #nimatedTts.say("^start(animations/Sit/Gestures/Enthusiastic_4)You have done great!")
        #ayText = "You've done better than %d percent of users" % percent
        #ts.say(sayText)
        sayText ="^start(animations/Stand/Gestures/enthusiastic_3)%s" % conditionSay
        animatedTts.say(sayText)
        tts.say("Keep up the great work!")
    # NEGATIVE CONDITION
    elif condition == 3:
        animatedTts.say("And^start(animations/Sit/Gestures/YouKnowWhat_1) you know what")
        time.sleep(.5)
        tts.say("You have not done well")
        #ayText = "You've done worse than %d percent of users" % percent
        tts.say(sayText)
        sayText ="In fact, ^start(animations/Sit/Gestures/Enthusiastic_4)%s" % conditionSay
        animatedTts.say(sayText)
        tts.say("Please try to do better if you can.")

    time.sleep(2)
    #animatedTts.say("Now ^start(animations/Stand/Gestures/Enthusiastic_2) let's do it again.")
    #time.sleep(1)


###################################################################################
# Start the main program here
if __name__ == "__main__":

    ##### CONTROL APP USING VARIABLES BELOW #######################################################
    # all times are in seconds

    # number of subtasks and time for each
    totalSubtasks = 8
    subtaskTime = 2     # seconds to perform task
    waitTime = 5     # MINIMUM wait period time between subtasks

    # Connectin to NAO
    ip = "localhost" 
    port = 9559

    # Order in which contiditions will be applied
    conditionOrder = [1,3,3,3,2,1,2,1,3]       # Latin ladder for 9 subjects - repeat for more

    ############################################
    # ROBOT UTTERANCES  AND SURVEY QUESTIONS

    # CONDITION FEEBACK TO PARTICIPANT - Need minimum one per subtask
    conditionSayings = [
        # condition 1 - POSITIVE
        [
            ("You are really good at this"),
            ("You are doing really well"),
            ("You are really mastering this"),
           #("You are amazing"),
            ("You did really well"),
           #("You are inspired today"),
            #"You are on fire"),
           #("You are the best")
        ],
        # condition 2 neutral is empty
        [
            ("You can continue to the next image"),
            ("You are halfway through"),
            ("You can move on now"),
            ("You are done now"),
            #(""),
            #(""),
            #(""),
            #("")
        ],
        # condition 3 - NEGATIVE
        [
            ("You are really bad at this"),
            ("You are doing terrible"),
            ("You just dont get this"),
            ("You did really badly"),
            #("You need some practice"),
            #("You are not so good at this"),
            #("Boy, you just don't get it"),
            #("This is not great performance")
        ]
    ]

    taskOrder = [("none"),("first"),("second"),("third"),("fourth"),("fifth"),("sixth"),("seventh")]

    percents = [85,87,92,92,94,93,95]




    ################################################################################################################
    ################################################################################################################
    ############################### DONT TOUCH BELOW
    # initiate robot communication
    tts = ALProxy("ALTextToSpeech", "192.168.1.138", 9559)
    motion = ALProxy("ALRobotPosture", "192.168.1.138", 9559)
    animatedTts = ALProxy("ALAnimatedSpeech", "192.168.1.138", 9559)


    subject = 0

    while (True):
        condition = conditionOrder[subject % 9]

        #Wait until subject ready to go
        root = Tk.Tk()
        app = HRIWait(root, waitTime)
        root.mainloop()

        # ##################################################
        # # open scriptfile
        scriptFile = open("script.csv")
        scriptReader = csv.reader(scriptFile)

        # create subject results file

        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%m-%d-%H-%M-%S')

        subjectFile = ("data\subject_II_%d_%d_%s_Output.txt" % (subject,condition,st))
        outputFile = open(subjectFile, "w")
       #subjectSurvey = ("data\subject_II_%d_%d_%s_Survey.txt" % (subject,condition,st))
       #surveyFile = open(subjectSurvey,"w")


        ####################################################################################
        # START INTERACTION

        #Perform Robot Welcome
        robotWelcome()

        ############
        # Perform Tasks
        for task in range(1,totalSubtasks+1):
            # #do subtask
            root = Tk.Tk()
            app = HRISubtask(root, outputFile, scriptReader, task, subtaskTime)
            root.mainloop()

            #wait between subtasks
            if task < totalSubtasks:    # No need to wait after last subtask
                root = Tk.Tk()
                app = HRIWait(root,.5) # wait briefly between subtasks
                root.mainloop()

                #Evaluate Task
                taskEvaluation(condition, conditionSayings[condition-1][task-1], taskOrder[task], percents[task - 1])

        ###############
        # Finish up and clean house
        tts.say("Thank you for your time.")
        time.sleep(.5)
        tts.say("The experiment is now complete.")
        time.sleep(1)
        animatedTts.say("Please^start(animations/Sit/Gestures/Please_1) call the experimenter back to the room.")
        tts.say("Good bye")
        time.sleep(5)

        # Close subject output files
        outputFile.close()
        scriptFile.close()
       #surveyFile.close()

        # get ready for next subject
        subject += 1
