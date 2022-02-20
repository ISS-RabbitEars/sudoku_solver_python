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


def create_notes_reduce(x):
    fs = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9], dtype=int)
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
                        x, y = update(x, y, comp, i, j)
    return x, y


def update(x, y, n, i, j):
    #remove number from notes row/column/box and check for singles
    #scan row and remove n
    for jj in range(9):
        note = np.asarray(y[i][jj], dtype=int)
        comp = np.setdiff1d(note, n)
        y[i][jj] = comp.tolist()
        if comp.size == 1:
            x[i][jj] = comp[0]
            y[i][jj] = []
            x, y = update(x, y, comp, i, jj)
    #scan column and remove n
    for ii in range(9):
        note = np.asarray(y[ii][j], dtype=int)
        comp = np.setdiff1d(note, n)
        y[ii][j] = comp.tolist()
        if comp.size == 1:
            x[ii][j] = comp[0]
            y[ii][j] = []
            x, y = update(x, y, comp, ii, j)
    #scan box and remove n
    a = i // 3
    b = j // 3
    for ii in range(3):
        for jj in range(3):
            mi = a * 3 + ii
            nj = b * 3 + jj
            note = np.asarray(y[mi][nj], dtype=int)
            comp = np.setdiff1d(note, n)
            y[mi][nj] = comp.tolist()
            if comp.size == 1:
                x[mi][nj] = comp[0]
                y[mi][nj] = []
                x, y = update(x, y, comp, mi, nj)
    return x, y


def reduce(x, y):
    fs = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9], dtype=int)
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
                if comp.size == 1:
                    x[i][j] = comp[0]
                    y[i][j] = []
                    x, y = update(x, y, comp, i, j)
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
                    x, y = update(x, y, comp, i, j)
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
                    x ,y = update(x, y, comp, i, j)
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
                            x ,y = update(x, y, comp, ii, jj)
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
                                    x, y = update(x, y, comp, i, m)
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
                                    x, y = update(x, y, comp, m, j)
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
                                                    x, y = update(x, y, comp, mm1, nn1)
    return x, y


def hidden_pair_row(x, y):
    for i in range(9):
        for j in range(9):
            if x[i][j] == 0:
                note1 = np.asarray(y[i][j], dtype=int)
                for jj in range(9):
                    if jj != j and x[i][jj] == 0:
                        note2 = np.asarray(y[i][jj], dtype=int)
                        numb = np.isin(note1, note2)
                        num = note1[numb]
                        if num.size == 2:
                            union = np.zeros([1], dtype=int)
                            for jjj in range(9):
                                if jjj != j and jjj != jj and x[i][jjj] == 0:
                                    note = np.asarray(y[i][jjj], dtype=int)
                                    union = np.union1d(union, note)
                            numb2 = np.isin(union, num)
                            if not numb2.any():
                                y[i][j] = num.tolist()
                                y[i][jj] = num.tolist()
    return x, y


def hidden_pair_column(x, y):
    for i in range(9):
        for j in range(9):
            if x[i][j] == 0:
                note1 = np.asarray(y[i][j], dtype=int)
                for ii in range(9):
                    if ii != i and x[ii][j] == 0:
                        note2 = np.asarray(y[ii][j], dtype=int)
                        numb = np.isin(note1, note2)
                        num = note1[numb]
                        if num.size == 2:
                            union = np.zeros([1], dtype=int)
                            for iii in range(9):
                                if iii != i and iii != ii and x[iii][j] == 0:
                                    note = np.asarray(y[iii][j], dtype=int)
                                    union = np.union1d(union, note)
                            numb2 = np.isin(union, num)
                            if not numb2.any():
                                y[i][j] = num.tolist()
                                y[ii][j] = num.tolist()
    return x, y


