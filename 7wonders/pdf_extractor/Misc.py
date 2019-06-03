import pickle
import os
import traceback
import time
import tkinter
import tkinter.ttk

# tkinter aliases
#
N = tkinter.N
S = tkinter.S
E = tkinter.E
W = tkinter.W
NE = tkinter.NE
SE = tkinter.SE
SW = tkinter.SW
NW = tkinter.NW
CENTER = tkinter.CENTER
tkFrame = tkinter.ttk.Frame
tkLabel = tkinter.ttk.Label
tkCombobox = tkinter.ttk.Combobox
tkStringVar = tkinter.StringVar
tkIntVar = tkinter.IntVar
tkButton = tkinter.Button
tkCheckbutton = tkinter.Checkbutton
tkLabelframe = tkinter.ttk.Labelframe
tkEntry = tkinter.ttk.Entry
tkText = tkinter.Text
tkScrollbar = tkinter.Scrollbar
tkProgressbar = tkinter.ttk.Progressbar
tkListbox = tkinter.Listbox
MajorTitleFontString = 'TkDefaultFont 20 bold'
MinorTitleFontString = 'TkDefaultFont 16 bold'
MajorFontString   = 'TkDefaultFont 16'
DefaultFontString = 'TkDefaultFont 14'
MinorFontString   = 'TkDefaultFont 12'
DefaultBoldFontString = 'TkDefaultFont 14 bold'
FixedFontString = 'TkFixedFont'

## Function to save Python object in ATK directory in pickle format
## https://stackoverflow.com/questions/19201290/how-to-save-a-dictionary-to-a-file
##	
def SaveObj(Obj = None, Name = None, SaveFolder = None):

	with open(os.path.join(SaveFolder, "{}.pkl".format(Name)), 'wb') as f:
		pickle.dump(Obj, f, pickle.HIGHEST_PROTOCOL)

## Function to load Python object in ATK directory in pickle format
## https://stackoverflow.com/questions/19201290/how-to-save-a-dictionary-to-a-file
##
def LoadObj(Name = None, SaveFolder = None):

	FileToLoad = os.path.join(SaveFolder, "{}.pkl".format(Name))
	if not os.path.exists(FileToLoad):
		return None
	with open(FileToLoad, 'rb') as f:
		return pickle.load(f)
	
## Returns the exception text
##
def GetExceptionText():
	return traceback.format_exc()
	
## pandas dataframe to csv
##
def Df2Csv(df = None, csv_path = None):
	LOG.debug("Save to {} ...".format(csv_path))
	df.to_csv(
		path_or_buf = csv_path,
		index = False,
	)

def GetConnectionStringId(
	DfRow = None,
	DeviceColumnName = None,
	ConnectionColumnName = None,
):
	if DfRow is not None:
		DeviceName     = DfRow[DeviceColumnName]
		ConnectionName = DfRow[ConnectionColumnName]
	else:
		DeviceName     = DeviceColumnName
		ConnectionName = ConnectionColumnName
		
	return "[{}] ({})".format(
		str(DeviceName    ).strip(),
		str(ConnectionName).strip(),
	).upper()

## top folder
##
TopFolder = os.path.dirname(os.path.realpath(__file__))

## proc folder
##
ProcFolder = os.path.join(TopFolder, "proc")

## Function to centre a Tk window on screen
## https://stackoverflow.com/questions/3352918/how-to-center-a-window-on-the-screen-in-tkinter
##
def CentreTkOnScreen(SomeTk = None):

	SomeTk.update_idletasks()
	w = SomeTk.winfo_screenwidth()
	h = SomeTk.winfo_screenheight()
	SomeTk.geometry().split('+')[0].split('x')
	size = tuple(int(_) for _ in SomeTk.geometry().split('+')[0].split('x'))
	x = w/2 - size[0]/2
	y = h/2 - size[1]/2
	SomeTk.geometry("%dx%d+%d+%d" % (size + (x, y)))

## Abstract class to allow user to enter some values
##
class ChoiceTk(tkinter.Tk):

	def __init__(self, Title = 'Untitled', Text = "Insert some text here.", FieldList = ['Field 1', 'Field 2']):

		# instantiate parent class first
		tkinter.Tk.__init__(self)
		
		# set McLaren logo as icon
		self.iconbitmap(r'mclaren_logo.ico')		

		# custom attributes
		self.RetVal	= None	
		
		# give window a title
		self.title(Title)
		
		# we don't want the window to be resizable
		self.resizable(False, False)

		# register on close callback
		self.protocol("WM_DELETE_WINDOW", self.OnClose)	

		# create main frame
		self.MainFrame = tkFrame(self)
		self.MainFrame.grid(row = 0, column = 0)
		
		# create text frame
		self.TextLabel = tkLabel(self.MainFrame, text = Text, font = DefaultFontString, width = 30)
		self.TextLabel.grid(row = 0, column = 0, sticky = W+E)
		
		# create buttons
		self.ButtonList = []
		for FieldIndex, Field in enumerate(FieldList):
			Button = tkButton(self.MainFrame, text = Field, font = FixedFontString, command = lambda ButtonIndex = FieldIndex: self.OnButton(ButtonIndex))
			Button.grid(row = FieldIndex + 1, column = 0, sticky = W+E)
			self.ButtonList.append(Button)

		# Get window focus
		self.focus_force()

		# Centre window on screen
		CentreTkOnScreen(self)

		# Start main loop
		self.mainloop()

	def OnButton(self, ButtonIndex = None):

		self.RetVal = [1, self.ButtonList[ButtonIndex].cget('text')]
		self.destroy()

	def OnClose(self):

		self.RetVal = [0, "User closed window"]
		self.destroy()

