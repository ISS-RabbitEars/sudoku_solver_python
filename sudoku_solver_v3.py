#!/usr/bin/env python3.9
import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
import numpy as np


def sa_partition(a):
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
                    sa_boxes = sa_partition(x)
                    m = i // 3
                    n = j // 3
                    box_mn = sa_boxes[m * 3 + n]
                    union = np.union1d(sa_transpose[j], box_mn)
                    union = np.union1d(union, x[i])
                    comp = np.setdiff1d(fs, union)
                    y[i][j] = comp.tolist()
                    if comp.size == 1:
                        x[i][j] = comp[0]
                        y[i][j] = []
    return x, y


def hidden_singles_row(x, y):
    for i in range(9):
        for j in range(9):
            if x[i][j] == 0:
                union = np.zeros([1], dtype=int)
                for k in range(9):
                    if k != j and x[i][k] == 0:
                        note = np.asarray(y[i][k], dtype=int)
                        union = np.union1d(union, note)
                note = np.asarray(y[i][j], dtype=int)
                comp = np.setdiff1d(note, union)
                if comp.size == 1:
                    x[i][j] = comp[0]
                    y[i][j] = []
            x, y = reduce(x)
    return x, y


def hidden_singles_column(x, y):
    for i in range(9):
        for j in range(9):
            if x[i][j] == 0:
                union = np.zeros([1], dtype=int)
                for k in range(9):
                    if k != i and x[k][j] == 0:
                        note = np.asarray(y[k][j], dtype=int)
                        union = np.union1d(union, note)
                note = np.asarray(y[i][j], dtype=int)
                comp = np.setdiff1d(note, union)
                if comp.size == 1:
                    x[i][j] = comp[0]
                    y[i][j] = []
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
                        union = np.zeros([1], dtype=int)
                        for m in range(3):
                            for n in range(3):
                                mm = i + m
                                nn = j + n
                                if not (mm == ii and nn == jj) and x[mm][nn] == 0:
                                    note = np.asarray(y[mm][nn], dtype=int)
                                    union = np.union1d(union, note)
                        note = np.asarray(y[ii][jj], dtype=int)
                        comp = np.setdiff1d(note, union)
                        if comp.size == 1:
                            x[ii][jj] = comp[0]
                            y[ii][jj] = []
                    x, y = reduce(x)
    return x, y


def locked_pair_row(x, y):
    for i in range(9):
        for j in range(9):
            note1 = np.asarray(y[i][j], dtype=int)
            if x[i][j] == 0 and note1.size == 2:
                for k in range(9):
                    note2 = np.asarray(y[i][k], dtype=int)
                    if k != j and x[i][k] == 0 and np.array_equal(note1, note2):
                        for m in range(9):
                            if m != j and m != k and x[i][m] == 0:
                                note3 = np.asarray(y[i][m], dtype=int)
                                comp = np.setdiff1d(note3, note2)
                                y[i][m] = comp.tolist()
                                if comp.size == 1:
                                    x[i][m] = comp[0]
                                    y[i][m] = []
    return x, y


def locked_pair_column(x, y):
    for i in range(9):
        for j in range(9):
            note1 = np.asarray(y[i][j], dtype=int)
            if x[i][j] == 0 and note1.size == 2:
                for k in range(9):
                    note2 = np.asarray(y[k][j], dtype=int)
                    if k != i and x[k][j] == 0 and np.array_equal(note1, note2):
                        for m in range(9):
                            if m != i and m != k and x[m][j] == 0:
                                note3 = np.asarray(y[m][j], dtype=int)
                                comp = np.setdiff1d(note3, note2)
                                y[m][j] = comp.tolist()
                                if comp.size == 1:
                                    x[m][j] = comp[0]
                                    y[m][j] = []
    return x, y


def locked_pair_box(x, y):
    for i in (0, 3, 6):
        for j in (0, 3, 6):
            for k in range(3):
                for l in range(3):
                    ii = i + k
                    jj = j + l
                    note1 = np.asarray(y[ii][jj], dtype=int)
                    if x[ii][jj] == 0 and note1.size == 2:
                        for m in range(3):
                            for n in range(3):
                                mm = i + m
                                nn = j + n
                                note2 = np.asarray(y[mm][nn], dtype=int)
                                if not (mm == ii and nn == jj) and x[mm][nn] == 0 and \
                                        np.array_equal(note1, note2):
                                    for m1 in range(3):
                                        for n1 in range(3):
                                            mm1 = i + m1
                                            nn1 = j + n1
                                            if not (mm1 == ii and nn1 == jj) and not (mm1 == mm and nn1 == nn) and \
                                                    x[mm1][nn1] == 0:
                                                note3 = np.asarray(y[mm1][nn1], dtype=int)
                                                comp = np.setdiff1d(note3, note2)
                                                y[mm1][nn1] = comp.tolist()
                                                if comp.size == 1:
                                                    x[mm1][nn1] = comp[0]
                                                    y[mm1][nn1] = []
    return x, y


