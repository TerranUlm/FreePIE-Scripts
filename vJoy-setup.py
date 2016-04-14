import BaseHTTPServer
import time

# Usage guide:
# 1) you need TWO vJoy devices - one to be set up and a temporary one to read the configured vJoy events
# 2) modify your script to send the vJoy events to the temporary one instead of the regular vJoy
# 3) start your script
# 4) start another instance of FreePIE and load+run this script
# 5) to start recording press Ctrl+Alt+S
# 6) select which type to record, currently there are two types implemented:
#    a) joysticks                                       - Ctrl+Alt+J
#    b) keyboard (kinda useless except as an example)   - Ctrl+Alt+K
# 7) trigger the event you want to record, for joystick events make sure to move the axis all the way into the desired direction
# 8) once an event is recorded you can start the delayed playback (about 10 seconds delay) by pressing Ctrl+Alt+P. That should be enough time to switch to the target process and start the event recording there.
# 9) you can either repeat the playback or start a new recording
# 10) stop this script
# 11) stop your script, reconfigure it to use the regular vJoy
# 12) start your script
#
# it might be necessary to run FreePIE as administrator



if starting:
	system.setThreadTiming(TimingTypes.HighresSystemTimer)
	system.threadExecutionInterval = 5
	def calculate_rate(max, time):
		if time > 0:
			return max / (time / system.threadExecutionInterval)
		else:
			return max

	int32_max = (2 ** 14) - 1
	int32_min = (( 2** 14) * -1) + 1
	
	vJoy0 = vJoy[1]
	# joysticks as seen by Windows "Gamecontrollers"
	# 0: vJoy[1]
	# 1: Hotas
	# 2: Lenkrad
	# 3: Gamepad
	# 4: vJoy[0]
	vJoy1 = joystick[4]
	
	recordInput=False
	recordKeyboard=False
	recordJoystick=False
	recordedKey=False
	recordedJoystick=False
	recordedJoystickValue=False
	
	joyCenter = 0

	vJoy0.setAnalogPov(0, -1)
	vJoy0.setAnalogPov(1, -1)
	vJoy0.slider = joyCenter
	vJoy0.dial = joyCenter
	vJoy0.x = joyCenter
	vJoy0.y = joyCenter
	vJoy0.z = joyCenter
	vJoy0.rx = joyCenter
	vJoy0.ry = joyCenter
	vJoy0.rz = joyCenter
	
	def moveAxis(axis, maxval):
		for x in range(0, maxval, maxval/abs(maxval)):
			if axis=="x":
				vJoy0.x=x
			if axis=="y":
				vJoy0.y=x
			if axis=="z":
				vJoy0.z=x
			if axis=="rx":
				vJoy0.rx=x
			if axis=="ry":
				vJoy0.ry=x
			if axis=="rz":
				vJoy0.rz=x
			if axis=="Slider1":
				vJoy0.slider=x
			if axis=="Slider2":
				vJoy0.dial=x
			time.sleep(0.0001)
		speech.say("ping")
		time.sleep(1)


	
#diagnostics.watch(recordInput)
#diagnostics.watch(recordKeyboard)
#diagnostics.watch(recordJoystick)
#diagnostics.watch(recordedKey)
diagnostics.watch(recordedJoystick)
diagnostics.watch(recordedJoystickValue)
diagnostics.watch(vJoy1.getDown(0))
diagnostics.watch(vJoy1.x)
diagnostics.watch(vJoy1.y)
diagnostics.watch(vJoy1.z)
diagnostics.watch(vJoy1.xRotation )
diagnostics.watch(vJoy1.yRotation )
diagnostics.watch(vJoy1.zRotation )
diagnostics.watch(vJoy1.sliders[0])
diagnostics.watch(vJoy1.sliders[1])
diagnostics.watch(vJoy1.pov[0])
diagnostics.watch(vJoy1.pov[1])

if recordInput==False:
	if keyboard.getKeyDown(Key.LeftAlt) and keyboard.getKeyDown(Key.LeftControl) and keyboard.getKeyDown(Key.S):
		speech.say("Aufzeichnung aktiviert")
		recordInput=True
		recordKeyboard=False
		recordJoystick=False
		recordedKey=False
		recordedJoystick=False

