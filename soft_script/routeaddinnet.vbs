option explicit 
dim cpan,serverxinghao(100),ser64(10),sxinghao,fsserver,ostype,cpi386,cppatch,cpoem,cpsif,ntstart
dim   fso,fread,strline,i,fr641,fr64,k,strline64
dim objShell
dim diskpt,diskpterr,sxinghao2,fcp,d
dim strComputer,objWMIService,IPConfigSet,IPConfig,myip,j,myipture,myip10,myipgw1,myipgw2,myipgw3
dim dftfile
set   fso=createobject("scripting.filesystemobject")  



'得到ip地址
strComputer = "." 
Set objWMIService = GetObject("winmgmts:\\" & strComputer & "\root\cimv2") 
Set IPConfigSet = objWMIService.ExecQuery _ 
("Select IPAddress from Win32_NetworkAdapterConfiguration where IPEnabled=TRUE") 
For Each IPConfig in IPConfigSet 
If Not IsNull(IPConfig.IPAddress) Then 
For j=LBound(IPConfig.IPAddress) to UBound(IPConfig.IPAddress) 
'WScript.Echo IPConfig.IPAddress(j) 
myip=IPConfig.IPAddress(0) 
Next 
End If 
myipture=InStr(myip,"218.")
if myipture>=1 then myip10=myip

'将ip末位设置成1 或者254

myipgw1=inStrRev(myip10,".")
'WScript.Echo "末尾.位置是"
'WScript.Echo myipgw1
myipgw2=Len(myip10)
'WScript.Echo myipgw2
myipgw3=myipgw2-(myipgw2-myipgw1)
'WScript.Echo myipgw3
myip10=Left(myip10,myipgw3) 
'WScript.Echo myip10
myip10=myip10+"1"
'WScript.Echo myip10

Next 
'WScript.Echo myip10
d="route add 10.0.0.0 mask 255.0.0.0 "+myip10+" -p"
WScript.Echo d
set objShell=wscript.createObject("WScript.Shell")
diskpterr=objShell.Run (d,3,true)