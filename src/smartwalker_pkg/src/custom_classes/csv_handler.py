#!/usr/bin/env python3

import csv
import time
import os

def create_csv_file(name_file, dir, col1, col2, col3=None, col4=None):

    name_file = os.path.join("/home/crist/tesi/src/smartwalker_pkg/csv_datafiles/" + dir, name_file)
    with open(name_file, "w", newline='') as f:
        writer = csv.writer(f)
        if col4 is None:
            if col3 is None:
                writer.writerow([col1, col2])
            else:
                writer.writerow([col1, col2, col3])
        else:
            writer.writerow([col1, col2, col3, col4])

def save_to_csv_one_value(name_file, dir, val1, start_time):
    name_file = os.path.join("/home/crist/tesi/src/smartwalker_pkg/csv_datafiles/" + dir, name_file)
    current_time = (time.time() - start_time)
    with open(name_file, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([current_time, val1])

def save_to_csv_two_values(name_file, dir, val1, val2, start_time):
    name_file = os.path.join("/home/crist/tesi/src/smartwalker_pkg/csv_datafiles/" + dir, name_file)
    current_time = (time.time() - start_time)
    with open(name_file, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([current_time, val1, val2])

def save_to_csv_three_values(name_file, dir, val1, val2, val3, start_time):
    name_file = os.path.join("/home/crist/tesi/src/smartwalker_pkg/csv_datafiles/" + dir, name_file)
    current_time = (time.time() - start_time)
    with open(name_file, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([current_time, val1, val2, val3])

def read_from_csv_two_values(name_file, dir):
    name_file = os.path.join("/home/crist/tesi/src/smartwalker_pkg/csv_datafiles/" + dir, name_file)
    istoftime = []
    val1 = []
    val2 = []
    with open(name_file, newline='') as f:
        reader = csv.reader(f, delimiter=',', quotechar='|')
        next(reader) # Non leggo i "titoli" delle colonne
        for row in reader:
            istoftime.append(float(row[0]))
            val1.append(float(row[1]))
            val2.append(float(row[2]))
        return istoftime, val1, val2

def read_from_csv_one_value(name_file, dir):
    name_file = os.path.join("/home/crist/tesi/src/smartwalker_pkg/csv_datafiles/" + dir, name_file)
    istoftime = []
    val1 = []
    with open(name_file, newline='') as f:
        reader = csv.reader(f, delimiter=',', quotechar='|')
        next(reader) # Non leggo i "titoli" delle colonne
        for row in reader:
            istoftime.append(float(row[0]))
            val1.append(float(row[1]))
        return istoftime, val1
