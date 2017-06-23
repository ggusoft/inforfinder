Inforfinder
===========

Inforfinder is a tool made to collect information of any domain pointing at a server (ip,domain,range,file).

Requires python libs: pyRequests and pyDNS

-First, you need to install complementary libraries: 
	
	user@machine$ sudo apt-get install python-dns python-dnspython python-requests python-lxml python

	OR

        pip install  pydns
	pip install requests --upgrade
        pip install  lxml
	
-Then Download "inforfinder"

-The next step is to run "inforfinder.py": python inforfinder.py --help

Find more information on how to use this app:
	 
	 InforFinder v1.0.9 Powered By GGUsoft 2017

	 Powered By GGUsoft 2017

	 Commands:

	 -d <dominio>				Get a domain for apply any optional commands

	 -dD <dominio>				Get a domain list hosted in IP of the specified domain

	 -dI <IP>				Get a domain list hosted in the specified IP 

	 -dR <IP inicio> <IP fin>		Get a domain list hosted in every IP of the specified range

	 -dF <file>				Get a list with all domains hosted at same IP from a file, the file contens a IP by line


	 Optionals:

	 inforfinder <command> -cms		Check if every domain found has a cms website (wordpress, joomla ,etc) and show version

	 inforfinder <command> -servinfo	Check web server parameters
