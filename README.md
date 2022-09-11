# Inforfinder
===========

Inforfinder is a tool made to collect information of any domain pointing at a server (ip,domain,range,file).

Requires python libs: pyRequests, lxml and py3DNS

You can do the installation, with pip or you can install the inforfinder app as a package using `python setup.py install` or `pip install inforfinder.zip`

## Installing dependencies without the setup.py

- First, you need to install complementary libraries: 

	user@machine$ sudo apt-get install python-dns python-dnspython python-requests python-lxml python
	
	OR
	
	    pip install  py3dns
	pip install requests --upgrade
	    pip install  lxml

- Then Download "inforfinder"


## Using

- The next step is to run "inforfinder.py": python inforfinder.py --help

Find more information on how to use this app:
	 <pre>
	 InforFinder v2.0.0 Powered By GGUsoft 2022
	
	 Powered By GGUsoft 2022
	
	 Commands:
	
	 -d <dominio>				Gets a domain for apply any optional commands
	
	 -dD <dominio>				Gets a domain list hosted in IP of the specified domain
	
	 -dI <IP>				Gets a domain list hosted in the specified IP 
	
	 -dR <IP inicio> <IP fin>		Gets a domain list hosted in every IP of the specified range
	
	 -dF <file>				Gets a list with all domains hosted at same IP from a file, the file contens a IP by line
	 
	 Optionals:
	
	 inforfinder <command> -cms			Checks if every domain found has a cms website (wordpress, joomla ,etc) and show version
	
	 inforfinder <command> -servinfo		Checks web server parameters
	
	 inforfinder <command> --subdomain-enum          Lists subdomains of every domain found
	 </pre>
