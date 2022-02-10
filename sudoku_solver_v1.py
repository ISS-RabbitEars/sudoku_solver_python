#!/usr/bin/env python3.9
import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
import numpy as np


def partition(a):
    b = init_array()
    m = 0
    for i in (0, 3, 6):
        for j in (0, 3, 6):
            n = 0
            for k in range(3):
                for l in range(3):
                    b[i + k][j + l] = a[m][n]
                    n += 1
            m += 1
    return b


def init_array():
    a = np.zeros((9, 9), dtype=int)
    return a


def init_notes():
    a = []
    for i in range(9):
        temp = []
        for j in range(9):
            temp.append([])
        a.append(temp)
    return a


def reduce(x):
    fs = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
    sa_temp = init_array()
    y = init_notes()
    while not np.array_equal(sa_temp, x):
        sa_temp = x
        for i in range(9):
            for j in range(9):
                if x[i][j] == 0:
                    sa_transpose = x.T
                    sa_boxes = partition(x)
                    m = i // 3
                    n = j // 3
                    temp = sa_boxes[m * 3 + n]
                    union = np.union1d(sa_transpose[j], temp)
                    union = np.union1d(union, x[i])
                    comp = np.setdiff1d(fs, union)
                    y[i][j] = comp.tolist()
                    if len(y[i][j]) == 1:
                        x[i][j] = y[i][j][0]
                        y[i][j] = []
                        x, y = reduce(x)
                        x, y = hidden_singles_row(x, y)
                        x, y = hidden_singles_column(x, y)
                        x, y = hidden_singles_box(x, y)
                        #x, y = locked_pair_row(x, y)
                        #x, y = locked_pair_column(x, y)
                        #x, y = locked_pair_box(x, y)
                        #x, y = locked_triple_row(x, y)
    return x, y


def hidden_singles_row(x, y):
    for i in range(9):
        for j in range(9):
            if x[i][j] == 0:
                union =np.zeros([1], dtype=int)
                for k in range(9):
                    if k != j and x[i][k] == 0:
                        note = np.asarray(y[i][k])
                        union = np.union1d(union, note)
                note = np.asarray(y[i][j])
                comp = np.setdiff1d(note, union)
                if comp.size == 1:
                    x[i][j] = comp[0]
                    x, y = reduce(x)
    return x, y


def hidden_singles_column(x, y):
    for i in range(9):
        for j in range(9):
            if x[i][j] == 0:
                union =np.zeros([1], dtype=int)
                for k in range(9):
                    if k != i and x[k][j] == 0:
                        note = np.asarray(y[k][j])
                        union = np.union1d(union, note)
                note = np.asarray(y[i][j])
                comp = np.setdiff1d(note, union)
                if comp.size == 1:
                    x[i][j] = comp[0]
                    x, y = reduce(x)
    return x, y


def hidden_singles_box(x, y):
    for i in (0, 3, 6):
        for j in (0, 3, 6):
            for k in range(3):
                for l in range(3):
                    ii = i + k
                    jj = j + l
                    if x[ii][jj] == 0:
                        union =np.zeros([1], dtype=int)
                        for m in range(3):
                            for n in range(3):
                                mm = i + m
                                nn = j + n
                                if not (mm == ii and nn == jj) and x[mm][nn] == 0:
                                    note = np.asarray(y[mm][nn])
                                    union = np.union1d(union, note)
                        note = np.asarray(y[ii][jj])
                        comp = np.setdiff1d(note, union)
                        if comp.size == 1:
                            x[ii][jj] = comp[0]
                            x, y = reduce(x)
    return x, y


# -----------------------------------------------------
def get_grid():
    a = init_array()
    for i in range(9):
        for j in range(9):
            a[i][j] = sav[i][j].get()
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
        notes = init_notes()
        notes_temp = init_notes()
        s = get_grid()
        s, notes = reduce(s)
        while notes != notes_temp:
            notes_temp = notes
            s, notes = reduce(s)
        set_grid(s)
    except:
        tkinter.messagebox.showerror('Input Error',
                                     'You either entered \'09\' instead of \'9\' or you left a space blank. Please use \'0\' for empty cells. Thank you.')


# ------------------------------------------------------
root = tk.Tk()
root.title('RabbitEars - Sudoku Solver')
ww = 300
wh = 300
sw = root.winfo_screenwidth()
sh = root.winfo_screenheight()
cx = int(sw / 2 - ww / 2)
cy = int(sh / 2 - wh / 2)
root.geometry(f'{ww}x{wh}+{cx}+{cy}')
root.resizable(False, False)
root.configure(bg='black')

box = ttk.Frame(root)
box.grid(column=1, row=1)
box.pack(padx=35, pady=10)

sav = []
for i in range(9):
    temp = []
    for j in range(9):
        temp.append(tk.IntVar())
    sav.append(temp)



sa = []
for bi in range(3):
    for bj in range(3):
        gb = ttk.Frame(box)
        gb.grid(row=bi, column=bj, padx=2, pady=2)
        temp = []
        i = 0
        for ei in range(3):
            for ej in range(3):
                temp.append(ttk.Entry(gb, width=1, textvariable=sav[bi * 3 + ei][bj * 3 + ej]))
                temp[i].grid(row=bi * 3 + ei, column=bj * 3 + ej)
                i += 1
        sa.append(temp)

sb = ttk.Button(box, text="Solve", width=4)
sb.grid(column=0, row=10)
sb.configure(command=solve)
cb = ttk.Button(box, text="Clear", width=4)
cb.grid(column=2, row=10)
cb.configure(command=csa)

root.mainloop()