if recordInput:
	if keyboard.getKeyDown(Key.LeftAlt) and keyboard.getKeyDown(Key.LeftControl) and keyboard.getKeyDown(Key.K):
		speech.say("Tastatur wird aufgezeichnet sobald keine Taste mehr gedrückt ist")
		recordKeyboard=True
		recordJoystick=False
	if keyboard.getKeyDown(Key.LeftAlt) and keyboard.getKeyDown(Key.LeftControl) and keyboard.getKeyDown(Key.J):
		speech.say("Joystick wird aufgezeichnet")
		recordJoystick=True
		recordKeyboard=False
		recordInput=False

if recordKeyboard and recordInput and keyboard.getKeyUp(Key.LeftAlt) and keyboard.getKeyUp(Key.LeftControl) and keyboard.getKeyUp(Key.K):
	recordInput=False
	speech.say("Tastatur wird jetzt aufgezeichnet")
	
if recordJoystick and recordInput==False and recordedJoystick==False:
	for x in range(0, 21):
		if vJoy1.getDown(x):
			recordedJoystickValue=x
			recordedJoystick="Button"

	if vJoy1.x> 900:
		recordedJoystickValue=vJoy0.axisMax
		recordedJoystick="x"
	if vJoy1.x< -900:
		recordedJoystickValue=-vJoy0.axisMax
		recordedJoystick="x"
	if vJoy1.y> 900:
		recordedJoystickValue=vJoy0.axisMax
		recordedJoystick="y"
	if vJoy1.y< -900:
		recordedJoystickValue=-vJoy0.axisMax
		recordedJoystick="y"
	if vJoy1.z> 900:
		recordedJoystickValue=vJoy0.axisMax
		recordedJoystick="z"
	if vJoy1.z< -900:
		recordedJoystickValue=-vJoy0.axisMax
		recordedJoystick="z"

	if vJoy1.xRotation> 900:
		recordedJoystickValue=vJoy0.axisMax
		recordedJoystick="rx"
	if vJoy1.xRotation< -900:
		recordedJoystickValue=-vJoy0.axisMax
		recordedJoystick="rx"
	if vJoy1.yRotation> 900:
		recordedJoystickValue=vJoy0.axisMax
		recordedJoystick="ry"
	if vJoy1.yRotation< -900:
		recordedJoystickValue=-vJoy0.axisMax
		recordedJoystick="ry"
	if vJoy1.zRotation> 900:
		recordedJoystickValue=vJoy0.axisMax
		recordedJoystick="rz"
	if vJoy1.zRotation< -900:
		recordedJoystickValue=-vJoy0.axisMax
		recordedJoystick="rz"

	if vJoy1.sliders[0]> 900:
		recordedJoystickValue=vJoy0.axisMax
		recordedJoystick="Slider1"
	if vJoy1.sliders[0]< -900:
		recordedJoystickValue=-vJoy0.axisMax
		recordedJoystick="Slider1"
	if vJoy1.sliders[1]> 900:
		recordedJoystickValue=vJoy0.axisMax
		recordedJoystick="Slider2"
	if vJoy1.sliders[1]< -900:
		recordedJoystickValue=-vJoy0.axisMax
		recordedJoystick="Slider2"

	if vJoy1.pov[0] <> -1:
		recordedJoystickValue=vJoy1.pov[0]
		recordedJoystick="Pov1"
	if vJoy1.pov[1] <> -1:
		recordedJoystickValue=vJoy1.pov[1]
		recordedJoystick="Pov2"



if recordJoystick and recordInput==False and recordedJoystick<>False:
	recordJoystick=False
	# Joystick ist aufgezeichnet und kann jetzt abgespielt werden, vorher aber alles "auf Null"
	#vJoy0.setPressed() # nix zu tun
	speech.say("Joystick ist aufgezeichnet, Wiedergabe kann gestartet werden")
	vJoy0.setAnalogPov(0, -1)
	vJoy0.setAnalogPov(1, -1)
	vJoy0.slider = joyCenter
	vJoy0.dial = joyCenter
	vJoy0.x = joyCenter
	vJoy0.y = joyCenter
	vJoy0.z = joyCenter
	vJoy0.rx = joyCenter
	vJoy0.ry = joyCenter
	vJoy0.rz = joyCenter
	
