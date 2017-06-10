import requests

class HeadersCheck:
    headers = {}
    def getHeaders(self,url,useragent):
        if url != None:
            if useragent=="" or useragent==None or useragent==False or useragent==0:
                r = requests.get(url,verify=False,headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2)'})
            else:
                r = requests.get(url,verify=False,headers={'User-Agent': useragent })   
            self.headers=r.headers
                
    def returnHeaders(self):
        return self.headers
                
    def getServerName(self):
        try:
            return self.headers['server']
        except KeyError as ke:
            return ""

    def getPoweredBy(self):
        try:
            return self.headers['x-powered-by']        
        except TypeError as te:
            return ""
        except KeyError as ke:
            return ""
