#!/usr/bin/python

import DNS
import pycurl
import cStringIO



class DomainSearch:


	def getDomainAEntry(self,dominio):
		try:
		        if(dominio!=""):
                                DNS.defaults['server'] = ['8.8.8.8', '8.8.4.4']
                                resul = DNS.dnslookup(dominio, "A")
                                if( len(resul) > 0 ):
                                        return resul[0]
                                else:
                                        return -1
                                 
                        else:
                                return -1
                except DNS.ServerError as e:
                        if e.rcode == 3:
                                return -1
                        else:
                                return -2

	def isSeriuslyAtThere(self,dominio,ip):
		if (self.getDomainAEntry(dominio)==ip):
		        return 1
		else:
		        return 0
		        
        def SearchDomains(self,ip):
                buf = cStringIO.StringIO()
                c = pycurl.Curl()
                c.setopt(c.URL, 'http://www.bing.com/search?q=ip%3a'+ip)
                c.setopt(c.USERAGENT,'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2)\
                         AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36')
                c.setopt(c.WRITEFUNCTION, buf.write)
                c.perform()
                res = buf.getvalue()
                buf.close()
                contentmp= res.split("<cite>")
                resul = []
                for i in range(1,len(contentmp)):
                       tmp=contentmp[i].split("</cite>")[0]
                       tmp=tmp.replace("https://","")
                       tmp=tmp.replace("http://","")
                       tmp=tmp.replace("www.","")
                       tmp=tmp.split("?")[0]
                       tmp=tmp.split("/")[0]
                       try:
                        resul.index(tmp)
                       except ValueError as e:
                        
                        if(self.isSeriuslyAtThere(tmp,ip)):
                                resul.append(tmp)
                       
                return resul
        
        def SearchDomainsOnIpRange(self,ipini,ipfin):
		if(ipini==""):
		        ipini="0.0.0.0"
		if(ipfin==""):
		        ipfin="0.0.0.0"
		        
		ipinitmp = ipini.split(".")
		ipfintmp = ipfin.split(".")
		
		octa = [ipinitmp[0],ipinitmp[1],ipinitmp[2],ipinitmp[3]]
		count = int(octa[3])
		tmpreturn=[]
		
		if (int(ipinitmp[0])>=int(ipfintmp[0]) and int(ipinitmp[1])>=int(ipfintmp[1])\
                  and int(ipinitmp[2])>=int(ipfintmp[2]) and int(ipinitmp[3])>=int(ipfintmp[3])):
                        count = -1
		while(count != -1):
        		iptmp=octa[0]+"."+octa[1]+"."+str(octa[2])+"."+str(octa[3])
        		tmpres=self.SearchDomains(iptmp)
        		print ("Dominios de "+iptmp+":\n")
        		for w in range(0,len(tmpres)):
        		        if(self.isSeriuslyAtThere(tmpres[w],iptmp)):
        		                print tmpres[w]+"\n"
        		                tmpreturn.append([iptmp,tmpres[w]])
        		print "--------------------------------------\n"
        		
        		if(int(octa[0])==int(ipfintmp[0]) and int(octa[1])==int(ipfintmp[1])\
        		 and int(octa[2])==int(ipfintmp[2]) and int(octa[3])==int(ipfintmp[3])):
        		        count=-1
        		       
        		else:
        		        if(int(octa[3])>=255 and int(octa[2])>=255 and int(octa[1])>=255 and int(octa[0])<int(ipfintmp[0]) ):
        		               octa[0]=octa[0]+1
        		               octa[1]=0
        		               
        		        if(int(octa[3])>=255 and int(octa[2])>=255 and int(octa[1])<int(ipfintmp[1]) ):
					octa[1]=octa[1]+1
					octa[2]=0
				
				#Fin Sumatorio de 2 byte
				#Sumatorio de 3er y 4 byte
				
				if(count < 255 ): 
					count=count+1
					octa[3]=count
					
				
				else:
				        if(count >= 255 and int(octa[2])<int(ipfintmp[2]) ):
					        count=0
					        octa[3]=count
					        octa[2]=int(octa[2])+1			
				
				        else:
				        	count=-1
                return tmpreturn
                
                
