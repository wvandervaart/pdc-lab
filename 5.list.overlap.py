def same (list1, list2):
  list_same = [i for i in list1 + list2 if i in list1 and i in list2]
  list_same = list(dict.fromkeys(list_same))
  return list_same

a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
b = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

print ("List first: " + str(a))
print ("List second: " + str(b))

z = same (a, b)
print ("Found in both lists: " + str(z))

