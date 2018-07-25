import Tkinter as Tk
from PIL import Image, ImageTk
from os import listdir
import time
import datetime
import csv
from naoqi import ALProxy

# Robot welcome and startup
def robotWelcome():
    # Welcome script

    # make sure robot is sitting down
    motion.goToPosture("Sit", 1.0)

    animatedTts.setBodyLanguageMode(2)
    time.sleep(1)
    animatedTts.say("^start(animations/Sit/Hello) Hello! ")
    animatedTts.say("^start(animations/Sit/Gestures/Enthusiastic_5)Nice to meet you!")
    animatedTts.say("My^wait(animations/Sit/Gestures/Me_1)name is Oscar")

    tts.say("Thank you for spending a bit of time with me")
    animatedTts.say("Let me walk ^start(animations/Sit/Gestures/You_1)you through the task")
    tts.say("There will be a total of six tasks")
    tts.say("In each, you will  be presented with a series of screens")
    animatedTts.say("Please^start(animations/Sit/Gestures/Please_1) look closely at the word at the bottom of the screen")
    animatedTts.say("Then select^start(animations/Sit/Gestures/Enthusiastic_4)all the pictures that show that object")
    tts.say("For example, if it says pen, then select all pens")
    tts.say("If you make a mistake and select one in error, dont worry!")
    tts.say("You can click again to deselect it")
    animatedTts.say("No problem^start(animations/Sit/Gestures/Enthusiastic_5)")
    time.sleep(3)
    tts.say("After you finish each task, I will check your answers")
    tts.say("Now let's get started.")
    time.sleep(1)

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

    def bcolorchange(self,x):
        currColor = self.but[x].config('bg')[-1]
        if currColor == "blue":
            self.but[x].configure(bg="red")
        else:
            self.but[x].configure(bg="blue")

    def do_buttons(self, files):
        self.but = [0 for x in range(1,10)]
        self.photo = [0 for x in range (1,10)]

        for button in range(0,9):
            self.imgName = files[button]

            self.photo[button] = ImageTk.PhotoImage(Image.open(self.imgName))

            self.but[button] = Tk.Button(self.frame, height=150, width=150, borderwidth=30, image=self.photo[button], bg="blue", command=lambda x=button: self.bcolorchange(x))
            row, col = divmod(button,3)
            self.but[button].grid(row=row+1, column=col+1)

    def stopProg(self,e):
        elapsedTime = time.time() - self.startTime
        #print ("Elapsed time " + str(elapsedTime) + " ")

        #compute and write to file the percentage accuracy for this screen
        correct = 0
        incorrect = 0
        for x in range(0, 9):
            answer = self.but[x].config('bg')[-1]
            # number of correct answers minus a penalty for incorrect choices
            if answer == "red":
                if (x + 1) in self.correctAnswers:
                    correct += 1
                else:
                    incorrect += 1

        if (correct+incorrect > 0):
            maxCorrect = self.correctAnswers.__len__()
            self.outputFile.write("%d, %d, %d, %d, %d\n" % (self.currentTask,self.screen, correct, maxCorrect, incorrect))

            if elapsedTime < self.subtaskTime:
                self.screen += 1
                self.typeselect()
            else:
                self.parent.destroy()

    def choosefiles(self):
        row = next(self.scriptReader)
        self.currType = row[0]

        chosenFiles = []
        correctAnswers = []

        for i in range(2,20,2):
            type = row[i]
            x = row[i+1]
            if type == self.currType:
                correctAnswers.append(int(i/2))
            imgfiles = listdir("images/"+type)
            chosenfile = imgfiles[int(x)]

            #print ("choosing "+chosenfile)
            chosenFiles.append("images/"+type+"/"+chosenfile)
        #print (correctAnswers)
        return chosenFiles,correctAnswers

    def typeselect(self):

        self.chosenFiles, self.correctAnswers = self.choosefiles()
        self.do_buttons(self.chosenFiles)

        vartext = "Select Images of: "
        self.label = Tk.Label(self.frame,text=vartext,width=20,font='Helvetica 8 bold')
        self.label.grid(row=4,column=2)

        self.labelType = Tk.Label(self.frame,text=self.currType.upper(),width=8, font='Helvetica 16 bold')
        self.labelType.grid(row=5,column=2)

        self.label2 = Tk.Label(self.frame,text="then click NEXT")
        self.label2.grid(row=6,column=2)

        self.nextbut = Tk.Button(self.frame,text="NEXT",font = 'Helvetica 10 bold')
        self.nextbut.grid(row=7, column=2)
        self.nextbut.bind('<Button-1>', self.stopProg)

    def initialize(self):
        self.parent.title("SUBTASK %d" % self.currentTask)
        self.parent.grid_rowconfigure(1, pad=20, weight=1)
        self.parent.grid_columnconfigure(1, pad=20, weight=1)

        self.parent.geometry('640x800+600+100')
        self.parent.resizable(False,False)

        self.frame = Tk.Frame(self.parent)
        self.frame.pack(fill=Tk.X, padx=5, pady=5)

        #start sub-task time
        self.startTime = time.time()

        #start first screen
        self.screen = 1
        self.typeselect()