def locked_triple_row(x, y):
    for i in range(9):
        for j in range(9):
            note1 = np.asarray(y[i][j], dtype=int)
            if x[i][j] == 0 and note1.size == 3:
                for k in range(9):
                    note2 = np.asarray(y[i][k], dtype=int)
                    if k != j and x[i][k] == 0 and np.array_equal(note1, note2):
                        for h in range(9):
                            note3 = np.asarray(y[i][h], dtype=int)
                            if h != j and h != k and x[i][h] == 0 and np.array_equal(note2, note3):
                                for m in range(9):
                                    if m != j and m != k and m != h and x[i][m] == 0:
                                        note4 = np.asarray(y[i][m], dtype=int)
                                        comp = np.setdiff1d(note4, note3)
                                        y[i][m] = comp.tolist()
                                        if comp.size == 1:
                                            x[i][m] = comp[0]
                                            y[i][m] = []
    return x, y


def locked_triple_column(x, y):
    for i in range(9):
        for j in range(9):
            note1 = np.asarray(y[i][j], dtype=int)
            if x[i][j] == 0 and note1.size == 3:
                for k in range(9):
                    note2 = np.asarray(y[k][j], dtype=int)
                    if k != i and x[k][j] == 0 and np.array_equal(note1, note2):
                        for h in range(9):
                            note3 = np.asarray(y[h][j], dtype=int)
                            if h != i and h != k and x[h][j] == 0 and np.array_equal(note2, note3):
                                for m in range(9):
                                    if m != i and m != k and m != h and x[m][j] == 0:
                                        note4 = np.asarray(y[m][j], dtype=int)
                                        comp = np.setdiff1d(note4, note3)
                                        y[m][j] = comp.tolist()
                                        if comp.size == 1:
                                            x[m][j] = comp[0]
                                            y[m][j] = []
    return x, y


def locked_triple_box(x, y):
    for i in (0, 3, 6):
        for j in (0, 3, 6):
            for k in range(3):
                for l in range(3):
                    ii = i + k
                    jj = j + l
                    note1 = np.asarray(y[ii][jj], dtype=int)
                    if x[ii][jj] == 0 and note1.size == 3:
                        for m in range(3):
                            for n in range(3):
                                mm = i + m
                                nn = j + n
                                note2 = np.asarray(y[mm][nn], dtype=int)
                                if not (mm == ii and nn == jj) and x[mm][nn] == 0 and \
                                        np.array_equal(note1, note2):
                                    for m1 in range(3):
                                        for n1 in range(3):
                                            mm1 = i + m1
                                            nn1 = j + n1
                                            note3 = np.asarray(y[mm1][nn1], dtype=int)
                                            if not (mm1 == ii and nn1 == jj) and not (mm1 == mm and nn1 == nn) and \
                                                    x[mm1][nn1] == 0 and np.array_equal(note2, note3):
                                                for m2 in range(3):
                                                    for n2 in range(3):
                                                        mm2 = i + m2
                                                        nn2 = j + m2
                                                        if not (mm2 == ii and nn2 == jj) and \
                                                                not (mm2 == mm and nn2 == nn) and \
                                                                not (mm2 == mm1 and nn2 == nn1) and \
                                                                x[mm2][nn2] == 0:
                                                            note4 = np.asarray(y[mm2][nn2], dtype=int)
                                                            comp = np.setdiff1d(note4, note3)
                                                            y[mm2][nn2] = comp.tolist()
                                                            if comp.size == 1:
                                                                x[mm2][nn2] = comp[0]
                                                                y[mm2][nn2] = []
    return x, y


def hidden_triple_row(x, y):
    for i in range(9):
        for j in range(9):
            note1 = np.asarray(y[i][j], dtype=int)
            if x[i][j] == 0 and (note1.size == 2 or note1.size == 3):
                for k in range(9):
                    note2 = np.asarray(y[i][k], dtype=int)
                    if k != j and x[i][k] == 0 and (note2.size == 3 or note2.size == 2):
                        union12 = np.union1d(note1, note2)
                        if union12.size == 3:
                            for m in range(9):
                                note3 = np.asarray(y[i][m], dtype=int)
                                if m != j and m != k and x[i][m] == 0 and (note3.size == 3 or note3.size == 2):
                                    union123 = np.union1d(union12, note3)
                                    if union123.size == 3:
                                        for n in range(9):
                                            if n != j and n != k and n != m and x[i][n] == 0:
                                                note4 = np.asarray(y[i][n], dtype=int)
                                                comp = np.setdiff1d(note4, union123)
                                                y[i][n] = comp.tolist()
                                                if comp.size == 1:
                                                    x[i][n] = comp[0]
                                                    y[i][n] = []
    return x, y


