very basic drawing tool I use as a scratch pad.
features:
- infinite panning and zooming
- no gui, everything is controlled by hotkeys
- everything is vector graphics

if you want to use it yourself:
- `pip install -r requirements.txt` and `python chalkboard.py`
- edit `configs/default.json` with your desired settings, should be pretty self-explanatory

if someone wants to add a setup.py script, you can submit a pr

see the controls section of the default config file for controls

also, I have tested it on the following OSes:
- Windows: works fine (using 2x global scaling), although the taskbar icon is a python thing and not the piece of chalk
- Manjaro Linux: works fine, but stuff is zoomed out and a bit slower b/c no global scaling, the zooming thing can be fixed by changing some settings, but i should maybe add scaling built into it
- Mac: Exact same situation as Manjaro