# Behavior between subtasks: currently just waits
class HRIWait(Tk.Frame):
    def __init__(self, parent,waitTime):
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
        self.label2 = Tk.Label(self.frame, width=29, text="Click NEXT when ready to continue",font='Helvetica 14 bold')
        self.label2.grid(row=2, column=0)

        self.nextbut = Tk.Button(self.frame,text="NEXT",font = 'Helvetica 16 bold')
        self.nextbut.grid(row=3, column=0)
        self.nextbut.bind('<Button-1>', self.stopProg)

    def initialize(self):
        self.parent.title("PLEASE WAIT")
        self.parent.grid_rowconfigure(1, weight=1)
        self.parent.grid_columnconfigure(1, weight=1)

        self.parent.geometry('425x100+800+450')
        self.parent.resizable(False,False)

        self.frame = Tk.Frame(self.parent)
        self.frame.pack(fill=Tk.X, padx=5, pady=5)

        #start sub-task time
        self.startTime = time.time()

        #start first screen
        self.typeselect()

# Task Evaluation METHOD
def taskEvaluation(condition,conditionSay,task, percent):

    time.sleep(1)
    sayText = "You have finished the %s task" % task
    tts.say(sayText)
    tts.say("I will now evaluate your answers")
    time.sleep(2)
    sayText = "I have evaluated your answers"
    tts.say(sayText)

    # POSITIVE CONDITION
    if condition == 1:
        animatedTts.say("And^start(animations/Sit/Gestures/YouKnowWhat_1) you know what")
        time.sleep(.5)
        animatedTts.say("^start(animations/Sit/Gestures/Enthusiastic_4)You have done great!")
        sayText = "You've done better than %d percent of users" % percent
        tts.say(sayText)
        sayText ="^start(animations/Sit/Gestures/Enthusiastic_4)%s" % conditionSay
        animatedTts.say(sayText)
        tts.say("Keep up the great work!")
    # NEGATIVE CONDITION
    elif condition == 3:
        animatedTts.say("And^start(animations/Sit/Gestures/YouKnowWhat_1) you know what")
        time.sleep(.5)
        tts.say("You have not done well")
        sayText = "You've done worse than %d percent of users" % percent
        tts.say(sayText)
        sayText ="In fact, ^start(animations/Sit/Gestures/Enthusiastic_4)%s" % conditionSay
        animatedTts.say(sayText)
        tts.say("Please try to do better if you can.")

    time.sleep(2)
    animatedTts.say("Now ^start(animations/Sit/Gestures/Enthusiastic_5) let's do it again.")
    time.sleep(1)

