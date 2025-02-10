import time, codecs, os, shutil, psutil, datetime

# launch NFS:Unbound with different player profiles
# the code can be found on https://github.com/Diogenes232/nfsUnboundProfileLauncher

def readFile(filename):
    datei_IN = False
    try:
        datei_IN = codecs.open(filename, "r", "utf-8")
        return datei_IN.read()
    except Exception as error:
        print ("\nERROR while reading file " + filename + ": " + error)

def changePathToUnixConvention(string):    
    return string.replace(r'\\', '/').replace(r'//', '/')

def writeFile(filename, data):
	try:
		f = open(filename, "w")
		f.write(data)
		f.close()
	except Exception as error:
		print('\nERROR while writing file ' + filename + ': ' + error)

def getSetting(someStr, isResultOneLine):
    someStr = str(someStr).strip()
    settings = readFile(settingsFile)
    settingSearched = []
    found = 0
    for line in settings.splitlines():
        line = str(line).strip()

        if found==0 and someStr in line and len(someStr)==len(line):
            found = 1
        elif found==1:
            if len(line) and not (len(line)==1 and "-" in line):
                settingSearched.append(line)
            else:
                found = 2

    if not len(settingSearched):
        print ("\nerror - no setting found for input '" + someStr + "'\n")
        return False
    elif len(settingSearched)==1 and isResultOneLine == True:
        return settingSearched[0]
    else:
        return settingSearched

def getChoice(choice, allChoices):
	for c in allChoices:
		if (c.startswith(choice.lower())):
			return c
	return ''

def concatSavegameName(gamerName, counter):
	return nfsuSavegamePath + '\\' + gamerName + '-' + str(counter)

def getLastSavegame(gamerName):
	counter = 1
	possibleSavegameName = ''
	
	while (True):
		possibleSavegameName = concatSavegameName(gamerName, counter)
		if (os.path.isfile(possibleSavegameName) == False):
			return counter - 1
		counter += 1

def gameIsRunning():
	try:
		return nfsuExeFile in (p.name() for p in psutil.process_iter())
	except:
		return True

def getModifiedDate(file):
	return str(datetime.datetime.fromtimestamp(os.path.getmtime(file))).split('.')[0]

def ask(question, options):
	result = ''
	while (len(result) == 0):
		typedInput = input(question)
		result = getChoice(typedInput, options)
	return result

def chooseActionWithOldSavegame():
	print("\nFile '1' was found which is the latest state of the game (savegame). ", end='')
	print('It indicates your first start of the launcher OR the last execution did not end properly.', end='')
	print(' What do you want to do with the file?')
	print('use: hold the state & start the game with it (for the player you will choose)')
	print('ignore: it will be ignored and renamed (ignoredState-XY)')
	question = "type 'ignore' or 'use': "
	
	answer = ask(question, ['use','ignore'])
	
	if (answer == 'ignore'):
		resultCounter = getLastSavegame('ignoredState')
		resultSavegameFile = concatSavegameName('ignoredState', resultCounter+1)
		shutil.move(savegameOrphanOrCurrent, resultSavegameFile)

	return answer

def writeNewSettingsFile(filename):
	print("Seems like this is your first start of the 'NFS Unbound Profile Launcher'. Creating a settings file.\nWho are the players for which a profile needs to be created?")
	print("Allowed characters: A-Z a-z 0-9 ! @ # $ % ^ & ( ) - _ + = [ ] { } ; ' , .")
	gamers = []
	gamerName = 'start'
	while (not gamerName == ''):
		print('\n(Player profiles at the moment: ' + ' / '.join(gamers) + ')')
		gamerName = input("Type name of player to add or just press 'Enter' when everyone was added: ")
		if (len(gamerName) > 2):
			gamers.append(gamerName)
		else:
			break
	
	data = 'allGamerNames\n' + '\n'.join(gamers)
	data += '''
-
nfsuSavegamePath
%userprofile%\\OneDrive\\Documents\\Need For Speed(TM) Unbound\\SaveGame\\savegame
'''
	writeFile(filename, data)
	
def prepareDefaultGameStart(gamerName):
	resultCounter = getLastSavegame(gamerName)
	resultSavegameFile = concatSavegameName(gamerName, resultCounter)
	nextSavegameFile = concatSavegameName(gamerName, resultCounter+1)
	if (resultCounter == 0):
		print('\nFor player ' + gamerName + ' was no savegame found. Starting a fresh game.')
	else:
		print('\nSavegame loaded: ' + os.path.basename(resultSavegameFile) + ' (last played: ' + getModifiedDate(resultSavegameFile) + ')')
		shutil.copy2(resultSavegameFile, savegameOrphanOrCurrent)
		
	print('Next savegame will be: ' + os.path.basename(nextSavegameFile))
	
	return nextSavegameFile
	
def prepareResumingGameStart(gamerName):
	resultCounter = getLastSavegame(gamerName)
	nextSavegameFile = concatSavegameName(gamerName, resultCounter+1)
	return nextSavegameFile

def startNfs():
	print('\nStarting the game')
	os.system('"' + nfsuExeFile + '"')
	print('NFS:Unbound started', end='')
	
	wasGameStartDetected = False
	startTime = time.time()
	
	while(not wasGameStartDetected or gameIsRunning()):
		print('.', end='')
		if (not wasGameStartDetected and gameIsRunning()):
			wasGameStartDetected = True
			print('->', end='')
		time.sleep(checkIfGameIsRunningEveryXSeconds)
	print('quit (after ' + str(int((time.time()-startTime)/60)) + ' min.)')
	
	#input('\nYou did a good job? PRESS ENTER to preserve the savegame!\nOtherwise just close this window..')
	print('\nHope you had fun!')

os.system('cls')
print('\nWelcome to NFS:Unbound profile launcher')

# constants
checkIfGameIsRunningEveryXSeconds = 7
settingsFile = "nfsUnbound_ProfileLauncher_settings.txt"
nfsuExeFile = "NeedForSpeedUnbound.exe"

# check if game was ever started // detect first launch
if (os.path.isfile(settingsFile) == False):
	writeNewSettingsFile(settingsFile)

# load settings
allGamerNames = getSetting("allGamerNames", False)
nfsuSavegamePath = getSetting("nfsuSavegamePath", True).replace('%userprofile%', os.environ['USERPROFILE'])
savegameOrphanOrCurrent = nfsuSavegamePath + '\\1'

detectedPreviousGameStateFile = os.path.isfile(savegameOrphanOrCurrent)

# detect if file '1' is there (which is unexpected)
choice = ''
if (detectedPreviousGameStateFile):
	choice = chooseActionWithOldSavegame()

# ask for current player
print('\nAvailable players (from settings file): ' + ' / '.join(allGamerNames))
gamerName = ask('Who wants to play? ', allGamerNames)

nextSavegameFile = ''
if (detectedPreviousGameStateFile == False or (detectedPreviousGameStateFile and choice == 'ignore')):
	nextSavegameFile = prepareDefaultGameStart(gamerName)
else:
	nextSavegameFile = prepareResumingGameStart(gamerName)

# start the game
startNfs()

print ("Saving as: " + os.path.basename(nextSavegameFile))
shutil.move(savegameOrphanOrCurrent, nextSavegameFile)

print('\nSee you next time /w NFS:Unbound')
print('(you can close the window now)')
time.sleep(120)
