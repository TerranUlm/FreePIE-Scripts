# FreePIE-Scripts

Some sample FreePIE scripts like "vJoy setup" to setup any game for use with a vJoy device

----------------------------

<h2>vJoy-setup.py</h2>

Usage guide:

1. you need TWO vJoy devices - one to be set up and a temporary one to read the configured vJoy events
2. modify your script to send the vJoy events to the temporary one instead of the regular vJoy device
3. start your script
4. start another instance of FreePIE and load+run this script
5. to start recording press Ctrl+Alt+S
6. select which type to record, currently there are two types implemented:
  1. joysticks                                       - Ctrl+Alt+J
  2. keyboard (kinda useless except as an example)   - Ctrl+Alt+K
7. trigger the event you want to record, for joystick events make sure to move the axis all the way into the desired direction
8. once an event is recorded you can start the delayed playback (about 10 seconds delay) by pressing Ctrl+Alt+P. That should be enough time to switch to the target process and start the event recording there.
9. you can either repeat the playback or start a new recording
10. stop this script
11. stop your script, reconfigure it to use the regular vJoy
12. start your script

it might be necessary to run FreePIE as administrator
