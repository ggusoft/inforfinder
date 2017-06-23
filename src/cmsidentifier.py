#!/usr/bin/python

import DNS
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from headerscheck import HeadersCheck

class CmsIdentifier:
    def curl(self, url, useragent):
        try:
            requests.packages.urllib3.disable_warnings()
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
            url = unicode(url)
            if useragent == "":
                useragent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2)\
                 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36'
            headers = {'User-Agent': useragent}
            r = requests.get(url, headers=headers, verify=False,timeout=10)
            res = r.text
            return res
        except Exception as e:
            return "."

    def checkRedir(self,url):
        res=self.curl(url,"")
        try:
            contentmp= res.index("<title>301 Moved Permanently</title>")
            resfilter=[]
            if contentmp > -1:
                resfilter=res.split("href=\"")
                resul=resfilter[1].split("\">")[0]
            else:
                return 0
        except ValueError as verr:
            return 0
        except IndexError as ie:
            return "www."+url
        
    def existsText(self,texto,cadena):
        resul = 0
        try:
            if texto != None and cadena != None:
                contentmp= texto.lower().index(cadena)
                resul = 0
                if contentmp > -1:
                    resul = 1
            else:
                resul = 0
        except ValueError as verr:
            resul = 0
        return resul
        
    def checkJoomla(self,url):
        if url != "":
            res=self.curl(str(url),"")
            reslogin=self.curl(str(url)+"/wp-login.php","")
            resadmin=self.curl(str(url)+"/wp-admin","")
            #if self.existsText(res,"wp-content") or self.existsText(res,"wp-include") or self.existsText(res,"wordpress") or self.existsText(reslogin,"wp-content") or self.existsText(resadmin,"wordpress") :
            if self.existsText(res,"content=\"joomla!") :
                return 1
            else:
                return 0                
        return 0 #si no ocurre nada de lo anterior devuelve 0
        
    def checkJoomlaVersion(self,url):
        res=self.curl(url,"")
        try:
            resfilter=res.split("content=\"Joomla!")
            resfilter[1]=resfilter[1].replace("\n","")
            resultmp = resfilter[1].split("- Open Source Content Management\"")[0]
            resultmp=resultmp.replace(" ","")
            if resultmp=="":
                return "No detected"
            else:
                return resultmp    
        except ValueError as verr:
            return "No detected"
        except IndexError as ierr:         
            return "No detected"
        return ""        
        
    

    def checkWP(self,url):
        if url != "":
            res=self.curl(str(url),"")
            reslogin=self.curl(str(url)+"/wp-login.php","")
            resadmin=self.curl(str(url)+"/wp-admin","")
            if self.existsText(res,"wp-content") or self.existsText(res,"wp-include")  or self.existsText(reslogin,"wp-content") or self.existsText(resadmin,"wordpress") :
                return 1
            else:
                return 0
        else:
            return 0

    def checkWPVersion(self,url):
        res=self.curl(url+"/wp-login.php","")
        try:
            contentmp= res.lower().index("name=\"generator\"")
            resfilter=[]
            if contentmp > -1:
                resfilter=res.split("meta name=\"generator\" content=\"")
                return resfilter[1].split("\" />")[0]
        except IndexError as ierr:         
            return "No detected"
        except ValueError as verr:
            try:
                contentmp= res.lower().index("buttons-css")
                resfilter=[]
                if contentmp > -1:
                    resfilter=res.split("wp-includes/css/buttons.min.css?ver=")
                    return resfilter[1].split("'")[0]         
            except IndexError as ierr:         
                                return "No detected"
            except ValueError as verr:
                res=self.curl(url+"/readme.html","")
                try:
                    resfilter=res.split("<br /> Version ")
                    resfilter[1]=resfilter[1].replace("\n","")
                    return resfilter[1].split("</h1>")[0]
                except ValueError as verr:
                    return "No detected"
                except IndexError as ierr:         
                    return "No detected"

    def checkPrestaShop(self,url):
        hc = HeadersCheck() 
        try:     
            hc.getHeaders(url,"")
            headers = hc.returnHeaders()
        except Exception:
            return False
        try:
            if headers['Powered-By'] == "PrestaShop":
                return True        
        except TypeError as te:
            return False
        except KeyError as ke:
            return False
        

        
