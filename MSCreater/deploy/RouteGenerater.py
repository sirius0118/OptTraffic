import os
 
service，然后匹配使用哪个Pod 

def CreateService(FilePath):
    os.system("kubectl apply -f " + FilePath)