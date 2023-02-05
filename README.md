KeyRepeat Version 1.0a
Author: https://github.com/mw-wood

========== Description ===========

A multi-threaded program to record and repeat a set of given inputs.

========== Motivation ===========

Me and my friends have played games where we could benefit from
macros based on whats happening on screen. Therefore, I
created a program to facilitate this.

======== Package Contents =========

Scripts folder to contain inputs.
main.py program.
config.json file.
OUTPUT.txt log file.

======== Usage =========

Note: Whilst you can record key and mouse inputs simultaniously,
the following are disallowed:
  .Shortcuts
  .Mouse dragging
  .Mouse holding
 
For example, this would make sprinting in games that require Shitft + W
impossible.

These features will be possible in the near future.

Recording:
  1) Launch the main.py file.
  2) Press "record" and input your macro.
  3) Press ESC when finished.

Running:
  1) If you want to repeat your macro, tick record.
  2) Press Run.
  3) To exit the macro, press ESC.
 
Programming:
  You may also write a text file instead of recording.
  
  The query structure is:
  command key duration x y

  For example: key_press e 0.5
               mouse_press left 0.5 567 1028
               do mouse_wait 1.65
  
  For key presses, x and y are optional.
  
  Keyboard commands:
    key_press - presses the key for the specified duration.
    do key_wait - waits for the specified duration. No button field required.
  Mouse commands:
    mouse_press - presses the mouse for the specified duration.
    do mouse_wait - waits for the specified duration. No button field required.

====== Feature List =======

.Threading
.Logging
.Input automation
.Image recognition

TODO:

.Image recognition
.file explorer to select image and presets
.shortcuts
.mouse drag
.mouse hold
.UI to build script rather than txt file
