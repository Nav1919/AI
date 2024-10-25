import sys; args = sys.argv[1:]
idx = int(args[0])-40

myRegexLst = [
  r"/^[x.o]{64}$/i", #40
  r"/^[xo]*\.[xo]*$/i", #41
  r"/^((x+o*)?\.[xo.]*|[xo.]*\.(o*x+)?)$/i", #52
  r"/^.(..)*$/s", #43
  r"/^((0([10]{2})*)|(1[10]([10]{2})*))$/", #44
  r"/\w*(a[eiou]|e[aiou]|i[aeou]|o[aeiu]|u[aeio])\w*/i", #45
  r"/^(1?0+)*1*$/", #46
  r"/^\b[bc]*a?[bc]*$/", #47
  r"/^\b[bc]*((a[bc]*){2})*$/", #48
  r"/^\b(2[02]*)?((1[02]*){2})*$/" #49
  ]

if idx < len(myRegexLst):
  print(myRegexLst[idx])
#Pranav Panicker 1 2024