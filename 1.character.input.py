#!/usr/local/bin/python3
import datetime

now = datetime.datetime.now()
name = input("Give me your name: ")
age = int(input("Give me your age: "))

hundred = str(( 100 - age ) + now.year)

print ("Hi, " + name + ", you will turn 100 in: " + hundred)

