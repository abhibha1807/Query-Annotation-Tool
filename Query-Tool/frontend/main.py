from tkinter import *
import tkinter as tk
from tkinter import Frame, Menu
from tkinter import ttk 
from tkinter import filedialog
from tkinter.filedialog import asksaveasfilename
from dummy import get_query,export_as,create_dict,ent_dict,create_mulents,create_muldict,clear_dicts
from dummy import MUL_ENTS,getOptions,getInstruct,export_as_search
import os
from os import listdir
from os.path import isfile, join

def truncate(n):
	return int(n * 100) / 100

IP_DATASET=''
RESULTS=''

# main class that handles tabs 
class TabControl(tk.Frame):
	def __init__(self, master):
		tk.Frame.__init__(self, master) 
		tabControl = ttk.Notebook(self)
		tab1 =ImportTab(tabControl)
		tab2=AnnotationTool(tabControl)
		tab3=SearchTool(tabControl)
		tabControl.add(tab1, text ='Import Files') 
		tabControl.add(tab2, text ='Annotation Tool')
		tabControl.add(tab3, text='Search Tool')
		
		def tab_switch(event):
			if event.widget.identify(event.x, event.y) == "label":
				index = event.widget.index("@%d,%d" % (event.x, event.y))
				title = event.widget.tab(index, "text")

				if title == 'Import Files':
					tab1.update()
				elif title == 'Search Tool':
					tab3.update()
				elif title == 'Annotation Tool':
					tab2.update()

		tabControl.bind("<Button-1>", tab_switch)
		tabControl.bind("<Button-2>", tab_switch)
		tabControl.bind("<Button-3>", tab_switch)
		tabControl.pack(fill="both", expand=True)
		