def hidden_pair_box(x, y):
    for m in (0, 3, 6):
        for n in (0, 3, 6):
            for i1 in range(3):
                for j1 in range(3):
                    i = m + i1
                    j = n + j1
                    if x[i][j] == 0:
                        note1 = np.asarray(y[i][j], dtype=int)
                        for i2 in range(3):
                            for j2 in range(3):
                                ii = m + i2
                                jj = n + j2
                                if not (ii == i and jj == j) and x[ii][jj] == 0:
                                    note2 = np.asarray(y[ii][jj], dtype=int)
                                    numb = np.isin(note1, note2)
                                    num = note1[numb]
                                    if num.size == 2:
                                        union = np.zeros([1], dtype=int)
                                        for i3 in range(3):
                                            for j3 in range(3):
                                                iii = m + i3
                                                jjj = n + j3
                                                if not (iii == i and jjj == j) and not (iii == ii and jjj == jj) and \
                                                        x[iii][jjj] == 0:
                                                    note = np.asarray(y[iii][jjj], dtype=int)
                                                    union = np.union1d(union, note)
                                        numb2 = np.isin(union, num)
                                        if not numb2.any():
                                            y[i][j] = num.tolist()
                                            y[ii][jj] = num.tolist()
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
                                            x, y = update(x, y, comp, i, m)
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
                                            x, y = update(x, y, comp, m, j)
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
                                                                x, y = update(x, y, comp, mm2, nn2)
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
                                                    x, y = update(x, y, comp, i, n)
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
                                                    x, y = update(x, y, comp, n, j)
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
                                                                        x, y = update(x, y, comp, mm2, nn2)
    return x, y


def hidden_triple2_row(x, y):
    for i in range(9):
        for j in range(9):
            if x[i][j] == 0:
                note1 = np.asarray(y[i][j], dtype=int)
                for j2 in range(9):
                    if j2 != j and x[i][j2] == 0:
                        note2 = np.asarray(y[i][j2], dtype=int)
                        numb = np.isin(note1, note2)
                        num = note1[numb]
                        if num.size == 3:
                            for j3 in range(9):
                                if j3 != j2 and j3 != j and x[i][j3] == 0:
                                    note3 = np.asarray(y[i][j3], dtype=int)
                                    numb1 = np.isin(note1, note3)
                                    num1 = note1[numb1]
                                    if np.array_equal(num1, num):
                                        union = np.zeros([1], dtype=int)
                                        for j4 in range(9):
                                            if j4 != j3 and j4 != j2 and j4 != j and x[i][j4] == 0:
                                                note = np.asarray(y[i][j4], dtype=int)
                                                union = np.union1d(union, note)
                                        numb2 = np.isin(union, num)
                                        if not numb2.any():
                                            y[i][j] = num.tolist()
                                            y[i][j2] = num.tolist()
                                            y[i][j3] = num.tolist()
    return x, y


def hidden_triple2_column(x, y):
    for i in range(9):
        for j in range(9):
            if x[i][j] == 0:
                note1 = np.asarray(y[i][j], dtype=int)
                for i2 in range(9):
                    if i2 != i and x[i2][j] == 0:
                        note2 = np.asarray(y[i2][j], dtype=int)
                        numb = np.isin(note1, note2)
                        num = note1[numb]
                        if num.size == 3:
                            for i3 in range(9):
                                if i3 != i2 and i3 != i and x[i3][j] == 0:
                                    note3 = np.asarray(y[i3][j], dtype=int)
                                    numb1 = np.isin(note1, note3)
                                    num1 = note1[numb1]
                                    if np.array_equal(num1, num):
                                        union = np.zeros([1], dtype=int)
                                        for i4 in range(9):
                                            if i4 != i3 and i4 != i2 and i4 != i and x[i4][j] == 0:
                                                note = np.asarray(y[i4][j], dtype=int)
                                                union = np.union1d(union, note)
                                        numb2 = np.isin(union, num)
                                        if not numb2.any():
                                            y[i][j] = num.tolist()
                                            y[i2][j] = num.tolist()
                                            y[i3][j] = num.tolist()
    return x, y


def hidden_triple2_box(x, y):
    for m in (0, 3, 6):
        for n in (0, 3, 6):
            for i1 in range(3):
                for j1 in range(3):
                    i = m + i1
                    j = n + j1
                    if x[i][j] == 0:
                        note1 = np.asarray(y[i][j], dtype=int)
                        for i2 in range(3):
                            for j2 in range(3):
                                ii = m + i2
                                jj = n + j2
                                if not (ii == i and jj == j) and x[ii][jj] == 0:
                                    note2 = np.asarray(y[ii][jj], dtype=int)
                                    numb = np.isin(note1, note2)
                                    num = note1[numb]
                                    if num.size == 2:
                                        for i3 in range(3):
                                            for j3 in range(3):
                                                iii = m + i2
                                                jjj = n + j2
                                                if not (iii == i and jjj == j) and not (iii == ii and jjj == jj) \
                                                        and x[iii][jjj] == 0:
                                                    note3 = np.asarray(y[iii][jjj], dtype=int)
                                                    numb1 = np.isin(note1, note3)
                                                    num1 = note1[numb1]
                                                    if np.array_equal(num1, num):
                                                        union = np.zeros([1], dtype=int)
                                                        for i4 in range(3):
                                                            for j4 in range(3):
                                                                iiii = m + i4
                                                                jjjj = n + j4
                                                                if not (iiii == i and jjjj == j) and \
                                                                        not (iiii == ii and jjjj == jj) and \
                                                                        not (iiii == iii and jjjj == jjj) and \
                                                                        x[iiii][jjjj] == 0:
                                                                    note = np.asarray(y[iiii][jjjj], dtype=int)
                                                                    union = np.union1d(union, note)
                                                        numb2 = np.isin(union, num)
                                                        if not numb2.any():
                                                            y[i][j] = num.tolist()
                                                            y[ii][jj] = num.tolist()
                                                            y[iii][jjj] = num.tolist()
    return x, y


