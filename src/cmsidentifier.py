#!/usr/bin/python

import DNS
import pycurl
import cStringIO



class CmsIdentifier:


	def checkRedir(self,url):
	        buf = cStringIO.StringIO()
                c = pycurl.Curl()
                c.setopt(c.URL, url)
                c.setopt(c.USERAGENT,'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2)\
                         AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36')
                c.setopt(c.WRITEFUNCTION, buf.write)
                c.perform()
                res = buf.getvalue()
                buf.close()
                try:
	                contentmp= res.index("<title>301 Moved Permanently</title>")
	                resfilter=[]
	                if contentmp > -1:
	                        resfilter=res.split("href=\"")
	                        return resfilter[1].split("\">")[0]
	                else:
	                        return 0
	        except ValueError as verr:
	                return 0
	                
        def checkJoomla(self,url):
                return 0
        
        def checkJoomlaVersion(self,url):
                return 0
        
        def checkWP(self,url):
                
                buf = cStringIO.StringIO()
                c = pycurl.Curl()
                c.setopt(c.URL, url)
                c.setopt(c.USERAGENT,'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2)\
                         AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36')
                c.setopt(c.WRITEFUNCTION, buf.write)
                c.perform()
                res = buf.getvalue()
                buf.close()
                try:
                        contentmp= res.lower().index("wordpress")
                        resul = 0
                        if contentmp > -1:
                                buf = cStringIO.StringIO()
                                c = pycurl.Curl()
                                c.setopt(c.URL, url+"/wp-login.php")
                                c.setopt(c.USERAGENT,'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2)\
                                         AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36')
                                c.setopt(c.WRITEFUNCTION, buf.write)
                                c.perform()
                                res = buf.getvalue()
                                buf.close()
                                contentmp= res.lower().index("wp-admin")
                                if contentmp > -1:
                                       resul = 1
                except ValueError as verr:
                        resul = 0
                               
                return resul
                
        def checkWPVersion(self,url):
                buf = cStringIO.StringIO()
                c = pycurl.Curl()
                c.setopt(c.URL, url+"/wp-login.php")
                c.setopt(c.USERAGENT,'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2)\
                    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36')
                c.setopt(c.WRITEFUNCTION, buf.write)
                c.perform()
                res = buf.getvalue()
                buf.close()
                try:
	                contentmp= res.lower().index("name=\"generator\"")
	                resfilter=[]
	                if contentmp > -1:
	                        resfilter=res.split("meta name=\"generator\" content=\"")
	                        return resfilter[1].split("\" />")[0]

	                
	        except ValueError as verr:
	                try:
	                        contentmp= res.lower().index("buttons-css")
                                resfilter=[]
                            
	                        if contentmp > -1:
	                                resfilter=res.split("wp-includes/css/buttons.min.css?ver=")
	                                return resfilter[1].split("'")[0]         
                        
                        except ValueError as verr:
                                buf = cStringIO.StringIO()
                                c = pycurl.Curl()
                                c.setopt(c.URL, url+"/readme.html")
                                c.setopt(c.USERAGENT,'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2)\
                                    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36')
                                c.setopt(c.WRITEFUNCTION, buf.write)
                                c.perform()
                                res = buf.getvalue()
                                buf.close()
                                try:
                                        resfilter=res.split("<br /> Version ")
	                                resfilter[1]=resfilter[1].replace("\n","")
	                                return resfilter[1].split("</h1>")[0]
	                        except ValueError as verr:
	                                return "No detected"
                                except IndexError as ierr:         
                                        return "No detected"
        
#a=CmsIdentifier()

#url = raw_input()
#if url == "":
#        url="http://esandra.com"
#redir=a.checkRedir(url)
#print "checkredir:"+str(redir)
#if redir == 0:
#        print "checkwp:"+str(a.checkWP(url))
#        print "Version:"+str(a.checkWPVersion(url))
#else:
#        print "checkwp(R):"+str(a.checkWP(redir))
#        print "Version:"+str(a.checkWPVersion(redir))
        

        
