
from tkinter import ttk
import os,sys
from threading import Thread
from .ValAgents import ValAgents

try:
    import valclient
except ImportError:
    os.system('pip install valclient')

try:
    import colorama
except ImportError:
    os.system('pip install colorama')

try:
    import pystyle
except ImportError:
    os.system('pip install pystyle')

try:
    import tkinter
except ImportError:
    os.system('pip install tkinter')


from valclient.client import Client
from colorama import *
from pystyle import *
import tkinter as tk

def mt(titre):
    if os.name == 'nt':
        os.system(f"title {titre}")
    else:
        print("La modification du titre de la console n'est pas supportée sur ce système d'exploitation.")


titre = "Kamilock"
mt(titre)

os.system('cls')

intro = """


 ▄▄▄▄ ▓██   ██▓    ██ ▄█▀▄▄▄       ███▄ ▄███▓ ██▓
▓█████▄▒██  ██▒    ██▄█▒▒████▄    ▓██▒▀█▀ ██▒▓██▒
▒██▒ ▄██▒██ ██░   ▓███▄░▒██  ▀█▄  ▓██    ▓██░▒██▒
▒██░█▀  ░ ▐██▓░   ▓██ █▄░██▄▄▄▄██ ▒██    ▒██ ░██░   by.kami on discord
░▓█  ▀█▓░ ██▒▓░   ▒██▒ █▄▓█   ▓██▒▒██▒   ░██▒░██░
░▒▓███▀▒ ██▒▒▒    ▒ ▒▒ ▓▒▒▒   ▓▒█░░ ▒░   ░  ░░▓  
▒░▒   ░▓██ ░▒░    ░ ░▒ ▒░ ▒   ▒▒ ░░  ░      ░ ▒ ░
 ░    ░▒ ▒ ░░     ░ ░░ ░  ░   ▒   ░      ░    ▒ ░
 ░     ░ ░        ░  ░        ░  ░       ░    ░  
      ░░ ░                                       
                >Press Enter <3
      
"""


Anime.Fade(Center.Center(intro), Colors.black_to_red, Colorate.Vertical, interval=0.035, enter=True)

class GUI():
    def __init__(self):
        self.reg=["North America","Europe","Brazil","Korea","Latin America","Asian Pacific"]
        self.regions=["NA","EU","BR","KR","LATAM","AP"]
        self.agents=[]
        try:
            self.agentSelect = ValAgents()
            lis=[]
            for i in self.agentSelect.get_agents():
                lis.append(str(i))
            self.agents=sorted(lis)
        except: #list of agents if api does not grab them
            self.agents=["Astra","Breach","Brimstone","Chamber","Cypher","Fade","Harbor","Jett","Kay/O","Killjoy","Neon","Omen","Phoenix","Raze","Reyna","Sage","Skye","Sova","Viper","Yoru","Deadlock"]
        self.currAgent="Astra"
        
        self.indCombo=self.getInt()
        # self.indCombo=1
        self.currRegion=self.regions[self.indCombo].lower()
        self.runnable = Thread(target=self.agentLock)
        self.running=True
        try:
            self.client=Client(region=self.currRegion)
            self.client.activate()
        except:
            self.client=None
        self.run()

    def on_select(self,event):

        try:
            region=self.reg.index(event.widget.get())
            if str(self.regions[region]).lower() != self.currRegion:
                self.currRegion= str(self.regions[region]).lower()
                self.client=Client(region=self.currRegion)
                self.client.activate()
        except:
            pass


    def get_client(self):
        while self.client==None:
            try:
                self.client=Client(region=self.currRegion)
                self.client.activate()
                print("success")
            except Exception as e:
                self.client=None #automatically makes region otherwise

        
    def agentLock(self,start,stop,cb1,cb2):
        agent=self.currAgent

        seenMatches=[]
        try:
            uuid=str(self.agentSelect.get_agent(agent).uuid) #tries grabs from api (will work even after they add new agents)
        except:
            uuid=agents[agent] #uses dict of agents (wont work for newer agents)
        while self.running:

            try:

                sessionState = self.client.fetch_presence(self.client.puuid)['sessionLoopState']
                if ((sessionState == "PREGAME") and (self.client.pregame_fetch_match()['ID'] not in seenMatches)):
                    self.client.pregame_select_character(uuid)
                    self.client.pregame_lock_character(uuid)

                    self.killLook(start,stop,cb1,cb2) #stops after locking
            except Exception as e:
                print('', end='') # Using pass caused weird behavior


    def getInt(self):
        
        #try #1
        #works if they have started valorant
        try:
            client = Client(region="eu") #using na for default
            client.activate()

            h=client.riotclient_session_fetch_sessions()
            for i in h[list(h.keys())[0]]["launchConfiguration"]["arguments"]:
                if("-ares-deployment" in i):
                    v=i.split("=")
                    v=v[-1].upper()
            if(v in self.regions):
                return self.regions.index(v)
            else:
                pass
        except Exception as e:
            pass

        #try 2
        #Look line by line in logs and try to find region
        try:
            for i in range(1):
                inf=os.getenv("LOCALAPPDATA") +"\VALORANT\Saved\Logs\ShooterGame.log" #location of normal val logs // attempt #2 of retrieving region
                with open(inf) as f:
                    f = f.readlines()
                for line in f:
                    if "pvp" in line:
                        line=line.split()
                        for reg in self.regions:
                            for i in line:
                                if reg.lower()+".a.pvp" in i: #test against prob very inefficient
                                    return self.regions.index(reg)
        except Exception as e:
            pass
        return 0 #returns North American if other 2 dont work                     


    def resource_path(self, relative_path):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path.replace('/', '\\'))

    def run(self):
        root= tk.Tk()
        # icon=tk.PhotoImage(self.resource_path("1.ico"))
        root.iconbitmap(self.resource_path("images\\1.ico"))
        root.title("Instalock - ByKami")
        
        root.geometry("250x200")
        label1=tk.Label(text="Region (Change if incorrect): ")
        label1.pack()

        #regions
        combobox=ttk.Combobox(root,values=self.reg)
        combobox.current(self.indCombo)
        combobox.bind("<<ComboboxSelected>>", self.on_select) 
        combobox.pack()
        combobox.state(['readonly'])



        label2=tk.Label(text="Agent: ")
        label2.pack()

        #agents
        combobox2=ttk.Combobox(root,values=self.agents)
        combobox2.current(self.indCombo)
        combobox2.pack()
        combobox2.state(['readonly'])
        
        start=ttk.Button(root,text="Start",command=lambda: self.startLook(start,stop,combobox,combobox2))
        start.pack()

        stop=ttk.Button(root,text="Stop")
        stop.pack()
        stop.config(state='disable',command=lambda: self.killLook(start,stop,combobox,combobox2))


        # start.
        if(self.client==None):
            x=Thread(target=self.get_client)
            x.start()
            
        
        root.protocol("WM_DELETE_WINDOW",lambda: self.killAll(root)) #kills the window and the thread if active on closing
        root.mainloop()

    def startLook(self,start,stop,cb1,cb2):
        self.currAgent=cb2.get()

        self.runnable = Thread(target=self.agentLock,args=(start,stop,cb1,cb2))
        start.config(state='disable')
        stop.config(state='active')
        cb1.config(state='disable')
        cb2.config(state='disable')
        
        self.running=True
        self.runnable.start()
    def killAll(self,root):
        self.running=False#kills second thread
        root.destroy()
        self.client='na' #kills first thread
    def killLook(self,start,stop,cb1,cb2):
        start.config(state='active')
        stop.config(state='disable')
        cb1.config(state='readonly')
        cb2.config(state='readonly')
        self.running=False