class AnnotationTool(tk.Frame):
	def __init__(self, master):
		tk.Frame.__init__(self, master) 
		self.section='' #stores the selected section
		self.checks={} #stores the relational entities checked h
		tk.Label(self,text = "Entity",font =("Courier", 20)).grid(column=2,row=1,padx=5)
		tk.Button(self, text="Export",command=lambda: self.ExportAction()).grid(column=5,row=1,padx=20,sticky='E')

		#defining key,entity,checkbox 
		tk.Label(self,text = "A",font =("Courier", 20)).grid(column=1,row=2,padx=2)
		self.tagA='INGREDIENT'
		self.keyA='a'
		self.textA=tk.Text(self)
		self.textA.config(height=1,width=20,wrap='word')
		self.textA.grid(column=2,padx=10,row=2)
		self.textA.insert('insert','INGREDIENT')
		self.varA = IntVar()
		Checkbutton(self, variable=self.varA).grid(row=2,column=3)

		#tag for relational tagging 
		self.tagS='pair'

		tk.Label(self,text = "B",font =("Courier", 20)).grid(column=1,row=3,padx=2)
		self.tagB='PROCESS'
		self.keyB='b'
		self.textB=tk.Text(self)
		self.textB.config(height=1,width=20,wrap='word')
		self.textB.grid(column=2,padx=10,row=3,pady=3)
		self.textB.insert('insert','PROCESS')
		self.varB = IntVar()
		Checkbutton(self, variable=self.varB).grid(row=3,column=3,pady=3)

		tk.Label(self,text = "C",font =("Courier", 20)).grid(column=1,row=4,padx=2)
		self.tagC='QUANTITY'
		self.keyC='c'
		self.textC=tk.Text(self)
		self.textC.config(height=1,width=20,wrap='word')
		self.textC.grid(column=2,padx=10,row=4,pady=3)
		self.textC.insert('insert','QUANTITY')
		self.varC = IntVar()
		Checkbutton(self, variable=self.varC).grid(row=4,column=3,pady=3)

		tk.Label(self,text = "D",font =("Courier", 20)).grid(column=1,row=5,padx=2)
		self.tagD='CONDITIONS'
		self.keyD='d'
		self.textD=tk.Text(self)
		self.textD.config(height=1,width=20,wrap='word')
		self.textD.grid(column=2,padx=10,row=5,pady=3)
		self.textD.insert('insert','CONDITIONS')
		self.varD = IntVar()
		Checkbutton(self, variable=self.varD).grid(row=5, sticky=E,column=3,pady=3)
	
		tk.Label(self,text = "E",font =("Courier", 20)).grid(column=1,row=6,padx=2)
		self.tagE='SUBSTRATE'
		self.keyE='e'
		self.textE=tk.Text(self)
		self.textE.config(height=1,width=20,wrap='word')
		self.textE.grid(column=2,padx=10,row=6,pady=3)
		self.textE.insert('insert','SUBSTRATE')
		self.varE = IntVar()
		Checkbutton(self, variable=self.varE).grid(row=6,column=3,pady=3)

		tk.Label(self,text = "F",font =("Courier", 20)).grid(column=1,row=7,padx=2)
		self.tagF='EQUIPMENT'
		self.keyF='f'
		self.textF=tk.Text(self)
		self.textF.config(height=1,width=20,wrap='word')
		self.textF.grid(column=2,padx=10,row=7,pady=3)
		self.textF.insert('insert','EQUIPMENT')
		self.varF = IntVar()
		Checkbutton(self, variable=self.varF).grid(row=7,column=3,pady=3)

		tk.Label(self,text = "G",font =("Courier", 20)).grid(column=1,row=8,padx=2)
		self.tagG='COATING_PROCESS'
		self.keyG='g'
		self.textG=tk.Text(self)
		self.textG.config(height=1,width=20,wrap='word')
		self.textG.grid(column=2,padx=10,row=8,pady=3)
		self.textG.insert('insert','COATING_PROCESS')
		self.varG = IntVar()
		Checkbutton(self, variable=self.varG).grid(row=8,column=3,pady=3)

		tk.Label(self,text = "H",font =("Courier", 20)).grid(column=1,row=9,padx=2)
		self.tagH='COATING_TYPE'
		self.keyH='h'
		self.textH=tk.Text(self)
		self.textH.config(height=1,width=20,wrap='word')
		self.textH.grid(column=2,padx=10,row=9,pady=3)
		self.textH.insert('insert','COATING_TYPE')
		self.varH = IntVar()
		Checkbutton(self, variable=self.varH).grid(row=9,column=3,pady=3)

		tk.Label(self,text = "I",font =("Courier", 20)).grid(column=1,row=10,padx=2)
		self.tagI='INGREDIENT_FUNCTION'
		self.keyI='i'
		self.textI=tk.Text(self)
		self.textI.config(height=1,width=20,wrap='word')
		self.textI.grid(column=2,padx=10,row=10,pady=3)
		self.textI.insert('insert','INGREDIENT_FUNCTION')
		self.varI = IntVar()
		Checkbutton(self, variable=self.varI).grid(row=10,column=3,pady=3)

		tk.Label(self,text = "J",font =("Courier", 20)).grid(column=1,row=11,padx=2)
		self.tagJ='COATING_FUNCTION'
		self.keyJ='j'
		self.textJ=tk.Text(self)
		self.textJ.config(height=1,width=20,wrap='word')
		self.textJ.grid(column=2,padx=10,row=11,pady=3)
		self.textJ.insert('insert','COATING_FUNCTION')
		self.varJ = IntVar()
		Checkbutton(self, variable=self.varJ).grid(row=11,column=3,pady=3)

		tk.Label(self,text = "K",font =("Courier", 20)).grid(column=1,row=12,padx=2)
		self.tagK='COATING_ANALYSIS_TECHNIQUE'
		self.keyK='k'
		self.textK=tk.Text(self)
		self.textK.config(height=1,width=20,wrap='word')
		self.textK.grid(column=2,padx=10,row=12,pady=3)
		self.textK.insert('insert','COATING_ANALYSIS_TECHNIQUE')
		self.varK = IntVar()
		Checkbutton(self, variable=self.varK).grid(row=12,column=3,pady=3)

		tk.Label(self,text = "L",font =("Courier", 20)).grid(column=1,row=13,padx=2)
		self.tagL='ACTIONS'
		self.keyL='l'
		self.textL=tk.Text(self)
		self.textL.config(height=1,width=20,wrap='word')
		self.textL.grid(column=2,padx=10,row=13,pady=3)
		self.textL.insert('insert','ACTIONS')
		self.varL = IntVar()
		Checkbutton(self, variable=self.varL).grid(row=13,column=3,pady=3)



		self.query_field = Text(self)
		self.query_field.config(height=2,spacing1=5,yscrollcommand=True,wrap='word',undo=True)
		self.query_field.grid(pady=10,column=4,row=2,padx=10)
		self.query_field.insert('insert','INGREDIENT:word=steel')

		self.results_field = Text(self)
		self.results_field.config(height=20,spacing1=5,yscrollcommand=True,wrap='word',undo=True)
		self.results_field.grid(pady=10,column=4,row=3,padx=10,rowspan=12)

		tkvar = StringVar(self)

		self.instruct = Text(self)
		self.instruct.config(height=20,spacing1=5,yscrollcommand=True,wrap='word',width=40)
		self.instruct.grid(pady=10,column=5,row=3,padx=10,rowspan=12)
		self.instruct.insert('insert',getInstruct('annotation_instruct.txt'))

		tk.Button(self, text="Query",command=lambda: self.query()).grid(column=4,row=15,pady=10,sticky='W',padx=20)
		tk.Button(self, text="Clear",command=lambda: self.clear_results_field()).grid(column=4,row=15,sticky='E',padx=20,pady=10)
	
			
		self.tagging_mode = IntVar()
		self.R1 = Radiobutton(self, text="Related entity tagging", variable=self.tagging_mode, value=1,command=self.enable_annotation)
		self.R1.grid(row=15,column=2,pady=5)

		self.R2 = Radiobutton(self, text="Entity tagging", variable=self.tagging_mode, value=2)
		self.R2.grid(row=16,column=2)

		self.results_field.focus() 
		self.results_field.tag_configure(self.tagA, background="yellow")
		self.results_field.tag_configure(self.tagB, background="green")
		self.results_field.tag_configure(self.tagC, background="pink")
		self.results_field.tag_configure(self.tagD, background="light green")
		self.results_field.tag_configure(self.tagE, background="light blue")
		self.results_field.tag_configure(self.tagF, background="orange")
		self.results_field.tag_configure(self.tagG, background="grey")
		self.results_field.tag_configure(self.tagH, background="blue")
		self.results_field.tag_configure(self.tagI, background="purple")
		self.results_field.tag_configure(self.tagJ, background="brown")
		self.results_field.tag_configure(self.tagK, background="cyan")
		self.results_field.tag_configure(self.tagL, background="MediumPurple")
		self.results_field.tag_configure(self.tagS, background="red")
	
		
		self.results_field.bind(self.keyA, self.onKeyPressA)	
		self.results_field.bind(self.keyB, self.onKeyPressB)	
		self.results_field.bind(self.keyC, self.onKeyPressC)	
		self.results_field.bind(self.keyD, self.onKeyPressD)	
		self.results_field.bind(self.keyE, self.onKeyPressE)
		self.results_field.bind(self.keyF, self.onKeyPressF)
		self.results_field.bind(self.keyG, self.onKeyPressG)	
		self.results_field.bind(self.keyH, self.onKeyPressH)
		self.results_field.bind(self.keyI, self.onKeyPressI)
		self.results_field.bind(self.keyJ, self.onKeyPressJ)
		self.results_field.bind(self.keyK, self.onKeyPressK)
		self.results_field.bind(self.keyL, self.onKeyPressL)
		self.results_field.bind('x', self.onKeyPressX)
		
		self.results_field.tag_raise("sel")
		self.name = 'annotation tab'
	
	#sections menu
	def update(self):
		print ("Updating %s" % self.name)
		print('creating menu')
		choices=getOptions(IP_DATASET)
		tkvar = StringVar(self)
		tkvar.set(list(choices)[0]) 
		popupMenu = OptionMenu(self, tkvar, *choices)
		popupMenu.grid(row = 2, column =5,sticky='W')

		def change_dropdown(*args):
			self.section=tkvar.get()
			print('section:',tkvar.get())

		tkvar.trace('w', change_dropdown)

	


	def query(self):
		print('querying....')
		if self.results_field.get("1.0",'end-1c')!='':
			self.results_field.delete('1.0', END)
		
		inputt = self.query_field.get("1.0",'end-1c')
		inputt=(re.split(r"\s(?=\w+:)|:",inputt))
		for i in range(0,len(inputt),2):
			tag=inputt[i]
			if inputt!='' and self.section!='' :
				global RESULTS
				countVar = StringVar()
				RESULTS=get_query(inputt[i+1],IP_DATASET,self.section)
				self.results_field.insert('insert',RESULTS)
				pos1 = 1.0
				pos2=1.0
				start=1.0
				while 1:
					countVar = StringVar()
					pos1 = self.results_field.search('<WORD>', pos1, stopindex=END, count=countVar, regexp=True)
					pos2 = self.results_field.search('</WORD>', pos2, stopindex=END, count=countVar, regexp=True)
					if pos1=='':
						break
					self.results_field.tag_add(tag, pos1+'+6c', pos2)
					create_dict(tag,self.results_field.get(pos1+'+6c',pos2),(pos1),(str(truncate(float(pos2)-0.06))))
					self.results_field.delete(pos1,pos1+'+6c')
					self.results_field.delete(pos2+'-6c',pos2+'+1c')
					self.results_field.insert(pos2+'-6c',' ')
					pos1 = pos1+"+1c"
					pos2 = pos2+"+1c"
				

	def ExportAction(self):
		global RESULTS
		export_as(self.tagging_mode.get(),self.query_field.get("1.0",'end-1c'))


	def onKeyPressA(self,event):
		if  self.tagging_mode.get()==2:
			self.results_field.tag_add(self.tagA, 'sel.first', 'sel.last')
			start=(self.results_field.index('sel.first'))
			end=(self.results_field.index('sel.last'))
			create_dict(self.textA.get("1.0",'end-1c'),self.results_field.get(start,end),start,end,add=1)
			return "break"
		else: 
			self.results_field.tag_add(self.tagS, 'sel.first', 'sel.last')
			start=(self.results_field.index('sel.first'))
			end=(self.results_field.index('sel.last'))
			create_muldict(self.textA.get("1.0",'end-1c'),self.results_field.get(start,end),start,end)
			return "break"

	def onKeyPressB(self,event):
		if self.tagging_mode.get()==2:
			self.results_field.tag_add(self.tagB, 'sel.first', 'sel.last')
			start=self.results_field.index('sel.first')
			end=self.results_field.index('sel.last')
			create_dict(self.textB.get("1.0",'end-1c'),self.results_field.get(start,end),start,end,add=1)
			return "break"
		else:
			self.results_field.tag_add(self.tagS, 'sel.first', 'sel.last')
			start=self.results_field.index('sel.first')
			end=self.results_field.index('sel.last')
			create_muldict(self.textB.get("1.0",'end-1c'),self.results_field.get(start,end),start,end)
			return "break"

	def onKeyPressC(self,event):
		if self.tagging_mode.get()==2:
			self.results_field.tag_add(self.tagC, 'sel.first', 'sel.last')
			start=self.results_field.index('sel.first')
			end=self.results_field.index('sel.last')
			create_dict(self.textC.get("1.0",'end-1c'),self.results_field.get(start,end),start,end,add=1)
			return "break"
		else: 
			self.results_field.tag_add(self.tagS, 'sel.first', 'sel.last')
			start=self.results_field.index('sel.first')
			end=self.results_field.index('sel.last')
			create_muldict(self.textC.get("1.0",'end-1c'),self.results_field.get(start,end),start,end)
			return "break"

	def onKeyPressD(self,event):
		if self.tagging_mode.get()==2:
			self.results_field.tag_add(self.tagD, 'sel.first', 'sel.last')
			start=self.results_field.index('sel.first')
			end=self.results_field.index('sel.last')
			create_dict(self.textD.get("1.0",'end-1c'),self.results_field.get(start,end),start,end,add=1)
			return "break"
		else: 
			self.results_field.tag_add(self.tagS, 'sel.first', 'sel.last')
			start=self.results_field.index('sel.first')
			end=self.results_field.index('sel.last')
			create_muldict(self.textD.get("1.0",'end-1c'),self.results_field.get(start,end),start,end)
			return "break"

	def onKeyPressE(self,event):
		if self.tagging_mode.get()==2:
			self.results_field.tag_add(self.tagE, 'sel.first', 'sel.last')
			start=self.results_field.index('sel.first')
			end=self.results_field.index('sel.last')
			create_dict(self.textE.get("1.0",'end-1c'),self.results_field.get(start,end),start,end,add=1)
			return "break"
		else: 
			self.results_field.tag_add(self.tagS, 'sel.first', 'sel.last')
			start=self.results_field.index('sel.first')
			end=self.results_field.index('sel.last')
			create_muldict(self.textE.get("1.0",'end-1c'),self.results_field.get(start,end),start,end)
			return "break"

	def onKeyPressF(self,event):
		if self.tagging_mode.get()==2:
			self.results_field.tag_add(self.tagF, 'sel.first', 'sel.last')
			start=self.results_field.index('sel.first')
			end=self.results_field.index('sel.last')
			create_dict(self.textF.get("1.0",'end-1c'),self.results_field.get(start,end),start,end,add=1)
			return "break"
		else: 
			self.results_field.tag_add(self.tagS, 'sel.first', 'sel.last')
			start=self.results_field.index('sel.first')
			end=self.results_field.index('sel.last')
			create_muldict(self.textF.get("1.0",'end-1c'),self.results_field.get(start,end),start,end)
			return "break"

	def onKeyPressG(self,event):
		if self.tagging_mode.get()==2:
			self.results_field.tag_add(self.tagG, 'sel.first', 'sel.last')
			start=self.results_field.index('sel.first')
			end=self.results_field.index('sel.last')
			create_dict(self.textG.get("1.0",'end-1c'),self.results_field.get(start,end),start,end,add=1)
			return "break"
		else: 
			self.results_field.tag_add(self.tagS, 'sel.first', 'sel.last')
			start=self.results_field.index('sel.first')
			end=self.results_field.index('sel.last')
			create_muldict(self.textG.get("1.0",'end-1c'),self.results_field.get(start,end),start,end)
			return "break"

	def onKeyPressH(self,event):
		if self.tagging_mode.get()==2:
			self.results_field.tag_add(self.tagH, 'sel.first', 'sel.last')
			start=self.results_field.index('sel.first')
			end=self.results_field.index('sel.last')
			create_dict(self.textH.get("1.0",'end-1c'),self.results_field.get(start,end),start,end,add=1)
			return "break"
		else: 
			self.results_field.tag_add(self.tagS, 'sel.first', 'sel.last')
			start=self.results_field.index('sel.first')
			end=self.results_field.index('sel.last')
			create_muldict(self.textH.get("1.0",'end-1c'),self.results_field.get(start,end),start,end)
			return "break"

	def onKeyPressI(self,event):
		if self.tagging_mode.get()==2:
			self.results_field.tag_add(self.tagI, 'sel.first', 'sel.last')
			start=self.results_field.index('sel.first')
			end=self.results_field.index('sel.last')
			create_dict(self.textI.get("1.0",'end-1c'),self.results_field.get(start,end),start,end,add=1)
			return "break"
		else: 
			self.results_field.tag_add(self.tagS, 'sel.first', 'sel.last')
			start=self.results_field.index('sel.first')
			end=self.results_field.index('sel.last')
			create_muldict(self.textI.get("1.0",'end-1c'),self.results_field.get(start,end),start,end)
			return "break"

	def onKeyPressJ(self,event):
		if self.tagging_mode.get()==2:
			self.results_field.tag_add(self.tagJ, 'sel.first', 'sel.last')
			start=self.results_field.index('sel.first')
			end=self.results_field.index('sel.last')
			create_dict(self.textJ.get("1.0",'end-1c'),self.results_field.get(start,end),start,end,add=1)
			return "break"
		else: 
			self.resultsc
	def onKeyPressK(self,event):
		if self.tagging_mode.get()==2:
			self.results_field.tag_add(self.tagK, 'sel.first', 'sel.last')
			start=self.results_field.index('sel.first')
			end=self.results_field.index('sel.last')
			create_dict(self.textK.get("1.0",'end-1c'),self.results_field.get(start,end),start,end,add=1)
			return "break"
		else: 
			self.results_field.tag_add(self.tagS, 'sel.first', 'sel.last')
			start=self.results_field.index('sel.first')
			end=self.results_field.index('sel.last')
			create_muldict(self.textK.get("1.0",'end-1c'),self.results_field.get(start,end),start,end)
			return "break"

	def onKeyPressL(self,event):
		if self.tagging_mode.get()==2:
			self.results_field.tag_add(self.tagL, 'sel.first', 'sel.last')
			start=(self.results_field.index('sel.first'))
			end=(self.results_field.index('sel.last'))
			create_dict(self.textL.get("1.0",'end-1c'),self.results_field.get(start,end),start,end,add=1)
			return "break"
		else: 
			self.results_field.tag_add(self.tagS, 'sel.first', 'sel.last')
			start=(self.results_field.index('sel.first'))
			end=(self.results_field.index('sel.last'))
			create_muldict(self.textL.get("1.0",'end-1c'),self.results_field.get(start,end),start,end)
			return "break"


	def onKeyPressX(self,event):
		print('removing selection!')
		sel_start=float(self.results_field.index('sel.first'))
		sel_end=float(self.results_field.index('sel.last'))

		if self.tagging_mode.get()==2:
			for k in ent_dict.keys():
				for l in ent_dict[k]:
					if (sel_start)>=float(l[0])-0.2 and (sel_start)<=float(l[0])+0.2 and (sel_end)>=float(l[1])-0.2 and (sel_end)<=float(l[1])+0.2:
						ent_dict[k].remove(l)
						self.results_field.tag_remove(k, tk.SEL_FIRST, tk.SEL_LAST)
		else:
			for k in MUL_ENTS.keys():
				for l in MUL_ENTS[k]:
					if (sel_start)>=float(l[0])-0.2 and (sel_start)<=float(l[0])+0.2 and (sel_end)>=float(l[1])-0.2 and (sel_end)<=float(l[1])+0.2:
						MUL_ENTS[k].remove(l)
						self.results_field.tag_remove(self.tagS, tk.SEL_FIRST, tk.SEL_LAST)
		print('removed')
		return "break"


	def enable_annotation(self):
		self.checks[self.tagA]=self.varA.get()
		self.checks[self.tagB]=self.varB.get()
		self.checks[self.tagC]=self.varC.get()
		self.checks[self.tagD]=self.varD.get()
		self.checks[self.tagE]=self.varE.get()
		self.checks[self.tagF]=self.varF.get()
		self.checks[self.tagG]=self.varG.get()
		self.checks[self.tagH]=self.varH.get()
		self.checks[self.tagI]=self.varI.get()
		self.checks[self.tagJ]=self.varJ.get()
		self.checks[self.tagK]=self.varK.get()
		self.checks[self.tagL]=self.varL.get()
		for k in self.checks.keys():
			if self.checks[k]==1:
				create_mulents(k)
	
	def clear_results_field(self):
		clear_dicts()
		self.results_field.delete('1.0', END)