class SettingsTk(tkinter.Tk):

	def __init__(self):
	
		# instantiate parent class first
		tkinter.Tk.__init__(self)
		
		# set McLaren logo as icon
		self.iconbitmap(r'mclaren_logo.ico')		

		# custom attributes
		self.RetVal	= None	
		
		# give window a title
		self.title('Settings')
		
		# we don't want the window to be resizable
		self.resizable(False, False)

		# register on close callback
		self.protocol("WM_DELETE_WINDOW", self.OnClose)	

		# create main frame
		self.MainFrame = tkFrame(self)
		self.MainFrame.grid(row = 0, column = 0)
		
		# create text frame
		self.TextLabel = tkLabel(self.MainFrame, text = "Please configure the generator settings:", font = DefaultFontString)
		self.TextLabel.grid(row = 0, column = 0, sticky = W+E)
		
		# create OdbBom check button
		self.OdbBomCbVar = tkIntVar()
		self.OdbBomCb = tkCheckbutton(self.MainFrame, text = "1. Extract information from ODB++ data and BoM", variable = self.OdbBomCbVar, font = MinorFontString, command = self.OnOdbBomCb)
		self.OdbBomCb.grid(row = 1, column = 0, sticky = W)
		self.OdbBomCbVar.set(True)
		
		# create FptParser check button
		self.FptParserCbVar = tkIntVar()
		self.FptParserCb = tkCheckbutton(self.MainFrame, text = "2a. Extract test information from FPT report", variable = self.FptParserCbVar, font = MinorFontString, command = self.OnFptParserCb)
		self.FptParserCb.grid(row = 2, column = 0, sticky = W)
		self.FptParserCbVar.set(True)

		# create FptConverter check button
		self.FptConverterCbVar = tkIntVar()
		self.FptConverterCb = tkCheckbutton(self.MainFrame, text = "2b. Convert FPT test information to PCOLA/SOQ", variable = self.FptConverterCbVar, font = MinorFontString, command = self.OnFptConverterCb)
		self.FptConverterCb.grid(row = 3, column = 0, sticky = W)
		self.FptConverterCbVar.set(True)

		# create BstConverter check button
		self.BstConverterCbVar = tkIntVar()
		self.BstConverterCb = tkCheckbutton(self.MainFrame, text = "3. Extract BST PCOLA/SOQ information", variable = self.BstConverterCbVar, font = MinorFontString, command = self.OnBstConverterCb)
		self.BstConverterCb.grid(row = 4, column = 0, sticky = W)
		self.BstConverterCbVar.set(True)
		
		# create AoiConverter check button
		self.AoiConverterCbVar = tkIntVar()
		self.AoiConverterCb = tkCheckbutton(self.MainFrame, text = "4. Convert AOI test information to PCOLA/SOQ", variable = self.AoiConverterCbVar, font = MinorFontString, command = self.OnAoiConverterCb)
		self.AoiConverterCb.grid(row = 5, column = 0, sticky = W)
		self.AoiConverterCbVar.set(True)		

		# create ComputeCb check button
		self.ComputeCbVar = tkIntVar()
		self.ComputeCb = tkCheckbutton(self.MainFrame, text = "5. Generate final PCOLA/SOQ information", variable = self.ComputeCbVar, font = MinorFontString, command = self.OnComputeCb)
		self.ComputeCb.grid(row = 6, column = 0, sticky = W)
		self.ComputeCbVar.set(True)

		# create ReportCb check button
		self.ReportCbVar = tkIntVar()
		self.ReportCb = tkCheckbutton(self.MainFrame, text = "6. Generate Excel PCOLA/SOQ report", variable = self.ReportCbVar, font = MinorFontString, command = self.OnReportCb)
		self.ReportCb.grid(row = 7, column = 0, sticky = W)	
		self.ReportCbVar.set(True)
		
		# create OK Button		
		OkButton = tkButton(self.MainFrame, text = "OK", font = DefaultBoldFontString, command = self.OnOkButton)
		OkButton.grid(row = 8, column = 0, sticky = W+E)

		# Pressing return selects the OK button
		#
		self.bind('<Return>', self.OnOkButton)		
		
		# Get window focus
		self.focus_force()

		# Centre window on screen
		CentreTkOnScreen(self)

		# Start main loop
		self.mainloop()

	def OnOdbBomCb(self):
		pass
		
	def OnFptParserCb(self):
		pass
		
	def OnFptConverterCb(self):
		pass
		
	def OnBstConverterCb(self):
		pass

	def OnAoiConverterCb(self):
		pass		
		
	def OnComputeCb(self):
		pass
		
	def OnReportCb(self):
		pass
	
	def OnOkButton(self, ButtonIndex = None):

		self.RetVal = [1, 'OK']
		self.destroy()	
	
	def OnClose(self):

		self.RetVal = [0, "User closed window"]
		self.destroy()
