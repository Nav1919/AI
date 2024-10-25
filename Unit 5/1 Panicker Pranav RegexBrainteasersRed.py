# import sys; args = sys.argv[1:]
# idx = int(args[0])-50

myRegexLst = [
  r"/\w*(\w)\w*\1\w*/i", #50
  r"/\w*(\w)\w*(\1\w*){3}/i", #51
  r"/^([01])([01]*\1)?$/i", #52
  r"/\b(?=\w{6}\b)\w*cat\w*/i", #53
  r"/\b(?=\w*bri)(?=\w*ing)\w{5,9}\b/i", #54
  r"/\b(?!\w*cat)\w{6}\b/i", #55
  r"/\b((\w)(?!\w*\2))+\b/i", #56
  r"/^(?![01]*10011)[01]*$/", #57
  r"/\w*([aeiou])(?!\1)[aeiou]\w*/i", #58
  r"/^(?![01]*1[01]1)[01]*$/" #59
  ]

# if idx < len(myRegexLst):
#   print(myRegexLst[idx])

for i in myRegexLst:
    print(len(i))
#Pranav Panicker 1 2024