def pointing_row(x, y):
    for m in (0, 3, 6):
        for n in (0, 3, 6):
            for i in (0, 1, 2):
                row = m + i
                union1 = np.zeros([1], dtype=int)
                #--row1--scan--
                for j in (0, 1, 2):
                    column = n + j
                    note = np.asarray(y[row][column], dtype=int)
                    union1 = np.union1d(union1, note)
                union2 = np.zeros([1], dtype=int)
                #--row2&3-scan--
                for ii in range(3):
                    rowii = m + ii
                    if rowii != row:
                        for jj in range(3):
                            columnjj = n + jj
                            note = np.asarray(y[rowii][columnjj], dtype=int)
                            union2 = np.union1d(union2, note)
                comp1 = np.setdiff1d(union1, union2)
                if comp1.size == 1:
                    #--row1-scan-rest---
                    for jj in range(9):
                        if jj != n and jj != n + 1 and jj != n + 2:
                            note = np.asarray(y[row][jj], dtype=int)
                            comp2 = np.setdiff1d(note, comp1)
                            y[row][jj] = comp2.tolist()
                            if comp2.size == 1:
                                x[row][jj] = comp2[0]
                                y[row][jj] = []
                                x, y = update(x, y, comp2, row, jj)
    return x, y


def pointing_column(x, y):
    for m in (0, 3, 6):
        for n in (0, 3, 6):
            for i in (0, 1, 2):
                column = m + i
                union1 = np.zeros([1], dtype=int)
                #--column1--scan--
                for j in (0, 1, 2):
                    row = n + j
                    note = np.asarray(y[row][column], dtype=int)
                    union1 = np.union1d(union1, note)
                union2 = np.zeros([1], dtype=int)
                #--column2&3-scan--
                for ii in range(3):
                    columnii = m + ii
                    if columnii != column:
                        for jj in range(3):
                            rowjj = n + jj
                            note = np.asarray(y[rowjj][columnii], dtype=int)
                            union2 = np.union1d(union2, note)
                comp1 = np.setdiff1d(union1, union2)
                if comp1.size == 1:
                    #--column1-scan-rest---
                    for jj in range(9):
                        if jj != n and jj != n + 1 and jj != n + 2:
                            note = np.asarray(y[jj][column], dtype=int)
                            comp2 = np.setdiff1d(note, comp1)
                            y[jj][column] = comp2.tolist()
                            if comp2.size == 1:
                                x[jj][column] = comp2[0]
                                y[jj][column] = []
                                x, y = update(x, y, comp2, jj, column)
    return x, y


def box_line_reduction_row(x, y):
    for m in (0, 3, 6):
        for n in (0, 3, 6):
            for i in range(3):
                row = m + i
                union1 = np.zeros([1], dtype=int)
                #--row1--scan--
                for j in range(3):
                    column = n + j
                    note = np.asarray(y[row][column], dtype=int)
                    union1 = np.union1d(union1, note)
                union2 = np.zeros([1], dtype=int)
                #--row1--scan--other-2-boxes--
                for j in range(9):
                    if j != n and j != n+1 and j != n+2:
                        note = np.asarray(y[row][j], dtype=int)
                        union2 = np.union1d(union2, note)
                comp1 = np.setdiff1d(union1, union2)
                #--row2&3--scan
                if comp1.size == 1:
                    for j in range(3):
                        rowi = m + j
                        if rowi != row:
                            for jj in range(3):
                                column = n + jj
                                note = np.asarray(y[rowi][column], dtype=int)
                                comp2 = np.setdiff1d(note, comp1)
                                y[rowi][column] = comp2.tolist()
                                if comp2.size == 1:
                                    x[rowi][column] = comp2[0]
                                    y[rowi][column] = []
                                    x, y = update(x, y, comp2, rowi, column)
    return x, y