if recordKeyboard==False and recordInput==False and recordedJoystick<>False:
	if keyboard.getKeyDown(Key.LeftAlt) and keyboard.getKeyDown(Key.LeftControl) and keyboard.getKeyDown(Key.P):
		speech.say("Wiedergabe aktiviert, der Joystick-Event \"" + recordedJoystick + "\" wird ausgegeben in")
		time.sleep(5)
		speech.say("fünf")
		time.sleep(1)
		speech.say("vier")
		time.sleep(1)
		speech.say("drei")
		time.sleep(1)
		speech.say("zwei")
		time.sleep(1)
		speech.say("eins")
		time.sleep(1)
		if "Button" == recordedJoystick:
			vJoy0.setButton(recordedJoystickValue, True)
			time.sleep(1)
			vJoy0.setButton(recordedJoystickValue, False)
		if "Pov1" == recordedJoystick:
			vJoy0.setAnalogPov(0, recordedJoystickValue)
		if "Pov2" == recordedJoystick:
			vJoy0.setAnalogPov(1, recordedJoystickValue)
		if "Slider1" == recordedJoystick:
			moveAxis("Slider1", recordedJoystickValue)
		if "Slider2" == recordedJoystick:
			moveAxis("Slider2", recordedJoystickValue)
		if "x" == recordedJoystick:
			moveAxis("x", recordedJoystickValue)
		if "y" == recordedJoystick:
			moveAxis("y", recordedJoystickValue)
		if "z" == recordedJoystick:
			moveAxis("z", recordedJoystickValue)
		if "rx" == recordedJoystick:
			moveAxis("rx", recordedJoystickValue)
		if "ry" == recordedJoystick:
			moveAxis("ry", recordedJoystickValue)
		if "rz" == recordedJoystick:
			moveAxis("rz", recordedJoystickValue)
		time.sleep(1)
		# alles wieder "auf Null"
		vJoy0.setAnalogPov(0, -1)
		vJoy0.setAnalogPov(1, -1)
		vJoy0.slider = joyCenter
		vJoy0.dial = joyCenter
		vJoy0.x = joyCenter
		vJoy0.y = joyCenter
		vJoy0.z = joyCenter
		vJoy0.rx = joyCenter
		vJoy0.ry = joyCenter
		vJoy0.rz = joyCenter
		speech.say("fertig")

