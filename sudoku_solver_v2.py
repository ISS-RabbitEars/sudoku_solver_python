#!/usr/bin/env python3.9
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox

def transpose(a):
	b=[]
	for i in range(9):
		temp=[]
		for j in range(9):
			temp.append(0)
		b.append(temp)
	for i in range(9):
		for j in range(9):
			b[j][i]=a[i][j]
	return b

def partition(a):
	b=[]
	for i in range(9):
		temp=[]
		for j in range(9):
			temp.append(0)
		b.append(temp)	
	m=0
	for i in (0,3,6):
		for j in (0,3,6):
			n=0
			for k in range(3):
				for l in range(3):
					b[i+k][j+l]=a[m][n]
					n+=1
			m+=1
	return b

def init_notes():
	a=[]
	for i in range(9):
		temp=[]
		for j in range(9):
			temp.append(0)
		a.append(temp)
	return a

def reduce(x):
	fs=[]
	for i in range(9): fs.append(i+1)
	sa_temp=[]
	while sa_temp != x:
		y=init_notes()
		sa_temp=x
		for i in range(9):
			for j in range(9):
				if x[i][j]==0:
					sa_transpose=transpose(x)
					sa_boxes=partition(x)
					m=i//3
					n=j//3
					temp=set(sorted(sa_boxes[m*3+n]))
					y[i][j]=list(set(fs)-(set(sorted(x[i]))|set(sorted(sa_transpose[j]))|temp))
					if len(y[i][j])==1:
						x[i][j]=y[i][j][0]
						y[i][j]=[]
						x,y=reduce(x)
						x,y=locked_pair_row(x,y)
						x,y=locked_pair_column(x,y)
						x,y=locked_pair_box(x,y)
	return x,y

def hidden_singles_row(x,y):
	for i in range(9):
		for j in range(9):
			if x[i][j]==0:
				temp=set()
				for k in range(9):
					if k!=j and x[i][k]==0:
						temp=set(sorted(y[i][k]))|temp
				temp=list(set(sorted(y[i][j]))-temp)
				if len(temp)==1:
					x[i][j]=temp[0]
					x,y=reduce(x)
	return x,y 

def hidden_singles_column(x,y):
	for i in range(9):
		for j in range(9):
			if x[i][j]==0:
				temp=set()
				for k in range(9):
					if k!=i and x[k][j]==0:
						temp=set(sorted(y[k][j]))|temp
				temp=list(set(sorted(y[i][j]))-temp)
				if len(temp)==1:
					x[i][j]=temp[0]
					x,y=reduce(x)
	return x,y

def hidden_singles_box(x,y):
	for i in (0,3,6):
		for j in (0,3,6):
			for k in range(3):
				for l in range(3):
					ii=i+k
					jj=j+l
					if x[ii][jj]==0:
						temp=set()
						for m in range(3):
							for n in range(3):
								mm=i+m
								nn=j+n
								if not(mm==ii and nn==jj) and x[mm][nn]==0:
									temp=set(sorted(y[mm][nn]))|temp
						temp=list(set(sorted(y[ii][jj]))-temp)
						if len(temp)==1:
							x[ii][jj]=temp[0]
							x,y=reduce(x)
	return x,y

def locked_pair_row(x,y):
	for i in range(9):
		for j in range(9):
			if x[i][j]==0 and len(y[i][j])==2:
				for k in range(9):
					if k!=j and x[i][k]==0 and len(y[i][k])==2 and sorted(y[i][j])==sorted(y[i][k]):
						for l in range(9):
							if l!=j and l!=k and x[i][l]==0:
								y[i][l]=list(set(sorted(y[i][l]))-set(sorted(y[i][k])))
								if len(y[i][l])==1:
									x[i][l]=y[i][l][0]
									y[i][l]=[]
	return x,y