def box_line_reduction_column(x, y):
    for m in (0, 3, 6):
        for n in (0, 3, 6):
            for j in range(3):
                column = m + j
                union1 = np.zeros([1], dtype=int)
                #--column1--scan--
                for i in range(3):
                    row = n + i
                    note = np.asarray(y[row][column], dtype=int)
                    union1 = np.union1d(union1, note)
                union2 = np.zeros([1], dtype=int)
                #--column1--scan--other-2-boxes--
                for i in range(9):
                    if i != n and i != n+1 and i != n+2:
                        note = np.asarray(y[i][column], dtype=int)
                        union2 = np.union1d(union2, note)
                comp1 = np.setdiff1d(union1, union2)
                #--column2&3--scan
                if comp1.size == 1:
                    for i in range(3):
                        columni = m + i
                        if columni != column:
                            for ii in range(3):
                                row = n + ii
                                note = np.asarray(y[row][columni], dtype=int)
                                comp2 = np.setdiff1d(note, comp1)
                                y[row][columni] = comp2.tolist()
                                if comp2.size == 1:
                                    x[row][columni] = comp2[0]
                                    y[row][columni] = []
                                    x, y = update(x, y, comp2, row, columni)
    return x, y


def x_wing_row(x, y):
    for i in range(9):
        for j in range(9):
            notej = np.asarray(y[i][j], dtype=int)
            for k in range(notej.size):
                notejk = np.array([notej[k]], dtype=int)
                for jj in range(9):
                    if jj != j:
                        notejj = np.asarray(y[i][jj], dtype=int)
                        num1 = np.isin(notejj, notejk)
                        if num1.any():
                            union = np.zeros([1], dtype=int)
                            for jjj in range(9):
                                if jjj != j and jjj != jj:
                                    note = np.asarray(y[i][jjj], dtype=int)
                                    union = np.union1d(union, note)
                            num2 = np.isin(union, notejk)
                            if num2.any():
                                break
                            else:
                                for ii in range(9):
                                    if ii != i:
                                        noteiij = np.asarray(y[ii][j], dtype=int)
                                        noteiijj = np.asarray(y[ii][jj], dtype=int)
                                        num3 = np.isin(noteiij, notejk)
                                        num4 = np.isin(noteiijj, notejk)
                                        if num3.any() and num4.any():
                                            for jjj in range(9):
                                                if jjj != j and jjj != jj:
                                                    note = np.asarray(y[ii][jjj], dtype=int)
                                                    union = np.union1d(union, note)
                                            num5 = np.isin(union, notejk)
                                            if num5.any():
                                                break
                                            else:
                                                for iii in range(9):
                                                    if iii != i and iii != ii:
                                                        noteiiij = np.asarray(y[iii][j], dtype=int)
                                                        comp1 = np.setdiff1d(noteiiij, notejk)
                                                        y[iii][j] = comp1.tolist()
                                                        noteiiijj = np.asarray(y[iii][jj], dtype=int)
                                                        comp2 = np.setdiff1d(noteiiijj, notejk)
                                                        y[iii][jj] = comp2.tolist()
                                                        if comp1.size == 1:
                                                            x[iii][j] = comp1[0]
                                                            y[iii][j] = []
                                                            x, y = update(x, y, comp1, iii, j)
                                                        if comp2.size == 1:
                                                            x[iii][jj] = comp2[0]
                                                            y[iii][jj] = []
                                                            x, y = update(x, y, comp2, iii, jj)
    return x, y