# Final Survey QUESTIONS
class HRISurvey(Tk.Frame):
    def __init__(self, parent,outputFile,gqsQuestions,question):
        Tk.Frame.__init__(self, parent)
        self.parent = parent
        self.outputFile = outputFile
        self.gqsQuestions = gqsQuestions
        self.question = question
        self.questions = self.gqsQuestions.__len__()
        self.initialize()

    def stopProg(self, e):
        # Check that all questions were answered
        allChecked = True
        for x in range (0,self.var.__len__()-1):
            if (self.var[x].get() == 0):
                allChecked = False

        # If ALL answered, terminate
        if allChecked:
            for x in range (0,self.var.__len__()-1):
                self.outputFile.write("%d" % (self.var[x].get()))
                #add commas except to last number
                if (x < (self.var.__len__()-2)):
                    self.outputFile.write(",")
                else:
                    self.outputFile.write("\n")

            self.parent.destroy()

    def typeselect(self):
        # Frame for Title
        self.frame = Tk.Frame(self.parent)
        self.frame.pack(fill=Tk.X, padx=5, pady=5)

        self.label = Tk.Label(self.frame, text=self.question, width=48, font='Helvetica 14 bold')
        self.label.grid(row=1,column=3)

        # Frame for buttons
        self.frame2 = Tk.Frame(self.parent)
        self.frame2.pack(fill=Tk.X, padx=5, pady=5)

        self.var = [0 for x in range(self.questions+1)]
        self.questionLabel = [0 for x in range(self.questions+1)]

        #There will be 7 buttons on scale
        self.but = [0 for x in range(8)]
        number = 0

        for question in self.gqsQuestions:
            self.questionLabel[number] = Tk.Label(self.frame2, text = question, width=40).grid(row=3+number,column=0)

            self.var[number] = Tk.IntVar()
            self.but[number] = [0 for x in range(1,9)]
            for button in range(1,8):
                self.but[number][button] = Tk.Radiobutton(self.frame2,text=str(button),value=button,variable=self.var[number])
                self.but[number][button].grid(row=3+number,column=button+1)

            number += 1

        # Frame for clicking Next
        self.frame3 = Tk.Frame(self.parent)
        self.frame3.pack(fill=Tk.X, padx=5, pady=5)
        self.label2 = Tk.Label(self.frame3, width= 48,text="Click DONE when finished",font='Helvetica 14 bold')
        self.label2.grid(row=2+7, column=8)
        self.nextbut = Tk.Button(self.frame3, text="DONE", font='Helvetica 14 bold')
        self.nextbut.grid(row=3+7, column=8)
        self.nextbut.bind('<Button-1>', self.stopProg)

    def initialize(self):
        self.parent.title("EVALUATION: SURVEY")
        self.parent.grid_rowconfigure(1, weight=1)
        self.parent.grid_columnconfigure(1, weight=1)

        geometry = '700x%d+700+250' % (self.questions*67)

        self.parent.geometry(geometry)
        self.parent.resizable(False, False)

        # start first screen
        self.typeselect()

