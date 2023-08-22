# auto-exec-info-gathering
a python script when run in any laptop/server he make 2 nmap scans (localhost and network scan) save them to json files and send them to server with the public ip
# Description:
in simple terms : when the main.py run he grab the localhost local and publicip addr then make 2 nmap scans one for the localhost ,the second for the entire network then save the output to json files and send all files to a server
# REMARK: 
you can change the way the files send you can use an SMTP server and email service ...
# Installation:
1-git clone the repo
# How To Use:
1-run server.py in your device
2-send the main.py to the target (you can turn it into exe)

# REMARK
if you want to send the script outside your network you have to enable portforwarding or use some services like localhost.run