def x_wing_column(x, y):
    for i in range(9):
        for j in range(9):
            notei = np.asarray(y[i][j], dtype=int)
            for k in range(notei.size):
                noteik = np.array([notei[k]], dtype=int)
                for ii in range(9):
                    if ii != i:
                        noteii = np.asarray(y[ii][j], dtype=int)
                        num1 = np.isin(noteii, noteik)
                        if num1.any():
                            union = np.zeros([1], dtype=int)
                            for iii in range(9):
                                if iii != i and iii != ii:
                                    note = np.asarray(y[iii][j], dtype=int)
                                    union = np.union1d(union, note)
                            num2 = np.isin(union, noteik)
                            if num2.any():
                                break
                            else:
                                for jj in range(9):
                                    if jj != j:
                                        noteijj = np.asarray(y[i][jj], dtype=int)
                                        noteiijj = np.asarray(y[ii][jj], dtype=int)
                                        num3 = np.isin(noteijj, noteik)
                                        num4 = np.isin(noteiijj, noteik)
                                        if num3.any() and num4.any():
                                            for iii in range(9):
                                                if iii != i and iii != ii:
                                                    note = np.asarray(y[iii][jj], dtype=int)
                                                    union = np.union1d(union, note)
                                            num5 = np.isin(union, noteik)
                                            if num5.any():
                                                break
                                            else:
                                                for jjj in range(9):
                                                    if jjj != j and jjj != jj:
                                                        noteijjj = np.asarray(y[i][jjj], dtype=int)
                                                        comp1 = np.setdiff1d(noteijjj, noteik)
                                                        y[i][jjj] = comp1.tolist()
                                                        noteiijjj = np.asarray(y[ii][jjj], dtype=int)
                                                        comp2 = np.setdiff1d(noteiijjj, noteik)
                                                        y[ii][jjj] = comp2.tolist()
                                                        if comp1.size == 1:
                                                            x[i][jjj] = comp1[0]
                                                            y[i][jjj] = []
                                                            x, y = update(x, y, comp1, i, jjj)
                                                        if comp2.size == 1:
                                                            x[ii][jjj] = comp2[0]
                                                            y[ii][jjj] = []
                                                            x, y = update(x, y, comp2, ii, jjj)
    return x, y


def y_wing(x, y):
    for i in range(9):
        for j in range(9):
            if x[i][j] == 0:
                ab = np.asarray(y[i][j], dtype=int)
                if ab.size == 2:
                    b1j = j // 3
                    for j2 in range(9):
                        b2j = j2 // 3
                        if b2j != b1j:
                            bc = np.asarray(y[i][j2], dtype=int)
                            union_abbc = np.union1d(ab, bc)
                            if bc.size == 2 and union_abbc.size == 3:
                                c = np.setdiff1d(bc, ab)
                                b1i = i // 3
                                for i2 in range(9):
                                    b2i = i2 // 3
                                    if b2i != b1i:
                                        ac = np.asarray(y[i2][j], dtype=int)
                                        union_abbcac = np.union1d(union_abbc, ac)
                                        if ac.size == 2 and union_abbcac.size == 3:
                                            test_box = np.asarray(y[i2][j2], dtype=int)
                                            a = np.setdiff1d(ab, bc)
                                            if np.isin(ac, c).any() and np.isin(ac, a).any() and x[i2][j2] == 0 and \
                                                    np.isin(test_box, c).any():
                                                comp = np.setdiff1d(test_box, c)
                                                y[i2][j2] = comp.tolist()
                                                if comp.size == 1:
                                                    x[i2][j2] = comp[0]
                                                    y[i2][j2] = []
                                                    x, y = update(x, y, comp, i2, j2)
    return x, y

def y_wing_row(x, y):
    for i in range(9):
        for j in range(9):
            if x[i][j] == 0:
                ab = np.asarray(y[i][j], dtype=int)
                if ab.size == 2:
                    b1i = i // 3
                    b1j = j // 3
                    for i2 in range(3):
                        ii = b1i * 3 + i2
                        if ii != i:
                            for j2 in range(3):
                                jj = b1j * 3 + j2
                                if x[ii][jj] == 0:
                                    bc = np.asarray(y[ii][jj], dtype=int)
                                    union_abbc = np.union1d(ab, bc)
                                    if bc.size == 2 and union_abbc.size == 3:
                                        c = np.setdiff1d(bc, ab)
                                        for j3 in range(9):
                                            b2j = j3 // 3
                                            if b2j != b1j:
                                                ac = np.asarray(y[i][j3], dtype=int)
                                                union_abbcac = np.union1d(union_abbc, ac)
                                                if ac.size == 2 and union_abbcac.size == 3:
                                                    a = np.setdiff1d(ab, bc)
                                                    if np.isin(ac, c).any() and np.isin(ac, a).any():
                                                        for j4 in range(3):
                                                            jjj = b2j * 3 + j4
                                                            if x[ii][jjj] == 0:
                                                                note = np.asarray(y[ii][jjj], dtype=int)
                                                                comp = np.setdiff1d(note, c)
                                                                y[ii][jjj] = comp.tolist()
                                                                if comp.size == 1:
                                                                    x[ii][jjj] = comp[0]
                                                                    y[ii][jjj] = []
                                                                    x, y = update(x, y, comp, ii, jjj)
                                                        for j4 in range(3):
                                                            jjj = b1j * 3 + j4
                                                            if jjj != j and x[i][jjj] == 0:
                                                                note = np.asarray(y[i][jjj], dtype=int)
                                                                comp = np.setdiff1d(note, c)
                                                                y[i][jjj] = comp.tolist()
                                                                if comp.size == 1:
                                                                    x[i][jjj] = comp[0]
                                                                    y[i][jjj] = []
                                                                    x, y = update(x, y, comp, i, jjj)
    return x, y


