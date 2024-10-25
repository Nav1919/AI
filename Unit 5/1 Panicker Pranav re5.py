import sys; args = sys.argv[1:]
idx = int(args[0])-40

myRegexLst = [
  r"/^(?=\w*a)(?=\w*e)(?=\w*i)(?=\w*o)(?=\w*u)\w+$/i", #1
  r"/^(?!(\w*[aeiou]){6,})\w+$/i", #2
  r"/^(\w)(?=[^\1]*\1)\w*\1$/i", #3
  r"/^(\w)(\w)(\w)\w*(?<=\3\2\1)$/i", #4
  r"/^\w*(bt|tb)(?<![tb]\w*)(?!\w*[tb])\w*$/i", #5
  r"/^\w*(\w)\1{1}\w*$/i", #6
  r"/^\w*(\w)(\w*\1){1}\w*$/i", #7
  r"/^\w*(\w\w)(\w*\1){1}\w*$/i", #8
  r"/^([aeiou]*[b-df-hj-np-tv-z]){1}[aeiou]*$/i", #9
  r"/^((\w)(?!\w*\2))+$/i" #10
  ]

if idx < len(myRegexLst):
  print(myRegexLst[idx])
#Pranav Panicker 1 2024