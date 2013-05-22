from Tkinter import *
from tkSimpleDialog import askstring
from tkFileDialog   import asksaveasfilename, askopenfilename
from tkMessageBox import askokcancel, showinfo
import tkColorChooser
import webbrowser
import sys
import os
import subprocess

# line that checks the version of tkinter 
#Tkinter._test()
global robotName
robotName = None
global fileName
fileName = None

class ScrolledText(Frame):
    """ class that creates a scrolled text are inside the frame"""
    def __init__(self, parent=None, text='', file=None):
        # start the frame, set background color to white
        

        # read the filename specified by setup.py and assign global robotName to it
        if len(sys.argv) == 2:
            global fileName
            fileName = "./robots/" + sys.argv[1]
            name = sys.argv[1]
            global robotName
            robotName = name[:-3]
            
        if len(sys.argv) == 1:
            global fileName
            fileName = asksaveasfilename(defaultextension='.py', initialdir='./robots/',title="Create New Robot")
            if (len(fileName) == 0):
                print("quit")
                sys.exit()
            if fileName[-3:] != ".py":
                fileName = fileName + ".py"
            global robotName
            robotName = fileName.split("/")[len(fileName.split("/"))-1][:-3]
            print(robotName)
        
        Frame.__init__(self, parent, background="white")
        self.pack(expand=YES, fill=BOTH)               
        self.makewidgets()
        if len(sys.argv) == 2:
            self.settext(text, fileName)
    # inner method that creates the scrollable text area    
    def makewidgets(self):
        sbar = Scrollbar(self)
        text = Text(self, relief=SUNKEN, undo=TRUE, wrap=WORD, autoseparators=True,
                    maxundo=1000)
        sbar.config(command=text.yview)                  
        text.config(yscrollcommand=sbar.set)           
        sbar.pack(side=RIGHT, fill=Y)                   
        text.pack(side=LEFT, expand=YES, fill=BOTH)     
        self.text = text

    # setter method to use for opening new files
    def settext(self, text='', file=None):
        if file: 
            text = open(file, 'r').read()
        self.text.delete('1.0', END)                   
        self.text.insert('1.0', text)                  
        self.text.mark_set(INSERT, '1.0')              
        self.text.focus()

    # getter method to use for saving the working area
    def gettext(self):                               
        return self.text.get('1.0', END+'-1c')
        