def hidden_triple_column(x, y):
    for i in range(9):
        for j in range(9):
            note1 = np.asarray(y[i][j], dtype=int)
            if x[i][j] == 0 and (note1.size == 2 or note1.size == 3):
                for k in range(9):
                    note2 = np.asarray(y[k][j], dtype=int)
                    if k != i and x[k][j] == 0 and (note2.size == 3 or note2.size == 2):
                        union12 = np.union1d(note1, note2)
                        if union12.size == 3:
                            for m in range(9):
                                note3 = np.asarray(y[m][j], dtype=int)
                                if m != i and m != k and x[m][j] == 0 and (note3.size == 3 or note3.size == 2):
                                    union123 = np.union1d(union12, note3)
                                    if union123.size == 3:
                                        for n in range(9):
                                            if n != i and n != k and n != m and x[n][j] == 0:
                                                note4 = np.asarray(y[n][j], dtype=int)
                                                comp = np.setdiff1d(note4, union123)
                                                y[n][j] = comp.tolist()
                                                if comp.size == 1:
                                                    x[n][j] = comp[0]
                                                    y[n][j] = []
    return x, y


def hidden_triple_box(x, y):
    for i in (0, 3, 6):
        for j in (0, 3, 6):
            for k in range(3):
                for l in range(3):
                    ii = i + k
                    jj = j + l
                    note1 = np.asarray(y[ii][jj], dtype=int)
                    if x[ii][jj] == 0 and (note1.size == 3 or note1.size == 2):
                        for m in range(3):
                            for n in range(3):
                                mm = i + m
                                nn = j + n
                                note2 = np.asarray(y[mm][nn], dtype=int)
                                if not (mm == ii and nn == jj) and x[mm][nn] == 0 and \
                                        (note2.size == 3 or note2.size == 2):
                                    union12 = np.union1d(note1, note2)
                                    if union12.size == 3:
                                        for m1 in range(3):
                                            for n1 in range(3):
                                                mm1 = i + m1
                                                nn1 = j + n1
                                                note3 = np.asarray(y[mm1][nn1], dtype=int)
                                                if not (mm1 == ii and nn1 == jj) and not (mm1 == mm and nn1 == nn) and \
                                                        x[mm1][nn1] == 0 and (note3.size == 3 or note3.size == 2):
                                                    union123 = np.union1d(union12, note3)
                                                    if union123.size == 3:
                                                        for m2 in range(3):
                                                            for n2 in range(3):
                                                                mm2 = i + m2
                                                                nn2 = j + m2
                                                                if not (mm2 == ii and nn2 == jj) and \
                                                                        not (mm2 == mm and nn2 == nn) and \
                                                                        not (mm2 == mm1 and nn2 == nn1) and \
                                                                        x[mm2][nn2] == 0:
                                                                    note4 = np.asarray(y[mm2][nn2], dtype=int)
                                                                    comp = np.setdiff1d(note4, union123)
                                                                    y[mm2][nn2] = comp.tolist()
                                                                    if comp.size == 1:
                                                                        x[mm2][nn2] = comp[0]
                                                                        y[mm2][nn2] = []
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
        notes_temp = init_notes()
        s = get_grid()
        s, notes = reduce(s)
        while notes != notes_temp:
            notes_temp = notes
            s, notes = hidden_singles_row(s, notes)
            s, notes = hidden_singles_column(s, notes)
            s, notes = hidden_singles_box(s, notes)
            notes_temp2 = init_notes()
            while notes != notes_temp2:
                notes_temp2 = notes
                s, notes = locked_pair_row(s, notes)
                s, notes = locked_pair_column(s, notes)
                s, notes = locked_pair_box(s, notes)
                s, notes = locked_triple_row(s, notes)
                s, notes = locked_triple_column(s, notes)
                s, notes = locked_triple_box(s, notes)
                s, notes = hidden_triple_row(s, notes)
                s, notes = hidden_triple_column(s, notes)
                s, notes = hidden_triple_box(s, notes)
        set_grid(s)
    except:
        tkinter.messagebox.showerror('Input Error',
                                     'You either entered \'09\' instead of \'9\' or you left a space blank. Please '
                                     'use \'0\' for empty cells. Thank you.')


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
