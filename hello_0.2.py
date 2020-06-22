#simple
var1 = "Hello"
var2 = "World"
print(var1 + " " + var2 + "!")

#weird format stuff
print("{0:s} World!".format("Hello"))
print("{0:s} {1:s}!".format("Hello","World"))


#loop
text = "Hello World!\n"

for c in text:
  print(c, end = '')
