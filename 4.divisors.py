num = int(input("Give me a number: "))

x = range(1,num+1)

for ele in x:
  if num % ele == 0:
    print (ele)
