# Need for Speed: Unbound - Profile Launcher
Command line tool to manage multiple offline player accounts in NFS Unbound on Windows.

With this tool you can decide before starting NFS which profile to load (which player will play).

### Game states of the offline mode
I did not check how it reacts to online games because I just started the career a few weeks ago.

## Installation
You can install Python3 and compile the .py file yourself or just use the compiled application file:
Download the `nfsUnbound_ProfileLauncher.exe` from the `dist` directory to the directory where your game files are located (e.g. `C:\Games\EA - Games\Need for Speed Unbound`).
Run nfsUnbound_ProfileLauncher.exe - it will ask you which profiles you want to create. The settings are now saved in the file `nfsUnbound_ProfileLauncher_settings.txt`. It contains the created profiles and the path to your actual savegames (the default should work on most PCs).
If it finds a savegame there, it will ask you if you want to keep it (the next player will get the savegame state) or ignore it (everyone will start a new game).
After choosing which profile to start, the game will start.

## Default routine of the launcher
Run nfsUnbound_ProfileLauncher.exe, enter your profile name and the game will automatically start with your last savegame state.
The launcher detects if the game is running. When you quit NFS Unbound it will assign the current savegame to your profile (and explains what it does).
You can close the launcher or wait for it to close.

## Further information
NFS Unbound normally contains a savegame file named `C:\Users\UserNameXYZ\OneDrive\Documents\Need For Speed(TM) Unbound\SaveGame\savegame\1`. This launcher works with this file and manages the game states:
yourProfile-1
yourProfile-2
yourProfile-3
anotherProfile-1
anotherProfile-2
A new file is saved after each game session. So you have the chance to remove the last savegame file... or try something new and rename the latest savegame file to `ferrari-testarossa` to pick that state up at some point in the future.