if recordKeyboard and recordInput==False and recordedKey==False:
	if keyboard.getPressed(Key.A):
		recordedKey=Key.A
	if keyboard.getPressed(Key.AbntC1):
		recordedKey=Key.AbntC1
	if keyboard.getPressed(Key.AbntC2):
		recordedKey=Key.AbntC2
	if keyboard.getPressed(Key.Apostrophe):
		recordedKey=Key.Apostrophe
	if keyboard.getPressed(Key.Applications):
		recordedKey=Key.Applications
	if keyboard.getPressed(Key.AT):
		recordedKey=Key.AT
	if keyboard.getPressed(Key.AX):
		recordedKey=Key.AX
	if keyboard.getPressed(Key.B):
		recordedKey=Key.B
	if keyboard.getPressed(Key.Backslash):
		recordedKey=Key.Backslash
	if keyboard.getPressed(Key.Backspace):
		recordedKey=Key.Backspace
	if keyboard.getPressed(Key.C):
		recordedKey=Key.C
	if keyboard.getPressed(Key.Calculator):
		recordedKey=Key.Calculator
	if keyboard.getPressed(Key.CapsLock):
		recordedKey=Key.CapsLock
	if keyboard.getPressed(Key.Colon):
		recordedKey=Key.Colon
	if keyboard.getPressed(Key.Comma):
		recordedKey=Key.Comma
	if keyboard.getPressed(Key.Convert):
		recordedKey=Key.Convert
	if keyboard.getPressed(Key.D):
		recordedKey=Key.D
	if keyboard.getPressed(Key.D0):
		recordedKey=Key.D0
	if keyboard.getPressed(Key.D1):
		recordedKey=Key.D1
	if keyboard.getPressed(Key.D2):
		recordedKey=Key.D2
	if keyboard.getPressed(Key.D3):
		recordedKey=Key.D3
	if keyboard.getPressed(Key.D4):
		recordedKey=Key.D4
	if keyboard.getPressed(Key.D5):
		recordedKey=Key.D5
	if keyboard.getPressed(Key.D6):
		recordedKey=Key.D6
	if keyboard.getPressed(Key.D7):
		recordedKey=Key.D7
	if keyboard.getPressed(Key.D8):
		recordedKey=Key.D8
	if keyboard.getPressed(Key.D9):
		recordedKey=Key.D9
	if keyboard.getPressed(Key.Delete):
		recordedKey=Key.Delete
	if keyboard.getPressed(Key.DownArrow):
		recordedKey=Key.DownArrow
	if keyboard.getPressed(Key.E):
		recordedKey=Key.E
	if keyboard.getPressed(Key.End):
		recordedKey=Key.End
	if keyboard.getPressed(Key.Equals):
		recordedKey=Key.Equals
	if keyboard.getPressed(Key.Escape):
		recordedKey=Key.Escape
	if keyboard.getPressed(Key.F):
		recordedKey=Key.F
	if keyboard.getPressed(Key.F1):
		recordedKey=Key.F1
	if keyboard.getPressed(Key.F10):
		recordedKey=Key.F10
	if keyboard.getPressed(Key.F11):
		recordedKey=Key.F11
	if keyboard.getPressed(Key.F12):
		recordedKey=Key.F12
	if keyboard.getPressed(Key.F13):
		recordedKey=Key.F13
	if keyboard.getPressed(Key.F14):
		recordedKey=Key.F14
	if keyboard.getPressed(Key.F15):
		recordedKey=Key.F15
	if keyboard.getPressed(Key.F2):
		recordedKey=Key.F2
	if keyboard.getPressed(Key.F3):
		recordedKey=Key.F3
	if keyboard.getPressed(Key.F4):
		recordedKey=Key.F4
	if keyboard.getPressed(Key.F5):
		recordedKey=Key.F5
	if keyboard.getPressed(Key.F6):
		recordedKey=Key.F6
	if keyboard.getPressed(Key.F7):
		recordedKey=Key.F7
	if keyboard.getPressed(Key.F8):
		recordedKey=Key.F8
	if keyboard.getPressed(Key.F9):
		recordedKey=Key.F9
	if keyboard.getPressed(Key.G):
		recordedKey=Key.G
	if keyboard.getPressed(Key.Grave):
		recordedKey=Key.Grave
	if keyboard.getPressed(Key.H):
		recordedKey=Key.H
	if keyboard.getPressed(Key.Home):
		recordedKey=Key.Home
	if keyboard.getPressed(Key.I):
		recordedKey=Key.I
	if keyboard.getPressed(Key.Insert):
		recordedKey=Key.Insert
	if keyboard.getPressed(Key.J):
		recordedKey=Key.J
	if keyboard.getPressed(Key.K):
		recordedKey=Key.K
	if keyboard.getPressed(Key.Kana):
		recordedKey=Key.Kana
	if keyboard.getPressed(Key.Kanji):
		recordedKey=Key.Kanji
	if keyboard.getPressed(Key.L):
		recordedKey=Key.L
	if keyboard.getPressed(Key.LeftAlt):
		recordedKey=Key.LeftAlt
	if keyboard.getPressed(Key.LeftArrow):
		recordedKey=Key.LeftArrow
	if keyboard.getPressed(Key.LeftBracket):
		recordedKey=Key.LeftBracket
	if keyboard.getPressed(Key.LeftControl):
		recordedKey=Key.LeftControl
	if keyboard.getPressed(Key.LeftShift):
		recordedKey=Key.LeftShift
	if keyboard.getPressed(Key.LeftWindowsKey):
		recordedKey=Key.LeftWindowsKey
	if keyboard.getPressed(Key.M):
		recordedKey=Key.M
	if keyboard.getPressed(Key.Mail):
		recordedKey=Key.Mail
	if keyboard.getPressed(Key.MediaSelect):
		recordedKey=Key.MediaSelect
	if keyboard.getPressed(Key.MediaStop):
		recordedKey=Key.MediaStop
	if keyboard.getPressed(Key.Minus):
		recordedKey=Key.Minus
	if keyboard.getPressed(Key.Mute):
		recordedKey=Key.Mute
	if keyboard.getPressed(Key.MyComputer):
		recordedKey=Key.MyComputer
	if keyboard.getPressed(Key.N):
		recordedKey=Key.N
	if keyboard.getPressed(Key.NextTrack):
		recordedKey=Key.NextTrack
	if keyboard.getPressed(Key.NoConvert):
		recordedKey=Key.NoConvert
	if keyboard.getPressed(Key.NumberLock):
		recordedKey=Key.NumberLock
	if keyboard.getPressed(Key.NumberPad0):
		recordedKey=Key.NumberPad0
	if keyboard.getPressed(Key.NumberPad1):
		recordedKey=Key.NumberPad1
	if keyboard.getPressed(Key.NumberPad2):
		recordedKey=Key.NumberPad2
	if keyboard.getPressed(Key.NumberPad3):
		recordedKey=Key.NumberPad3
	if keyboard.getPressed(Key.NumberPad4):
		recordedKey=Key.NumberPad4
	if keyboard.getPressed(Key.NumberPad5):
		recordedKey=Key.NumberPad5
	if keyboard.getPressed(Key.NumberPad6):
		recordedKey=Key.NumberPad6
	if keyboard.getPressed(Key.NumberPad7):
		recordedKey=Key.NumberPad7
	if keyboard.getPressed(Key.NumberPad8):
		recordedKey=Key.NumberPad8
	if keyboard.getPressed(Key.NumberPad9):
		recordedKey=Key.NumberPad9
	if keyboard.getPressed(Key.NumberPadComma):
		recordedKey=Key.NumberPadComma
	if keyboard.getPressed(Key.NumberPadEnter):
		recordedKey=Key.NumberPadEnter
	if keyboard.getPressed(Key.NumberPadEquals):
		recordedKey=Key.NumberPadEquals
	if keyboard.getPressed(Key.NumberPadMinus):
		recordedKey=Key.NumberPadMinus
	if keyboard.getPressed(Key.NumberPadPeriod):
		recordedKey=Key.NumberPadPeriod
	if keyboard.getPressed(Key.NumberPadPlus):
		recordedKey=Key.NumberPadPlus
	if keyboard.getPressed(Key.NumberPadSlash):
		recordedKey=Key.NumberPadSlash
	if keyboard.getPressed(Key.NumberPadStar):
		recordedKey=Key.NumberPadStar
	if keyboard.getPressed(Key.O):
		recordedKey=Key.O
	if keyboard.getPressed(Key.Oem102):
		recordedKey=Key.Oem102
	if keyboard.getPressed(Key.P):
		recordedKey=Key.P
	if keyboard.getPressed(Key.PageDown):
		recordedKey=Key.PageDown
	if keyboard.getPressed(Key.PageUp):
		recordedKey=Key.PageUp
	if keyboard.getPressed(Key.Pause):
		recordedKey=Key.Pause
	if keyboard.getPressed(Key.Period):
		recordedKey=Key.Period
	if keyboard.getPressed(Key.PlayPause):
		recordedKey=Key.PlayPause
	if keyboard.getPressed(Key.Power):
		recordedKey=Key.Power
	if keyboard.getPressed(Key.PreviousTrack):
		recordedKey=Key.PreviousTrack
	if keyboard.getPressed(Key.PrintScreen):
		recordedKey=Key.PrintScreen
	if keyboard.getPressed(Key.Q):
		recordedKey=Key.Q
	if keyboard.getPressed(Key.R):
		recordedKey=Key.R
	if keyboard.getPressed(Key.Return):
		recordedKey=Key.Return
	if keyboard.getPressed(Key.RightAlt):
		recordedKey=Key.RightAlt
	if keyboard.getPressed(Key.RightArrow):
		recordedKey=Key.RightArrow
	if keyboard.getPressed(Key.RightBracket):
		recordedKey=Key.RightBracket
	if keyboard.getPressed(Key.RightControl):
		recordedKey=Key.RightControl
	if keyboard.getPressed(Key.RightShift):
		recordedKey=Key.RightShift
	if keyboard.getPressed(Key.RightWindowsKey):
		recordedKey=Key.RightWindowsKey
	if keyboard.getPressed(Key.S):
		recordedKey=Key.S
	if keyboard.getPressed(Key.ScrollLock):
		recordedKey=Key.ScrollLock
	if keyboard.getPressed(Key.Semicolon):
		recordedKey=Key.Semicolon
	if keyboard.getPressed(Key.Slash):
		recordedKey=Key.Slash
	if keyboard.getPressed(Key.Sleep):
		recordedKey=Key.Sleep
	if keyboard.getPressed(Key.Space):
		recordedKey=Key.Space
	if keyboard.getPressed(Key.Stop):
		recordedKey=Key.Stop
	if keyboard.getPressed(Key.T):
		recordedKey=Key.T
	if keyboard.getPressed(Key.Tab):
		recordedKey=Key.Tab
	if keyboard.getPressed(Key.U):
		recordedKey=Key.U
	if keyboard.getPressed(Key.Underline):
		recordedKey=Key.Underline
	if keyboard.getPressed(Key.Unknown):
		recordedKey=Key.Unknown
	if keyboard.getPressed(Key.Unlabeled):
		recordedKey=Key.Unlabeled
	if keyboard.getPressed(Key.UpArrow):
		recordedKey=Key.UpArrow
	if keyboard.getPressed(Key.V):
		recordedKey=Key.V
	if keyboard.getPressed(Key.W):
		recordedKey=Key.W
	if keyboard.getPressed(Key.Wake):
		recordedKey=Key.Wake
	if keyboard.getPressed(Key.WebBack):
		recordedKey=Key.WebBack
	if keyboard.getPressed(Key.WebFavorites):
		recordedKey=Key.WebFavorites
	if keyboard.getPressed(Key.WebForward):
		recordedKey=Key.WebForward
	if keyboard.getPressed(Key.WebHome):
		recordedKey=Key.WebHome
	if keyboard.getPressed(Key.WebRefresh):
		recordedKey=Key.WebRefresh
	if keyboard.getPressed(Key.WebSearch):
		recordedKey=Key.WebSearch
	if keyboard.getPressed(Key.WebStop):
		recordedKey=Key.WebStop
	if keyboard.getPressed(Key.VolumeDown):
		recordedKey=Key.VolumeDown
	if keyboard.getPressed(Key.VolumeUp):
		recordedKey=Key.VolumeUp
	if keyboard.getPressed(Key.X):
		recordedKey=Key.X
	if keyboard.getPressed(Key.Y):
		recordedKey=Key.Y
	if keyboard.getPressed(Key.Yen):
		recordedKey=Key.Yen
	if keyboard.getPressed(Key.Z):
		recordedKey=Key.Z

if recordKeyboard and recordInput==False and recordedKey<>False:
	recordKeyboard=False
	speech.say("Tastendruck ist aufgezeichnet, Wiedergabe kann gestartet werden")
	
if recordKeyboard==False and recordInput==False and recordedKey<>False:
	# Tastedruck ist aufgezeichnet und kann jetzt abgespielt werden
	if keyboard.getKeyDown(Key.LeftAlt) and keyboard.getKeyDown(Key.LeftControl) and keyboard.getKeyDown(Key.P):
		speech.say("Wiedergabe aktiviert, der Tastendruck wird ausgegeben in")
		time.sleep(5)
		speech.say("fünf")
		time.sleep(1)
		speech.say("vier")
		time.sleep(1)
		speech.say("drei")
		time.sleep(1)
		speech.say("zwo")
		time.sleep(1)
		speech.say("eins")
		time.sleep(1)
		keyboard.setPressed(recordedKey)
		speech.say("fertig")

