#!/usr/bin/python

import DNS
import requests
import sys
import socket
import os
from lxml import html

class DomainSearch:

    def getDomainAEntry(self,dominio):
        try:
            if (dominio != ""):
                DNS.defaults['server'] = ['8.8.8.8', '8.8.4.4']
                DNS.defaults['timeout'] = 5
                resul = DNS.dnslookup(dominio, "A")
                if (len(resul) > 0):
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
        except Exception as e:
            return -2

    def getDomainCNameEntry(self,dominio):
        try:
            if(dominio!=""):
                DNS.defaults['server'] = ['8.8.8.8', '8.8.4.4']
                DNS.defaults['timeout'] = 10
                resul = DNS.dnslookup(dominio, "CNAME")
                if( len(resul) > 0 ):
                    return resul[0]
                else:
                    return -1
            else:
                    return -1
        except Exception as e:
            if e.rcode == 3:
                return -1
            else:
                return -2

    def getDomainIP(self,dominio):
        try:
            aentry = self.getDomainAEntry(self.getDomainCNameEntry(dominio))
            if aentry == -1 or aentry == -2:
                aentry = self.getDomainAEntry(dominio)
                if aentry == -1 or aentry == -2:
                    return "NotResolved"
            return aentry
        except AttributeError as ae:
            return "NotResolved"

    def isSeriuslyAtThere(self,dominio,ip):
        try:
            if (self.getDomainAEntry(dominio)==ip or self.getDomainAEntry(self.getDomainCNameEntry(dominio))==ip):
                return 1
            else:
                return 0
        except AttributeError as ae:
            return 0

    def getWhois(self,target,whoisserver="whois.internic.net"):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((whoisserver, 43))
        s.send(target + "\r\n")

        response = ""
        while True:
            data = s.recv(4096)
            response += data
            if not data:
                break
        s.close()
        return response

    def searchDomainsByIF(self,host,isdomain=False):
        domsprovi = []
        try:
            if isdomain:
                host = self.getDomainIP(host)
            domsprovi = self.getWhois(host).split("for detailed information.\n\n")[1].split(
               "\n\nTo single out one record")[0].split("\n")
        except Exception as e:
            pass
            #print e
        doms = []
        for entrada in domsprovi:
            entradalower = str(entrada).lower()
            if self.isSeriuslyAtThere(entradalower,host):
                doms.append(entradalower)
                tmparraydom = entradalower.split(".")
                lentmparraydom = len(tmparraydom)
                dominio = str(tmparraydom[lentmparraydom-2]) + "." + str(tmparraydom[lentmparraydom-1])
                if self.isSeriuslyAtThere(dominio,host) and dominio not in doms:
                    doms.append(dominio)
        return doms

    def subdomainEnum(self,dominio):
        subdomenum = {}
        wordlisttext = ""
        try:
            f = open( os.path.dirname(os.path.abspath(__file__)) + "/subdomlist.txt","r")
            wordlisttext = f.read()
            f.close()
        except:
            return "Issue"
        subdomaintemp = []
        for word in wordlisttext.split("\n"):
            if word != "":
                wildcard = self.getDomainIP("1234.caca.test.1234.cacotas." + dominio)
                if wildcard != "NotResolved":
                    wildcararray = {'subdomain':'*.'+dominio,'ip':wildcard}
                    if wildcararray not in subdomaintemp:
                        subdomaintemp.append(wildcararray)
                    #break
                subdomain = word + "." + dominio
                subdominioip = self.getDomainIP(word + "." + dominio)
                if subdominioip != "NotResolved" and subdominioip != wildcard:
                    subdomaintemp.append({'subdomain':subdomain,'ip':subdominioip})
        subdomenum[dominio] = subdomaintemp
        return subdomenum

    def SearchDomainsInRobtex(self,ip):
        headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'}
        #iptrans=ip.replace(".","/")
        iptrans = str(ip)
        url="https://www.robtex.com/?ip="+iptrans+"&shared=1"
        dominios = []
        try:
            page = requests.get(url, headers=headers, verify=False)
            tree = html.fromstring(page.content)
            ols = tree.find_class("xbul")
            for ol in ols:
                lis = ol.xpath('li')
                for li in lis:
                    dominio = li.text_content()
                    try:
                        if (dominios.index(dominio) > -1) == False:
                            dominios.append(dominio)
                    except ValueError:
                        dominios.append(dominio)
        except Exception as e:
            print e
        return dominios

    def SearchDomains(self,ip):
        try:
            param = {'q': 'ip:'+str(ip)}
            headers = {
              'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'}
            url = 'http://www.bing.com/search'
            try:
                r = requests.get(url, params=param,headers=headers,timeout=20)
            except Exception as gie:
                print gie
                gie=gie
            contentmp= r.text.split("<cite>")
            resul = []
            #resul = self.SearchDomainsInRobtex(ip)
            resul = self.searchDomainsByIF(ip)
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
                    if(self.isSeriuslyAtThere(tmp.lower(),ip)):
                        resul.append(tmp.lower())
            #print ("\x1b[0;32m[\x1b[0m\x1b[0;32m*\x1b[0m\x1b[0;32m]\x1b[0mDominios de " + ip + ":\n")
            #for d in resul:
            #    print d
            #print "--------------------------------------\n"
        except Exception:
            pass
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
        tmpreturn={}
        if (int(ipinitmp[0])>=int(ipfintmp[0]) and int(ipinitmp[1])>=int(ipfintmp[1])\
          and int(ipinitmp[2])>=int(ipfintmp[2]) and int(ipinitmp[3])>=int(ipfintmp[3])):
            count = -1
        while(count != -1):
            iptmp=octa[0]+"."+octa[1]+"."+str(octa[2])+"."+str(octa[3])
            tmpres=self.SearchDomains(iptmp)
            #print ("Dominios de "+iptmp+":\n")
            tmpreturn[iptmp] = []
            print ("[-] Checking IP " + iptmp)
            for w in range(0,len(tmpres)):
                if(self.isSeriuslyAtThere(tmpres[w],iptmp)):
                    #print tmpres[w]+"\n"
                    tmpreturn[iptmp].append(tmpres[w])
                    sys.stdout.write(".")
            #print "--------------------------------------\n"
            print "\n"
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
        print "\n"
        return tmpreturn