def locked_pair_column(x,y):
	for i in range(9):
		for j in range(9):
			if x[i][j]==0 and len(y[i][j])==2:
				for k in range(9):
					if k!=i and x[k][j]==0 and len(y[k][j])==2 and sorted(y[i][j])==sorted(y[k][j]):
						for l in range(9):
							if l!=i and l!=k and x[l][j]==0:
								y[l][j]=list(set(sorted(y[l][j]))-set(sorted(y[k][j])))
								if len(y[l][j])==1:
									x[l][j]=y[l][j][0]
									y[l][j]=[]
	return x,y

def locked_pair_box(x,y):
	for i in (0,3,6):
		for j in (0,3,6):
			for k in range(3):
				for l in range(3):
					ii=i+k
					jj=j+l
					if x[ii][jj]==0 and len(y[ii][jj])==2:
						for m in range(3):
							for n in range(3):
								mm=i+m
								nn=j+n
								if not(mm==ii and nn==jj) and x[mm][nn]==0 and len(y[mm][nn])==2 and sorted(y[ii][jj])==sorted(y[mm][nn]):
									for m1 in range(3):
										for n1 in range(3):
											mm1=i+m1
											nn1=j+n1
											if not(mm1==ii and nn1==jj) and not(mm1==mm and nn1==nn) and x[mm1][nn1]==0:
												y[mm1][nn1]=list(set(sorted(y[mm1][nn1]))-set(sorted(y[mm][nn])))
												if len(y[mm1][nn1])==1:
													x[mm1][nn1]=y[mm1][nn1][0]
													y[mm1][nn1]=[]
	return x,y

#-----------------------------------------------------
def get_grid():
	a=init_notes()
	for i in range(9):
		for j in range(9):
			a[i][j]=sav[i][j].get()
	return a

def set_grid(a):
	for i in range(9):
		for j in range(9):
			sav[i][j].set(a[i][j])

def csa():
	for i in range(9):
		for j in range(9):
			sav[i][j].set(0)

def solve():
	try:
		notes=init_notes()
		notes_temp=init_notes()
		s=get_grid()
		s,notes=reduce(s)
		while notes != notes_temp:
			notes_temp=notes
			s,notes=hidden_singles_row(s,notes)
			s,notes=hidden_singles_column(s,notes)
			s,notes=hidden_singles_box(s,notes)
		set_grid(s)
	except:
		tkinter.messagebox.showerror('Input Error', 'You either entered \'09\' instead of \'9\' or you left a space blank. Please use \'0\' for empty cells. Thank you.')

#------------------------------------------------------
root=tk.Tk()
root.title('RabbitEars - Sudoku Solver')
ww=300 
wh=300
sw=root.winfo_screenwidth()
sh=root.winfo_screenheight()
cx=int(sw/2-ww/2)
cy=int(sh/2-wh/2)
root.geometry(f'{ww}x{wh}+{cx}+{cy}')
root.resizable(0,0)
root.configure(bg='black')

box=ttk.Frame(root)
box.grid(column=1,row=1)
box.pack(padx=35,pady=10)

sav=[]
for i in range(9):
	temp=[]
	for j in range(9):
		temp.append(tk.IntVar())
	sav.append(temp)

sa=[]
for bi in range(3):
	for bj in range(3):
		gb=ttk.Frame(box)
		gb.grid(row=bi,column=bj,padx=2,pady=2)
		temp=[]
		i=0
		for ei in range(3):
			for ej in range(3):
				temp.append(ttk.Entry(gb,width=1,textvariable=sav[bi*3+ei][bj*3+ej]))
				temp[i].grid(row=bi*3+ei,column=bj*3+ej)
				i+=1
		sa.append(temp)

sb=ttk.Button(box,text="Solve",width=4)
sb.grid(column=0,row=10)
sb.configure(command=solve)
cb=ttk.Button(box,text="Clear",width=4)
cb.grid(column=2,row=10)
cb.configure(command=csa)

root.mainloop()
