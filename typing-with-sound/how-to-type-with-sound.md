# Using python and Sonic-Pi to play notes while typing  😊🎵🎹

So Sonic Pi is a cool program that allow a user to create music with code and even allow to live code.
In this short guide we will see how to send data which will be notes from a python script to sonic pi and play them.
The idea is to use `pynput` to listen to the keyboard and each time a on_press event occur then we will send a random
note to play on sonic py. This kind of code will create a musical effect that we can use for example  when writing a how-to guide in a cool vibe.  

What you will need to have installed:
* Sonic Pi <a href="https://sonic-pi.net/">Click here for download</a>
* Python
 
Dependencies:
```console
pip install pynput #1.7.7
pip install python-osc # 1.8.3
```
Good, now that we have everthing installed , launch Sonic pi and add the following code:

```sonic-pi
# play the note recived on osc
live_loop :playkey do
  use_real_time
  a = sync "/osc*/trigger/keystroke"
  use_synth :bass_foundation
  play a ,amp: 0.011
end
```

Next, Open you favorite IDE and copy the next python code:

```python
from pynput.keyboard import Listener
from pythonosc import udp_client
import random

def send_random_notes_to_sonic_pi(key):
    """
    This function is called when over a key is pressed, each time 
    a random note will be sent to the sonic pi live_loop that is waiting for data
    and the note will be played in sonic pi.
    """
    # Sonic Pi notes goes from 0 to 128 
    numbers_note = list(range(30, 80))
    # Choose random note
    random_note = random.choice(numbers_note)
    sender.send_message('/trigger/keystroke', random_note)
    print(f"Key pressed:{key}",f"Note sent:{random_note}")
   

# Use Keyboard Listener and listen for the on_press event
# When the on_press event occurs, call the send_random_notes_to_sonic_pi function
if __name__ == "__main__":
    # Your local adress
    local_adress = "127.0.0.1"
    # Sonic Pi default OSC port
    osc_sonic_pi_port = 4560
    # Establishe a connection between python script and Sonic Pi using the UDP protocol
    sender = udp_client.SimpleUDPClient('127.0.0.1', 4560)
    # Open Keyboard listener and each time a key is pressed call the function send_random_notes_to_sonic_pi
    with Listener(on_press=send_random_notes_to_sonic_pi) as l:
        l.join()
```
Finally, run the python code and the sonic pi code (order do not matter in this case).

And now while you are using your keyboard to type you should the hear random notes, happy typing :)
