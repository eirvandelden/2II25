## Generate test data
URI = "http://edocol.com/namespace/1.0/"
input = []

for i in range(0,100):
  input.append(URI+str(i))
print "Dit is de input: \n"
print input

## find a new id 

def getnewid(input):
  #initialisation
  index = []

  #Check for an empty list
  if input == []:
    output = "0"
  else: #input is a list of possible id's
    #filter only the values
    for i in input:                                                              # for each input
      p = len(i)-1                                                               # set the last position
      a = i[p:]                                                                  # get the last value from the result
      # Filter possible ) character
      if a[0] == ")":
        p = p-1
        a = i[p:]
      #start adding characters from back to front until we find a /
      while a[0] != "/":                                                        # while we haven't got the whole value
        p = p-1                                                                 # set the boundary lower
        a = i[p:]                                                               # add that extra character
      #We now have the complete value
      index.append(i[p+1:])
      print i[p+1:]
    # Sort the new array
    print "Dit is de index array na verwijdering van crap:\n"
    print index
    sorted(index)
    print "dit is de array na sorteren:\n"
    print index
    output = index.pop()
    print output
  return output
  
a = getnewid(input)
print a