class RobotEditor(ScrolledText):

    # call constructor
    def __init__(self, parent,file=None):

        #Frame.__init__(self, parent)
        frm = Frame(parent)
        frm.pack(fill=X)

        # reference to the parent (root)
        self.parent = parent

        # initialize the scrolled text area
        ScrolledText.__init__(self, parent, file=file)

        self.initUI()
        # set geometry manager in both directions, i.e. expand to the whole window
        # self.pack(fill=BOTH, expand=1)

        # center window
        self.centerWindow()
       

    def initUI(self):

        # set the window title to "Robot Editor"
        global robotName
        self.parent.title("RobotEditor: " + robotName +".py")

        # create a menubar (Menu widget), that will contain our menu buttons
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)
        self.parent.attributes('-topmost',1)
        

        # create a "File" menu pop-up window
        # tearoff=0 - removes the dotted line in the top of the widget
        fileMenu = Menu(menubar, tearoff=0)

        # create "New" submenu
        newSubmenu = Menu(fileMenu, tearoff=0)
        newSubmenu.add_command(label="Pythonbot", command=self.onNewBot)
        newSubmenu.add_command(label="Python file", command=self.onNewPython)
        fileMenu.add_cascade(label="New", menu=newSubmenu, accelerator="Ctrl+N")
        
        # fill the File menu with buttons
        fileMenu.add_command(label="Save", command=self.onSave)
        fileMenu.add_command(label="Save as ...", command=self.onSaveAs, accelerator="Ctrl+S")
        fileMenu.add_command(label="Rename", command=self.onRename, accelerator="Ctrl+N")

        #self.bind("<Control-S>", self.onSaveAs)
        
        fileMenu.add_separator()
        
        fileMenu.add_command(label="Exit", command=self.onExit)
        
        # add the menu to the menubar
        menubar.add_cascade(label="File", menu=fileMenu)

        # create a "Robot" menu pop-up window
        robotMenu = Menu(menubar, tearoff=0)

        # add buttons
        robotMenu.add_command(label="Change the colour...", command=self.onChangeColour)
        robotMenu.add_separator()
        robotMenu.add_command(label="Test", command=self.onTest)
        
        menubar.add_cascade(label="Robot", menu=robotMenu)

        # create an "Edit" menu pop-up window
        editMenu = Menu(menubar, tearoff=0)

        # add buttons
        editMenu.add_command(label="Undo", command=self.onUndo, accelerator="Ctrl+Q")
        editMenu.add_command(label="Redo", command=self.onRedo, accelerator="Ctrl+E")

        editMenu.add_separator()

        editMenu.add_command(label="Cut", command=self.onCut, accelerator="Ctrl+X")
        editMenu.add_command(label="Copy", command=self.onCopy, accelerator="Ctrl+C")
        editMenu.add_command(label="Paste", command=self.onPaste, accelerator="Ctrl+V")
        editMenu.add_command(label="Delete", command=self.onDelete, accelerator="Delete")

        editMenu.add_separator()

        editMenu.add_command(label="Find ...", command=self.onFind, accelerator="Ctrl+F")
        editMenu.add_command(label="Find Next", command=self.onFindNext)
        editMenu.add_command(label="Replace ...", command=self.onReplace, accelerator="Ctrl+R")

        editMenu.add_separator()

        editMenu.add_command(label="Select All", command=self.onSelectAll, accelerator="Ctrl+A")

        # add the menu to the menubar
        menubar.add_cascade(label="Edit", menu=editMenu)

        # create a "Format" menu pop-up window
        formatMenu = Menu(menubar, tearoff=0)

        formatMenu.add_command(label="Indent Region", command=self.onIndent)
        formatMenu.add_command(label="Dedent Region", command=self.onDedent)
        formatMenu.add_command(label="Format Paragraph", command=self.onFormat)

        menubar.add_cascade(label="Format", menu=formatMenu)

        # create a "Import" menu pop-up window
        importMenu = Menu(menubar, tearoff=0)

        importMenu.add_command(label="Copy Pythonbot",command=self.onImport, accelerator="Ctrl+I")

        menubar.add_cascade(label="Templates", menu=importMenu)

        # create a "Help" menu pop-up window
        helpMenu = Menu(menubar, tearoff=0)

        helpMenu.add_command(label="Editor Specification", command=self.onSpec)
        helpMenu.add_command(label="Pythonbots API", command=self.onAPI)

        menubar.add_cascade(label="Help", menu=helpMenu)
 


    # File Section    
    def onNewBot(self):
        print "New Bot"

    def onNewPython(self):
        print "Open new blank python file"
   
    def onSave(self):
        alltext = self.gettext()
        global fileName
        open(fileName, 'w').write(alltext)

    def onTest(self):
        self.onSave()
        addRobotToTesterFile(robotName)
        addTesterToRobotFile(robotName)
        process = subprocess.Popen(['python','components/Tester.py'],shell=False,stdout=subprocess.PIPE,stderr= subprocess.PIPE)
        testText = process.communicate()
        testText = testText[0]
        if (len(testText) == 0):
            testText = testText + " No Functions or commands found. "
        elif (testText[-6:-1] != "DONE!"):
            testText = testText + "\n Done command not found at end of commands. "
        testText = testText[:-1]
        os.remove("components/Tester.py")
        os.remove("robots/"+robotName+"TEST.py")
        
        results = showinfo(title="Test Results",message=testText)

    def onSaveAs(self):
        filename = asksaveasfilename(defaultextension='.py', initialdir='./robots/')
        if filename:
            alltext = self.gettext()
            open(filename, 'w').write(alltext)

    def onRename(self):
        global fileName
        target = askstring('Rename File', 'Type in the new name.')
        if target:
            newName = "./robots/" + target + ".py"
            os.rename(fileName, newName)
            fileName = newName
            self.parent.title("RobotEditor: " + target)
            import EditorMenu
            EditorMenu.RefreshScreen()
        
        
    def onExit(self):
        ans = askokcancel('Verify Exit', "Really Quit?")
        if ans:
            self.quit()

    # Robot Section
    def onChangeColour(self):
        index = self.text.search("def colour", "0.0", forwards=True)
        floatindex = float(index)
        colourtext = self.text.get((floatindex + 1.0), (floatindex + 1.99))
        r,g,b = 255,255,255
        if colourtext[-1] == ')':
            colourtext = colourtext.split("(")
            colourtext = colourtext[1]
            colourtext = colourtext[0:-1]
            colourlist = colourtext.split(",")
            r = int(colourlist[0])
            g = int(colourlist[1])
            b = int(colourlist[2])
            
        result = tkColorChooser.askcolor(title="Choose the robot colour", color=(r,g,b))
        if result:
            # get rgb value
            rgb = str(result[0])
            if rgb != 'None':
                # find the line with def colour method
                index = self.text.search("def colour", "0.0", forwards=True)
                floatindex = float(index)
                newIndex = floatindex + 1.0
                # new colour line
                newline = "    " + "    "+ "return " + rgb
                newIndex2 = newIndex + 0.99
                self.text.delete(newIndex, newIndex2)
                self.text.insert(newIndex, newline)
                
    # Edit Section
    def onUndo(self):
        try:
            self.text.edit_undo()
        except TclError:
            print
            # don't show the info message, it will interrupt user from work
            #info = showinfo("Nothing to Undo", "There is nothing to undo")

    def onRedo(self):
        try:
            self.text.edit_redo()
        except TclError:
            print
            # don't show the info message, it will interrupt user from work
            #info = showinfo("Nothing to Redo", "There is nothing to redo")

    def onCut(self):
        try:
            text = self.text.get(SEL_FIRST, SEL_LAST)
            self.text.delete(SEL_FIRST, SEL_LAST)
            self.clipboard_clear()
            self.clipboard_append(text)
        except TclError:
            info = showinfo("Select Area", "Please, select an area, first.")
    
    def onCopy(self):
        try:
            text = self.text.get(SEL_FIRST, SEL_LAST)
            self.clipboard_clear()
            self.clipboard_append(text)
        except TclError:
            info = showinfo("Select Area", "Please, select an area, first.")

    def onPaste(self):
        try:
            text = self.selection_get(selection='CLIPBOARD')
            self.text.insert(INSERT, text)
        except TclError:
            pass

    def onDelete(self):
        try:
            text = self.text.get(SEL_FIRST, SEL_LAST)
            self.text.delete(SEL_FIRST, SEL_LAST)
        except TclError:
            info = showinfo("Select Area", "Please, select an area, first.")

        
    def onFind(self):
        target = askstring('Find', 'Insert the target here.')
        if target:
            where = self.text.search(target, INSERT, END)  
            if where:                                    
                # print where
                pastit = where + ('+%dc' % len(target))   
                self.text.tag_remove(SEL, '1.0', END)     
                self.text.tag_add(SEL, where, pastit)     
                self.text.mark_set(INSERT, pastit)         
                self.text.see(INSERT)                    
                self.text.focus()

    def onFindNext(self):
        print "Find Next"

    def onReplace(self):
        print "Replace"
        """
        target = askstring('Replace', 'Insert the target here.')
        if target:
            where = self.text.search(target, INSERT, END)  
            if where:                                    
                # print where
                pastit = where + ('+%dc' % len(target))   
                self.text.tag_remove(SEL, '1.0', END)     
                self.text.tag_add(SEL, where, pastit)     
                self.text.mark_set(INSERT, pastit)         
                self.text.see(INSERT)                    
                self.text.focus()
        """

    def onSelectAll(self):
        print "Select All"

    # Format Section

    def onIndent(self):
        print "Indent"

    def onDedent(self):
        print "Dedent"

    def onFormat(self):
        print "Format"

    # Import Section

    def onImport(self):
        print "Import Pythonbot"


    # Help (Pythonbots API) Section
    def onAPI(self):
        # this method links to the webpage of the project API
        urlAPI = 'http://sourceforge.net/p/pythonrobocode/wiki/browse_pages/'
        webbrowser.open_new_tab(urlAPI)

    def onSpec(self):
        urlSpec = 'http://sourceforge.net/p/pythonrobocode/wiki/RobotEditor%20Specification/'
        webbrowser.open_new_tab(urlSpec)
    
    def centerWindow(self):

        # set window width and height
        width = 600
        height = 400

        # get screen sizes
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
            
        # calculate the centric values: x and y coordinates
        x = (sw - width)/2
        y = (sh - height)/2

        # set widnow size and center it
        self.parent.geometry('%dx%d+%d+%d' % (width, height, x, y))


def addRobotToTesterFile(robotname):
    Testerpure = file("components/TesterPURE.py")
    newlines = []
    for line in Testerpure:
        if "%ROBOTNAME" in line:
            line = line.replace("%ROBOTNAME", robotname)
        newlines.append(line)
    
    testerfile = file("components/Tester.py", 'w')
    testerfile.writelines(newlines)

def addTesterToRobotFile(robotname):
    Testerpure = file("robots/"+robotname+".py")
    newlines = []
    for line in Testerpure:
        if "import gamefile" in line:
            line = line.replace("import gamefile", "import Tester as gamefile")
        newlines.append(line)
    
    testerfile = file("robots/"+robotname+"TEST.py", 'w')
    testerfile.writelines(newlines)
    

def main():

    #obligatory line, creates tkinter
    root = Tk()

    # create an instance of the app
    app = RobotEditor(root)

    # obligatory line, enters the mainloop
    root.mainloop()


if __name__ == '__main__':
    main()