###################################################################################
# Start the main program here
if __name__ == "__main__":

    ##### CONTROL APP USING VARIABLES BELOW #######################################################
    # all times are in seconds

    # number of subtasks and time for each
    totalSubtasks = 5
    subtaskTime = 30     # seconds to perform task
    waitTime = 2        # MINIMUM wait period time between subtasks

    # Connectin to NAO
    ip = "192.168.1.140" # "192.168.1.140"#"localhost"
    port = 9559

    # Order in which contiditions will be applied
    conditionOrder = [1,2,3,3,2,1,2,1,3]       # Latin ladder for 9 subjects - repeat for more

    ############################################
    # ROBOT UTTERANCES  AND SURVEY QUESTIONS

    # CONDITION FEEBACK TO PARTICIPANT - Need minimum one per subtask
    conditionSayings = [
        # condition 1 - POSITIVE
        [
            ("You are the best"),
            ("You are awesome"),
            ("You are so cool"),
            ("You are amazing"),
            ("You are red hot"),
            ("You are inspired today"),
            ("You are on fire"),
            ("You are the best")
        ],
        # condition 2 neutral is empty
        [
            (""),
            (""),
            (""),
            (""),
            (""),
            (""),
            (""),
            ("")
        ],
        # condition 3 - NEGATIVE
        [
            ("You are not on the ball"),
            ("You are lagging behind"),
            ("You are distracted, I guess"),
            ("You are not on your game today"),
            ("You need some practice"),
            ("You are not so good at this"),
            ("Boy, you just don't get it"),
            ("This is not great performance")
        ]
    ]

    taskOrder = [("none"),("first"),("second"),("third"),("fourth"),("fifth"),("sixth"),("seventh")]

    percents = [85,87,92,92,94,93,95]

    # SURVEY: Questions for survey - more can be added / deleted
    gqsQuestionsAnimacy = [
        ("Dead.....Alive"),
        ("Stagnant.....Lively"),
        ("Mechanical.....Organic"),
        ("Artificial.....Lifelike"),
        ("Inert.....Interactive"),
        ("Apathetic.....Responsive")
    ]

    gqsQuestionsLikeability = [
        ("Dislike.....Like"),
        ("Unfriendly.....Friendly"),
        ("Unkind.....Kind"),
        ("PLEASE SELECT 3"),
        ("Unpleasant.....Pleasant"),
        ("Awful.....Nice")
    ]

    gqsQuestionsIntelligence = [
        ("Incompetent.....Competent"),
        ("Ignorant.....Knowledgeable"),
        ("Irresponsible.....Responsible"),
        ("Unintelligent.....Intelligent"),
        ("Foolish.....Sensible")
    ]

    gqsQuestionsSelf = [
        ("Incompetent.....Competent"),
        ("Ignorant.....Knowledgeable"),
        ("Unintelligent.....Intelligent"),
        ("Foolish.....Sensible"),

    ]



    ################################################################################################################
    ################################################################################################################
    ############################### DONT TOUCH BELOW
    # initiate robot communication
    tts = ALProxy("ALTextToSpeech", ip, port)
    motion = ALProxy("ALRobotPosture", ip, port)
    animatedTts = ALProxy("ALAnimatedSpeech", ip, port)

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
        subjectSurvey = ("data\subject_II_%d_%d_%s_Survey.txt" % (subject,condition,st))
        surveyFile = open(subjectSurvey,"w")


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

        # #############
        # Prepare robot for survey
        tts.say("We are almost done")
        animatedTts.say("Please^start(animations/Sit/Gestures/Please_1) Read carefully and answer these final questions")
        tts.say("Read the question at the top carefully")
        time.sleep(.5)
        tts.say("Below you will see pairs of words")
        tts.say("Select a number from one to seven for each pair")
        tts.say("the number one corresponds to the word on the left")
        tts.say("and seven to the word on the right")
        tts.say("and of course you can select any number in between")
        animatedTts.say("^start(animations/Sit/Gestures/Enthusiastic_4)Let's do it!")
        time.sleep(1)
        # Do Survey Questions
        vartext = "Please rate your impression of the ROBOT on these scales:"
        root = Tk.Tk()
        app = HRISurvey(root,surveyFile,gqsQuestionsAnimacy,vartext)
        root.mainloop()

        root = Tk.Tk()
        app = HRISurvey(root,surveyFile,gqsQuestionsLikeability,vartext)
        root.mainloop()

        root = Tk.Tk()
        app = HRISurvey(root,surveyFile,gqsQuestionsIntelligence,vartext)
        root.mainloop()

        vartext = "How did the robot make YOU feel:"
        root = Tk.Tk()
        app = HRISurvey(root,surveyFile,gqsQuestionsSelf,vartext)
        root.mainloop()

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
        surveyFile.close()

        # get ready for next subject
        subject += 1
