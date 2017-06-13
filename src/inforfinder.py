#!/usr/bin/python
from bingchecker import  DomainSearch
from cmsidentifier import CmsIdentifier
from headerscheck import HeadersCheck
import sys
import requests.packages.urllib3
from requests.packages.urllib3.exceptions import InsecureRequestWarning

class Inforfinder:

    config = {
        'commands': {
            '--help': 'self.printHelpInfo()',
            '-help':'self.printHelpInfo()',
            '-d':'self.execByDomain(args,pos)',
            '-dD':'self.execByMultiDomain(args,pos)',
            '-dI':'self.execByIP(args,pos)',
            '-dR':'self.execByIpRange(args,pos)',
            '-dF':'self.execByFile(args,pos)'
        },
        'optionals':{
            '-cms':0,
            '-servinfo':0
        }
    }

    def getLogo(self):
        return """
        \x1b[0;37m\n
    ,#@@@ +++       #+++
   @@@### @@@       @@@#
   @+     @@@       @@@#
  `@  @@@ @@@       @@@#
  `@  ##@ @@@       @@@#
   @'   @ @@@       @@@#
   @@@@@@ @@@       @@@#
    ,#### @@@       @@@#
          @@@       @@@#
    @@@@@ @@@       @@@#
   @@     @@@       @@@#
   @.     @@@       @@@#
  .@  @@@ @@@'      @@@;
   @.   @ @@@@,    @@@@
   @@   @  @@@@@@@@@@@#
    @@@@@  .@@@@@@@@@@
              :;'':.
    @@@@ ,@@@, +@@@@@@@@
   +'    @   @ @     @
    @@@@ @   @ @@@@  @
       @`@   @ @     @
   `@@@@ '@#@+ @     @
   \x1b[0m\n
   \x1b[0;33m
    ________________________________________________________________________

    InforFinder v0.98
    Powered By GGUsoft 2017
    Domain collector and CMS recognizer / HTTP information server collector
    ________________________________________________________________________
    \x1b[0m\n\n
    """

    def printHelpInfo(self):
        #print self.getLogo()
        print ("\n\t\x1b[0;38m Commands:\x1b[0m\r\n")
        print ("\t\x1b[0;38m -d <dominio>\x1b[0m\t\t\t\tGet a domain for apply any optional commands\r\n")
        print ("\t\x1b[0;38m -dD <dominio>\x1b[0m\t\t\t\tGet a domain list hosted in IP of the specified domain\r\n")
        print ("\t\x1b[0;38m -dI <IP>\x1b[0m\t\t\t\tGet a domain list hosted in the specified IP \r\n")
        print (
        "\t\x1b[0;38m -dR <IP inicio> <IP fin>\x1b[0m\t\tGet a domain list hosted in every IP of the specified range\r\n")
        print ("\t\x1b[0;38m -dF <file>\x1b[0m\t\t\t\tGet a list with all domains hosted"+
               " at same IP from a file, the file contens a IP by line\r\n")
        print ("\n\t\x1b[0;38m Optionals:\x1b[0m\r\n")
        print (
        "\t\x1b[0;38m inforfinder <command> -cms\x1b[0m\t\tCheck if every domain found has a cms website (wordpress, joomla ,etc) and show version\r\n")
        print ("\t\x1b[0;38m inforfinder <command> -servinfo\x1b[0m\tCheck web server parameter\r\n")

    def printCabeceraInfo(self,host):
        print ("\x1b[0;32m[\x1b[0m\x1b[0;32m*\x1b[0m\x1b[0;32m]\x1b[0mDomains of " + host + ":\n")

    def execByDomain(self,args,pos):
        dom = [args[pos + 1]]
        self.execCmsAndSinfo(dom)

    def execByMultiDomain(self,args,pos):
        ds = DomainSearch()
        try:
            ip = ds.getDomainAEntry(ds.getDomainCNameEntry(args[pos + 1]))
        except Exception as ie:
            ip = -1
        if (ip == -1 or ip == -2):
            ip = ds.getDomainAEntry(args[pos + 1])
        self.printCabeceraInfo(ip)
        dom = ds.SearchDomains(ip)
        if self.config['optionals']['-cms'] == 0 and self.config['optionals']['-servinfo'] == 0:
            for d in dom:
                print d
        else:
            self.execCmsAndSinfo(dom)
        print "================================================================================"

    def execByIP(self,args,pos):
        ds = DomainSearch()
        ip = args[pos + 1]
        self.printCabeceraInfo(ip)
        dom = ds.SearchDomains(ip)
        if self.config['optionals']['-cms'] == 0 and self.config['optionals']['-servinfo'] == 0:
            for d in dom:
                print d
        else:
            self.execCmsAndSinfo(dom)
        print "================================================================================"

    def execByIpRange(self,args,pos):
        ds = DomainSearch()
        ip = args[pos + 1]
        ip2 = args[pos + 2]
        self.printCabeceraInfo( str( ip + " - " + ip2 ))
        dom = ds.SearchDomainsOnIpRange(ip,ip2)
        if self.config['optionals']['-cms'] == 0 and self.config['optionals']['-servinfo'] == 0:
            for ip in dom:
                self.printCabeceraInfo(ip)
                for d in dom[ip]:
                    print d
                print "================================================================================"
        else:
            for ip in dom:
                self.printCabeceraInfo(ip)
                self.execCmsAndSinfo(dom[ip])
                print "================================================================================"

    def execByFile(self,args,pos):
        ips = []
        fichero = args[pos + 1]
        try:
            f = open(fichero, 'r')
            for line in f:
                ips.append(line.replace("\n", ""))
            f.close()
            ds = DomainSearch()
            self.printCabeceraInfo(fichero)
            for ip in ips:
                self.printCabeceraInfo(ip)
                dom = ds.SearchDomains(ip)
                if self.config['optionals']['-cms'] == 0 and self.config['optionals']['-servinfo'] == 0:
                    for d in dom:
                        print d
                else:
                    self.execCmsAndSinfo(dom)
                print "================================================================================"
        except IOError:
            print "The file couldn't be read"


    def execCmsAndSinfo(self,dom):
        ds = DomainSearch()
        cmsi = CmsIdentifier()
        hcheck = HeadersCheck()
        sname = ""
        cmstype = ""
        for y in dom:
            domi = y
            if self.config['optionals']['-cms'] == 1:
                cmstype = "No CMS detected"
                redir = cmsi.checkRedir(domi)
                if redir != 0:
                    url = redir
                else:
                    url = domi
                    url = unicode(url).replace(u'\xf1',"")
                if cmsi.existsText(str(url), "http") != 1 and url != 0 and url != None:
                    url = "http://" + url
                if cmsi.checkWP(url) == 1:
                    cmstype = "WordPress (version: " + str(cmsi.checkWPVersion(url)) + ")"
                if cmsi.checkJoomla(url) == 1:
                    cmstype = "Joomla (version: " + str(cmsi.checkJoomlaVersion(url)) + ")"
                if cmsi.checkPrestaShop(url) == True:
                    cmstype = "Prestashop (version: No version detected)"
                    # TODO cmstype="Prestashop (version: "+ str(cmsi.checkPrestashoVersion(url))+")"
            if self.config['optionals']['-servinfo'] == 1:
                try:
                    hcheck.getHeaders(url, "")
                    servname = hcheck.getServerName()
                except Exception:
                    servname = "No detected"
                sname = "Server-software:" + str(servname)
                spb = hcheck.getPoweredBy()
                if spb != 0 and spb != "" and spb != None:
                    sname = sname + " Powered-By:" + hcheck.getPoweredBy()
            print(unicode( domi + "\t" + cmstype + "\t" + unicode(sname)))

    def isExistsArg(self,argv,arg):
        try:
            pos = argv.index(arg)
            return [True,pos]
        except:
            return [False,-1]

    def howToDo(self,args):
        try:
            if (len(args) < 2):
                args.append("--help")
            for option in self.config['optionals']:
                optionchk = self.isExistsArg(args, option)
                if optionchk[0] == True:
                    self.config['optionals'][option] = 1
            for cmd in self.config['commands']:
                check = self.isExistsArg(args, cmd)
                if check[0]==True:
                    pos = check[1]
                    toexec = self.config['commands'][cmd]
                    exec(toexec)
                    break
            print "\n"
        except KeyboardInterrupt as kie:
            exit()

    def __init__(self):
        print (self.getLogo())
        requests.packages.urllib3.disable_warnings()
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

if __name__ == "__main__":
    ifinder = Inforfinder()
    ifinder.howToDo(sys.argv)