class ImportTab(tk.Frame):
	def __init__(self, master):
		tk.Frame.__init__(self, master) 
		tk.Button(self, text="Import File",command=lambda: self.UploadActionFile()).grid(column=1,row=1,padx=20,pady=20)
		tk.Button(self, text="Import Folder",command=lambda: self.UploadActionFolder()).grid(column=2,row=1,padx=20,pady=20)
		self.instruct=Text(self)
		self.instruct.config(height=12,spacing1=5,yscrollcommand=True,wrap='word')
		self.instruct.grid(pady=10,column=1,row=2,padx=20,columnspan=2)
		self.instruct.insert('insert',getInstruct('import_instruct.txt'))
		self.name = 'import tab'
	
	# def update(self):
	# # Update the contents of the frame...
	# 	print ("Updating %s" % self.name)



	def UploadActionFile(self,event=None):
		filename = filedialog.askopenfilename()
		global IP_DATASET
		IP_DATASET=filename

	def UploadActionFolder(self,event=None):
		directory = filedialog.askdirectory()
		print(directory)
		global IP_DATASET
		IP_DATASET=directory
	


class SearchTool(tk.Frame):
	def __init__(self, master):
		tk.Frame.__init__(self, master) 
		self.results=[] #captures non capture group results
		self.results_dict={} #captures capture group results
		self.section='' #captures section
		self.type=0 #to set the type of query 0=non capture group 1=capture group. 
		self.query_field = Text(self)
		self.query_field.config(height=2,spacing1=5,yscrollcommand=True,wrap='word')
		self.query_field.grid(pady=10,column=1,row=1,padx=10)
		#self.query_field.insert('insert','stainless,steel')

		self.results_field = Text(self)
		self.results_field.config(height=25,spacing1=5,yscrollcommand=True,wrap='word',undo=True)
		self.results_field.grid(pady=10,column=1,row=2,padx=5)
		self.results_field.tag_configure('result', background="yellow")

		tk.Button(self, text="Query",command=lambda: self.query()).grid(column=1,row=3,pady=5,sticky='W')
		tk.Button(self, text="Clear",command=lambda: self.clear_results_field()).grid(column=1,row=3,pady=5,sticky='E')
		tk.Button(self, text="Export",command=lambda: self.ExportAction()).grid(column=2,row=1,pady=5,sticky='E')
		self.name = 'search tab'
		self.instruct = Text(self)
		self.instruct.config(height=25,spacing1=5,yscrollcommand=True,wrap='word',width=40)
		self.instruct.grid(pady=10,column=2,row=2,padx=5)
		self.instruct.insert('insert',getInstruct('search_instruct.txt'))
	
	def update(self):
		print ("Updating %s" % self.name)
		print('creating menu')
		tkvar = StringVar(self)
		choices={'abstract', 'introduction', 'experiment','results', 'conclusion', 'references'}
		tkvar.set(list(choices)[0])
		popupMenu = OptionMenu(self, tkvar, *choices)
		popupMenu.grid(row = 1, column =2,sticky='W')

		def change_dropdown(*args):
			self.section=tkvar.get()
			print(tkvar.get())

		tkvar.trace('w', change_dropdown)

	def query(self):
		print('querying....')
		if self.results_field.get("1.0",'end-1c')!='':
			self.results_field.delete('1.0', END)
		inputt = self.query_field.get("1.0",'end-1c')
		self.type=0
		global IP_DATASET
		#/Users/abhibhagupta/Desktop/TCS/NER/coatings/Section_wise_text/coatings_0003.txt
		if '.txt' not in IP_DATASET:
			onlyfiles = [f for f in listdir(IP_DATASET) if isfile(join(IP_DATASET, f))]
		if ':' not in inputt:
			for f in range(len(onlyfiles)):
				if inputt!='' and self.section!='':
					countVar = StringVar()
					res=get_query(inputt,IP_DATASET+'/'+onlyfiles[f],self.section)
					if res!='':
						self.results_field.insert('insert',onlyfiles[f]+'\n'+res+'\n\n')
						pos1 = 1.0
						pos2=1.0
						start=1.0
						while 1:
							countVar = StringVar()
							pos1 = self.results_field.search('<WORD>', pos1, stopindex=END, count=countVar, regexp=True)
							pos2 = self.results_field.search('</WORD>', pos2, stopindex=END, count=countVar, regexp=True)
							if pos1=='':
								break
							self.results_field.tag_add('result', pos1+'+6c', pos2)
							self.results.append(self.results_field.get(pos1+'+6c',pos2))
							self.results_field.delete(pos1,pos1+'+6c')
							self.results_field.delete(pos2+'-6c',pos2+'+1c')
							self.results_field.insert(pos2+'-6c',' ')
							pos1 = pos1+"+1c"
							pos2 = pos2+"+1c"
		else:
			self.type=1
			inputt=re.split(r"\s(?=\w+:)|:",inputt)
			for f in range(len(onlyfiles)):
				if self.section!='':
					for i in range(0,len(inputt),2):
						tag=inputt[i]	
						countVar = StringVar()
						res=get_query(inputt[i+1],IP_DATASET+'/'+onlyfiles[f],self.section)
						if res!='':
							self.results_field.insert('insert',onlyfiles[f]+'\n'+res+'\n\n')
							pos1 = 1.0
							pos2=1.0
							start=1.0
							while 1:
								countVar = StringVar()
								pos1 = self.results_field.search('<WORD>', pos1, stopindex=END, count=countVar, regexp=True)
								pos2 = self.results_field.search('</WORD>', pos2, stopindex=END, count=countVar, regexp=True)
								if pos1=='':
									break
								self.results_field.tag_add('result', pos1+'+6c', pos2)
								try:
									self.results_dict[tag].append([(pos1),(str(truncate(float(pos2)-0.06))),self.results_field.get(pos1+'+6c',pos2)])
								except:
									self.results_dict[tag]=[]
									self.results_dict[tag].append([(pos1),(str(truncate(float(pos2)-0.06))),self.results_field.get(pos1+'+6c',pos2)])

								self.results_field.delete(pos1,pos1+'+6c')
								self.results_field.delete(pos2+'-6c',pos2+'+1c')
								self.results_field.insert(pos2+'-6c',' ')
								pos1 = pos1+"+1c"
								pos2 = pos2+"+1c"
	

	def ExportAction(self):
		if self.type==0:
			export_as_search(self.results)
		else:
			export_as_search(self.results_dict)
		self.type=0

	def clear_results_field(self):
		if self.type==0:
			self.results=[]
		else:
			self.results_dict={}
		self.results_field.delete('1.0', END)
		self.type=0


class App(tk.Tk):
	def __init__(self):
		tk.Tk.__init__(self)
		self._frame = None
		self.switch_frame(TabControl)
		self.title('Annotation cum Search Tool')

	def switch_frame(self, frame_class):
		new_frame = frame_class(self)
		if self._frame is not None:
			self._frame.pack_forget()
		self._frame = new_frame
		self._frame.pack()

	

def main():
	app=App()
	app.geometry("1300x1000") 
	app.mainloop()

if __name__ == '__main__':
	main()
