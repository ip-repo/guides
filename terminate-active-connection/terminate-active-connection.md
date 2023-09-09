<h2>How to identify active connection by pid using netstat and tasklist on windows 10</h2>
So, on windows if we want to see tcp connections we can use <b>netstat</b>. <br>
Lets say were using the command:

```console
netstat -a
```
This will list all the active connections.

```console
Active Connections

  Proto  Local Address          Foreign Address        State
  TCP    0.0.0.0:235            username:0                LISTENING
  TCP    0.0.0.0:345            username:0                LISTENING
```
So now we can see the active connections but we need more information in order to identify the process easliy.<br>
Lets say you want to know PID and process name ?<br>
The -b option will allow to know the process name and the -abon options will also show the PID.
```console
netstat -b #1
netstat -abon #2
netstat -a -o #3
tasklist /FI "PID eq 9624"
```

```console
#1 result
  TCP    0.0.0.0:0000         ccc-000-000-000-000:https  ESTABLISHED
 [chrome.exe]
#2 result
  TCP    0.0.0.0:0000        000.000.000.000:000    ESTABLISHED     9624
 [chrome.exe]
#3 result
 TCP    0.0.0.0:00000          username:0                LISTENING       820
#4 result
Image Name                     PID Session Name        Session#    Mem Usage
========================= ======== ================ =========== ============
chrome.exe                    9624 Console                    1     00,00 K
```

The problem with those commands 1 and 2 is that you need administrator privileges to execute them.<br>

Lets see how we can use <b>netstat -a -o</b> which do not require administrator privilege to generate a list of active connections.<br>
Then we can iterate the list and use the command <b>tasklist /FI "PID eq 0000" -[commandname][operation][condition][process id to find]</b>.<br>
Next we can print the information line by line:
<b>Information from netstat -a -o</b> + <b>information from tasklist /FI "PID eq 0000" </b>
This should give the user the active tcp connections image name with some additonal info.

<h3>Python</h3>

```python
import os
LINE = '-' * 100 
net_stat = os.popen('netstat -a -o').read()
active_connections = net_stat.split('\n')
print(LINE)
for connection in active_connections[4:-1]:
    output = os.popen('tasklist /FI "PID eq {}"'.format(connection.split(' ')[-1])).read().split('\n')
    output = output[1] + '\n' +  output[3] 
    print(LINE)
    print(active_connections[3].lstrip() + '\n' + connection.lstrip() + '\n')

    print(output + '\n')
    print(LINE)
print(LINE)
print('Ctrl + C to exit :D')
while True:
    try:
       continue
    except KeyboardInterrupt:
        break
```




