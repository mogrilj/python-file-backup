import ftplib
import os
import glob
import shutil
import json
from time import gmtime, strftime

USEROS = "\\"#Windows=\\ Mac&Linux = /
COMMANDS = ['add remote [remoteName] [ftpUrl] [ftpUsername] [ftpPassword]', 'backup [pathToDirectory]', 'cd [directory]', 'dir', 'exit', 'help', 'ls', 'quit']

#creates remotes.txt file



open("remote.txt","w").close()

pathToRemote = os.getcwd()

BACKUP = ""
UPLOADFILES =[]


def addRemote(remoteData):
    #remote name
    remoteName = remoteData[0]
    
    ftpUrl = remoteData[1]
    #FTP username
    ftpUsername = remoteData[2]
    #FPT password
    ftpPassword = remoteData[3]

    #create REMOTES and or loads old data into it
    f = open(pathToRemote+"/remotes.txt","r")
    text = f.read() 
    bool = len(text)> 0
    if bool:
        remote = json.loads(text)
    else:
        remote = {}
    f.close()
    #create REMOTES dictonary entry

    
    remote[remoteName]={
        'ftpUrl':ftpUrl,
        'ftpUsername':ftpUsername,
        'ftpPassword':ftpPassword
    }
    
   
    #saves the new data in remotes.txt
    #In that pattern
    '''
    REMOTE["remotename"]{
        ftpUrl:'value'
        ftpUsername:'value'
        ftpPassword:'value'
        }
    '''
    remotes = open(pathToRemote+"/remotes.txt","w")
    remotes.write(json.dumps(remote))
    remotes.close()

  
    print("Remote succsessfully added!")


def ls():
    for i in glob.glob("*"):
        print(i)

def cd(directory):
    try:
        os.chdir(directory)

    except:
        print("Couldn't find directory '"+directory+"'")
        
def createBackup(directory):
    global BACKUP
    #Make zipfile
    shutil.make_archive(directory+"-Backup-"+strftime("%Y-%m-%d", gmtime()), 'zip', directory)
    #set backuplink to new zipfile
    BACKUP = directory+"-Backup-"+strftime("%Y-%m-%d", gmtime())+".zip"
    print(BACKUP)
    print("Backup created succsessfully!Use commit to load it to the server!")
    
    

    
def showRemotes():
    
    f = open(pathToRemote+"/remotes.txt","r")
    text = f.read()
    if text != "":
        REMOTELIST = json.loads(text)
        f.close()
    
        for key in REMOTELIST:
            print(key)
            print("-"+REMOTELIST[key]["ftpUrl"])
            print("-"+REMOTELIST[key]["ftpUsername"])   
            print("-"+REMOTELIST[key]["ftpPassword"])
    else:
        print("No remotes added yet!")
        
def commit(remote):
    global BACKUP
    #Get remotes
    f = open(pathToRemote+"\\remotes.txt","r")
    REMOTELIST = json.loads(f.read())
    f.close()
      
    #Connect so server via FTP   
    ftp = ftplib.FTP(REMOTELIST[remote]['ftpUrl'])
    ftp.login(REMOTELIST[remote]["ftpUsername"],REMOTELIST[remote]["ftpPassword"])
    #Kann eventuell entfernt werden
    #Naviagted to direcotries with permission
    ftp.cwd("web/"+REMOTELIST[remote]["ftpUrl"]+"/htdocs")
    if BACKUP != "":
        #Get the backup files from your drive
        backupFile = open(BACKUP,"rb")
        #Load the file to the server
        ftp.storbinary("STOR "+BACKUP,backupFile)
        ftp.quit()
        print("Backup was succsessfully uploaded to "+REMOTELIST[remote]['ftpUrl']+" under the filename "+BACKUP)
    else:
        print("Files to upload couldn't be found!")



           


while True:
    print("$ "+os.getcwd())
    command = input("")
    if command[0:10] == "add remote":
        lst = command.split(" ")
        #[2] = RemoteName [3] = ftpAddress [4]= ftpUsername [5] = ftpPassword
        addRemote([lst[2],lst[3],lst[4],lst[5]])

    if command == "help":
        for item in COMMANDS:
            print("-"+item)
            
    if command == "ls" or command == "dir":
        ls()

    if command == "remotes":
        showRemotes()
        
    if command[0:2]== "cd":
       cd(command[3:len(command)])
        
    if command[0:6] == "backup":
        lst = command.split(" ")
        createBackup(lst[1])

    if command.split(" ")[0] == "commit":
        commit(command.split(" ")[1])
    if command == "exit" or command == "quit":
        print("Goodbey!")
        break
    
    

