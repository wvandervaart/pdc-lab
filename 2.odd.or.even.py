number = int(input("Give me a number: "))
calc = number % 2
four = number % 4

if calc == 0:
  print ("Number is even")
if calc > 0:
  print ("Number is odd")
if four == 0:
  print ("Number is a multiple of 4")
