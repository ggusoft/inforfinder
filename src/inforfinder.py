#!/usr/bin/python
from bingchecker import  DomainSearch
from cmsidentifier import CmsIdentifier
import sys

ds = DomainSearch()
cmsi = CmsIdentifier()
cms=0
dom=[]
try:

        if(len(sys.argv)<2):
                sys.argv.append("--help")

        for i in range(1,len(sys.argv)):
                if (sys.argv[i].lower() == "--help" ):
                        print ("\x1b[0;31m InforFinder v0.1\n Powered By GGUsoft 2014\x1b[0m\n\n")
                        print ("\t\x1b[0;32m -dD <dominio>  \x1b[0m\t\tSaca un listado de dominios alojados en la misma IP a partir del dominio\r\n")        
                        print ("\t\x1b[0;32m -dI <IP>  \x1b[0m\t\t\tSaca un listado de dominios alojados en la misma IP a partir de una IP\r\n")        
                        print ("\t\x1b[0;32m -dR <IP inicio> <IP fin>  \x1b[0m\tSaca un listado de dominios alojados en la misma IP a partir de cada IP del rango\r\n")  
                        print ("\t\x1b[0;32m -dF <Archivo>  \x1b[0m\tSaca un listado de dominios alojados en la misma IP a partir de cada IP del fichero\r\n")       
                        break
                if (sys.argv[i]=="-cms"):
                        cms=1
                if (sys.argv[i]=="-dD"):
                        ip=ds.getDomainAEntry(sys.argv[i+1])
                        dom=ds.SearchDomains(ip)
                if (sys.argv[i]=="-dI"):
                        dom=ds.SearchDomains(sys.argv[i+1])
                if (sys.argv[i]=="-dR" and len(sys.argv)>= 4):
                        dom=ds.SearchDomainsOnIpRange(sys.argv[i+1],sys.argv[i+2])
                if (sys.argv[i]=="-dF" and len(sys.argv)>= 4):
                        dom=ds.SearchDomainsOnIpRange(sys.argv[i+1],sys.argv[i+2])
                if cms==1:
                        for i in dom:
                                cmstype="No detectado"
                                redir=cmsi.checkRedir(i)
                                if redir != 0:
                                        url=redir
                                else:
                                        url=i
                                        
                                if cmsi.checkWP(url) == 1:
                                        cmstype="WordPress (version: "+ str(cmsi.checkWPVersion(url))+")"
                                        
                                print(i+" "+cmstype)
                else:
                        for i in dom:
                                print(i)
                                        
                
except KeyboardInterrupt as kie:
        exit()
#try:
#        
#        print("Introduce ip de inicio:")
#        ipini = raw_input()
#        print("Introduce ip de fin:")
#        ipfin = raw_input()
#        ds.SearchDomainsOnIpRange(ipini,ipfin)
#except KeyboardInterrupt as err:
#        exit()

