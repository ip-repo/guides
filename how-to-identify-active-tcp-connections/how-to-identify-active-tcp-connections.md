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
Then we can iterate the list and use the command <b>tasklist /FI "PID eq 0000" -[commandname][operation][condition-process id to find]</b>.<br>
Next we can print the information line by line:
<b>Information from netstat -a -o</b> + <b>information from tasklist /FI "PID eq 0000" </b>
This should give the user the active tcp connections image name with some additonal info.

<h3>Python</h3>

* generate active coneections list with the command netstat -a -o.
* iterate over each active connetion and use the tasklist /FI to find the connection equivalent information from the tasklist and then create a dictionary conatining all that information.
* iterate the processes dictionaries and print a formatted output to the user.

```python
import os
active_connection_list = os.popen('netstat -a -o').read().split("\n")
connection_dicts = []
for connection in active_connection_list[4:-1]:
    connection_values = [value for value in connection.split(" ") if value]

    pid = connection_values[-1]
    connection_values = connection_values[:-1]
    new_connection_dict = {}
    new_connection_dict[pid] = [connection_values]
    if len(connection_values) == 3:
        connection_values.append(" ")
    connection_dicts.append(new_connection_dict)
    find_by_pid = os.popen('tasklist /FI "PID eq {}"'.format(pid)).read()
    process_info = [elem for elem in  find_by_pid.split("\n")[3].split(" ") if elem != ""]
    new_connection_dict[pid].append(process_info)
   
for connection_dict in connection_dicts:
    print("*" * 70)
    for key in connection_dict.keys():       
        output_1 = "Protocol: {}\nLocal Address: {}\nForigen Address: {}".format(connection_dict[key][0][0], connection_dict[key][0][1],  connection_dict[key][0][2])
        output_2 = "State: {}\nImage Name: {}".format( connection_dict[key][0][3], connection_dict[key][1][0])
        output_3 = "PID: {}\nSession Name: {}\nSession# {}".format(connection_dict[key][1][1],connection_dict[key][1][2],connection_dict[key][1][3])
        output_4 = "Memory Usage: {}".format( connection_dict[key][1][4] + connection_dict[key][1][5])
        print(output_1)
        print(output_2)
        print(output_3)
        print(output_4)
    print("*" * 70)

```
Now, yo should see a list of active connection and the process name and combined information from the two commands.

```console
**********************************************************************
Protocol: TCP
Local Address: [0000:0000:0000:0000:0000:0000:0000:0000]:00000
Forigen Address:000000-00: https
State: ESTABLISHED
Image Name: processname.exe
PID: 6501
Session Name: Console
Session# 1
Memory Usage: 19,072K
**********************************************************************
```


