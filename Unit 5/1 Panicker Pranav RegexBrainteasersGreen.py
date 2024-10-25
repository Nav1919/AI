import sys; args = sys.argv[1:]
idx = int(args[0])-30

myRegexLst = [
  r"/^100$|^101$|^0$/", #30
  r"/\A[01]*\Z/", #31
  r"/^.*0$/", #32
  r"/\w*[aeiou]\w*[aeiou]\w*/i", #33
  r"/^0$|\A1[01]*0\Z/", #34
  r"/^[01]*110[01]*$/", #35
  r"/^...?.?$/s", #36
  r"/^\d{3} *-? *\d{2} *-? *\d{4}$/", #37
  r"/^.*?d\w*/mi", #38
  r"/^[01]?$|^0[01]*0$|^1[01]*1$/" #39
  #r"/^0*$|^1*$|^[01]$|^0[01]*0$|^1[01]*1$/" #39

  ]

if idx < len(myRegexLst):
  print(myRegexLst[idx])
#Pranav Panicker 1 2024