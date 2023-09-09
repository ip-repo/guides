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
```

```console
#1 result
  TCP    0.0.0.0:0000         ccc-000-000-000-000:https  ESTABLISHED
 [chrome.exe]
#2 result
  TCP    0.0.0.0:0000        000.000.000.000:000    ESTABLISHED     9624
 [chrome.exe]
```

The problem with those commands is that you need administrator privileges to execute them.<br>
Lets commbine the commands <b>netstat and tasklist with python </b> to create a script the will allow us to know the active tcp connection pid and name with some more information. 