def y_wing_column(x, y):
    for i in range(9):
        for j in range(9):
            if x[i][j] == 0:
                ab = np.asarray(y[i][j], dtype=int)
                if ab.size == 2:
                    b1i = i // 3
                    b1j = j // 3
                    for j2 in range(3):
                        jj = b1j * 3 + j2
                        if jj != j:
                            for i2 in range(3):
                                ii = b1i * 3 + i2
                                if x[ii][jj] == 0:
                                    bc = np.asarray(y[ii][jj], dtype=int)
                                    union_abbc = np.union1d(ab, bc)
                                    if bc.size == 2 and union_abbc.size == 3:
                                        c = np.setdiff1d(bc, ab)
                                        for i3 in range(9):
                                            b2i = i3 // 3
                                            if b2i != b1i:
                                                ac = np.asarray(y[i3][j], dtype=int)
                                                union_abbcac = np.union1d(union_abbc, ac)
                                                if ac.size == 2 and union_abbcac.size == 3:
                                                    a = np.setdiff1d(ab, bc)
                                                    if np.isin(ac, c).any() and np.isin(ac, a).any():
                                                        for i4 in range(3):
                                                            iii = b2i * 3 + i4
                                                            if x[iii][jj] == 0:
                                                                note = np.asarray(y[iii][jj], dtype=int)
                                                                comp = np.setdiff1d(note, c)
                                                                y[iii][jj] = comp.tolist()
                                                                if comp.size == 1:
                                                                    x[iii][jj] = comp[0]
                                                                    y[iii][jj] = []
                                                                    x, y = update(x, y, comp, iii, jj)
                                                        for i4 in range(3):
                                                            iii = b1i *3 + i4
                                                            if iii != i and x[iii][j] == 0:
                                                                note = np.asarray(y[iii][j], dtype=int)
                                                                comp = np.setdiff1d(note, c)
                                                                y[iii][j] = comp.tolist()
                                                                if comp.size == 1:
                                                                    x[iii][j] = comp[0]
                                                                    y[iii][j] = []
                                                                    x, y = update(x, y, comp, iii, j)
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
        s, notes = create_notes_reduce(s)
        count = 0
        while notes != notes_temp and count <= 2:
            notes_temp = notes
            s, notes = reduce(s, notes)
            s, notes = hidden_singles_row(s, notes)
            s, notes = hidden_singles_column(s, notes)
            s, notes = hidden_singles_box(s, notes)
            s, notes = locked_pair_row(s, notes)
            s, notes = locked_pair_column(s, notes)
            s, notes = locked_pair_box(s, notes)
            s, notes = hidden_pair_row(s, notes)
            s, notes = hidden_pair_column(s, notes)
            s, notes = hidden_pair_box(s, notes)
            s, notes = locked_triple_row(s, notes)
            s, notes = locked_triple_column(s, notes)
            s, notes = locked_triple_box(s, notes)
            s, notes = hidden_triple_row(s, notes)
            s, notes = hidden_triple_column(s, notes)
            s, notes = hidden_triple_box(s, notes)
            s, notes = hidden_triple2_row(s, notes)
            s, notes = hidden_triple2_column(s, notes)
            s, notes = hidden_triple2_box(s, notes)
            s, notes = pointing_row(s, notes)
            s, notes = pointing_column(s, notes)
            s, notes = box_line_reduction_row(s, notes)
            s, notes = box_line_reduction_column(s, notes)
            s, notes = x_wing_row(s, notes)
            s, notes = x_wing_column(s, notes)
            s, notes = y_wing(s, notes)
            s, notes = y_wing_row(s, notes)
            s, notes = y_wing_column(s, notes)
            if notes_temp == notes:
                s, notes = create_notes_reduce(s)
                count += 1
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