def main():
    agents ={#If API req goes down 
    "Astra" : "41fb69c1-4189-7b37-f117-bcaf1e96f1bf",
    "Breach" : "5f8d3a7f-467b-97f3-062c-13acf203c006",
    "Brimstone" : "9f0d8ba9-4140-b941-57d3-a7ad57c6b417",
    "Chamber" : "22697a3d-45bf-8dd7-4fec-84a9e28c69d7",
    "Cypher" : "117ed9e3-49f3-6512-3ccf-0cada7e3823b",
    "Fade" : "dade69b4-4f5a-8528-247b-219e5a1facd6",
    "Harbor" : "95b78ed7-4637-86d9-7e41-71ba8c293152",
    "Jett" : "add6443a-41bd-e414-f6ad-e58d267f4e95",
    "Kay/O" : "601dbbe7-43ce-be57-2a40-4abd24953621",
    "Killjoy" : "1e58de9c-4950-5125-93e9-a0aee9f98746",
    "Neon" : "bb2a4828-46eb-8cd1-e765-15848195d751",
    "Omen" : "8e253930-4c05-31dd-1b6c-968525494517",
    "Phoenix" : "eb93336a-449b-9c1b-0a54-a891f7921d69",
    "Raze" : "f94c3b30-42be-e959-889c-5aa313dba261",
    "Reyna" : "a3bfb853-43b2-7238-a4f1-ad90e9e46bcc",
    "Sage" : "569fdd95-4d10-43ab-ca70-79becc718b46",
    "Skye" : "6f2a04ca-43e0-be17-7f36-b3908627744d",
    "Sova" : "320b2a48-4d9b-a075-30f1-1f93a9b638fa",
    "Viper" : "707eab51-4836-f488-046a-cda6bf494859",
    "Yoru" : "7f94d92c-4234-0a36-9646-3a87eb8b5c89",
    "Deadlock" : "cc8b64c8-4b25-4ff9-6e7f-37b4da43d235",
    # You can add ISO here.
    }
    


    p = GUI()

if __name__ == "__main__":
    main()



# import tkinter as tk
# from tkinter import ttk
# from valclient.client import Client
# import os,sys
# from threading import Thread
# from ValAgents import ValAgents
# client = Client(region="na") #using na for default
# client.activate()
