import sys , os , discord , subprocess , json , io , random  ,time ,numpy,glob,asyncio , mal
from songdownloader import download_song

botid = ""

#file variables
f = io.open("call.json", mode="r", encoding="utf-8")
filesend = None
is_printinglogs = False

#reply handling variables
flag = False
anime_flag = False
secondary_flag = False
rep_pkg = json.load(f)
anime_reply = False
asrc = None
change_status = False

#uselessly useful variables
spc = " "
client = discord.Client()
oldfile = []
statustxt = "Help me ☠"



def system_call(command):
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()
    return (output,err)

@client.event
async def on_ready():
    global oldfile
    print("Bot's Up and runnin bois")
    activity = discord.Game(name=statustxt)
    await client.change_presence(status=discord.Status.online, activity=activity)


@client.event
async def on_message(message):
    #important Transfer variables
    global flag,filesend,anime_flag,change_status

    if(change_status):
        change_status = False
        activity = discord.Game(name=statustxt)
        await client.change_presence(status=discord.Status.online, activity=activity)

    if( message.author.id == client.user.id ):
        return
    if(message.author.bot):
        return
    to_reply = important_functions(message)


    #handle conversion after important duties
    #Replies handler
    for x in message.mentions:
        if(x==client.user):
           await message.channel.send(random.choice(rep_pkg["convos"]["calling"])+spc +  message.author.mention + spc + random.choice(rep_pkg["emojicons"]["adoring"]))



    if(to_reply == None):
        to_reply = single_starter_replies(message)

    if(anime_flag):
        embed=discord.Embed(title=asrc[0].title, description=f"[{asrc[0].type}]")
        embed.set_author(name=asrc[0].title)
        embed.set_thumbnail(url=asrc[0].image_url)
        embed.add_field(name="Rating", value=asrc[0].score, inline=False)
        embed.add_field(name="Episodes", value=asrc[0].episodes, inline=True)
        embed.add_field(name="Synopsis", value=asrc[0].synopsis, inline=True)
        embed.set_footer(text="data scraped from myanimelist")
        anime_flag = False
        await message.channel.send(embed=embed)

    try:
        if(to_reply != None):
            await message.channel.send(to_reply)
            await message.add_reaction("😉")
            
            if(filesend != None):
                await message.channel.send(file=discord.File(filesend))
                system_call("rm "+filesend)
                filesend = None
            return
    except:
        await client.change_presence(status=discord.Status.online, activity=activity)
        await message.add_reaction("😒")
    


def important_functions(message):
    global anime_flag,asrc,change_status,statustxt,filesend
    if(message.content.startswith("!upload")):
        nameOfFile = str(message.content)[8:]
        print(nameOfFile)
        #files = os.listdir('./music/')
        files = os.listdir('.')
        print(files)
        print((nameOfFile in list(files)))
        for name in files:
            print(str(name))
            if(nameOfFile in str(name)):
                filesend = name
                return "Uploading {}".format(str(name)) + spc + random.choice(rep_pkg["emojicons"]["adoring"])

        return "404 whoopsie" + spc + random.choice(rep_pkg["emojicons"]["broken"])
    
    if(message.content.startswith("!anime")):
        asrc = [" "]
        animestr = str(message.content)[6:]
        try:
            asrc = mal.AnimeSearch(animestr).results
            anime_flag = True;

        except ValueError:
            return f"No results found for {animestr}"

    if(message.content.startswith("!setstatus")):
        change_status = True
        try:
            statustxt = str(message.content)[10:20]
        except:
            return "Um i cant seem to set that as my status m8" + random.choice(rep_pkg["emojicons"]["sed"])

    if(message.content.startswith("!song")):
        sngname = str(message.content)[5:]
        download_song(sngname)
        files = os.listdir('.')
        
        nameOfFile = sngname.lower().replace(" ","")
        print(nameOfFile)
        #files = os.listdir('./music/')
        files = os.listdir('.')
        print(files)
        print((nameOfFile in list(files)))
        for name in files:
            print(str(name))
            if(nameOfFile in str(name).lower().replace(" ","")):
                filesend = name
                return "Uploading {}".format(str(name)) + spc + random.choice(rep_pkg["emojicons"]["adoring"])

        return "```diff\n -404 whoopsie```" + spc + random.choice(rep_pkg["emojicons"]["broken"])



def single_starter_replies(message):
    global flag,ispaused,filesend  
    if(message.content.startswith("!cmd")):
        if(any(msg in message.content.lower() for msg in rep_pkg["blocked_commands"]) or any(msg in message.content.lower() for msg in rep_pkg["prohibited_commands"]) or any(msg in message.content.lower() for msg in rep_pkg["infiniteloops"])):
            return "Temporary command blocked ⚡💀"
        try:
            return f"```{str(system_call(str(message.content)[4:])[0].decode(encoding='UTF-8',errors='strict'))}```"
        except:
            try:
                return f"```{str(system_call(str(message.content)[4:])[1])}```"
            except:
                return "Something broke?"

    elif("listen here you little shit" in message.content.lower() or "little shit" in message.content.lower()):
        filesend = "littleshit.png"
        return "How Dare you" + spc + random.choice(rep_pkg["emojicons"]["sed"])



    elif(((any(msg in message.content.lower() for msg in rep_pkg["triggers"]["emojitrigger"])) and flag) and randomizer(5)):
        ispaused = True
        return random.choice(rep_pkg["convos"]["Cantuseemoji"]) + spc + random.choice(rep_pkg["emojicons"]["fakku"] )

    elif(((any(msg in message.content.lower() for msg in rep_pkg["triggers"]["stopreal"])) and flag) and randomizer(10)):
        return random.choice(rep_pkg["convos"]["pausing"])+spc +  message.author.mention  + spc + random.choice(rep_pkg["emojicons"]["sed"])
    
    elif(((any(msg in message.content.lower() for msg in rep_pkg["triggers"]["simp"])) and flag) and randomizer(5)):
        return random.choice(rep_pkg["convos"]["simpreply"])+spc +  message.author.mention  + spc + random.choice(rep_pkg["emojicons"]["fakku"])

    elif(((any(msg in message.content.lower() for msg in rep_pkg["triggers"]["reallove"])) and flag) and randomizer(5)):
        return random.choice(rep_pkg["convos"]["breaking4wall"]) + spc + random.choice(rep_pkg["emojicons"]["adoring"])

    elif(((any(msg in message.content.lower() for msg in rep_pkg["triggers"]["reallove"])) and flag) and randomizer(10)):
        return random.choice(rep_pkg["convos"]["breaking4wall"]) + spc + random.choice(rep_pkg["emojicons"]["adoring"])

    elif(((any(msg in message.content.lower() for msg in rep_pkg["triggers"]["botstupidity"])) and flag) and randomizer(5)):
        return random.choice(rep_pkg["convos"]["scolding_reply"]) + spc + random.choice(rep_pkg["emojicons"]["scolding"])

    elif(((any(msg in message.content.lower() for msg in rep_pkg["triggers"]["praise"])) and flag) and randomizer(10)):
        return random.choice(rep_pkg["convos"]["praise_reply"]) + spc + random.choice(rep_pkg["emojicons"]["adoring"])

    elif(message.content.startswith("!python")):
        pyscript = f"""python3 -c '{str(message.content)[7:]}'"""
        print(pyscript)
        shell_out = system_call(pyscript)
        try:
            scriptout = str(shell_out[0].decode())
            print(scriptout)
        except:
            scriptout = "Something Failed"+spc + random.choice(rep_pkg["emojicons"]["broken"]) + "\n" + str(shell_out[1])
        return scriptout
    elif(randomizer(50)):
        return random.choice(rep_pkg["convos"]["jokes"])
    elif(((any(msg in message.content.lower() for msg in rep_pkg["triggers"]["nice_trig"])) and len(message.content) < 10) and randomizer(5)):
        return random.choice(rep_pkg["triggers"]["nice_trig"]) + spc + random.choice(rep_pkg["emojicons"]["smirk"])
    elif((any(msg in message.content.lower() for msg in rep_pkg["triggers"]["nums"])) and len(message.content) < 7 and randomizer(6)):
        return random.choice(rep_pkg["convos"]["numreply"]) + spc + random.choice(rep_pkg["emojicons"]["smirk"])
    elif(((any(msg in message.content.lower() for msg in rep_pkg["triggers"]["oof"])) and len(message.content) < 7) and randomizer(10)):
        return random.choice(rep_pkg["triggers"]["oof"]) + spc + random.choice(rep_pkg["emojicons"]["smirk"])
    elif((any(msg in message.content.lower() for msg in rep_pkg["triggers"]["savemsg"])) and randomizer(10)):
        return random.choice(rep_pkg["triggers"]["savemsg"])
    if((message.content.lower().startswith('um') or message.content.lower().startswith('ok') or message.content.lower().startswith('omfg') ) and randomizer(10)):
        flag = True
        if(randomizer(100)):
            return random.choice(rep_pkg["convos"]["hmm"])  
    else:
        flag = False
    time.sleep(1)

def randomizer(prob):
    if(random.randint(1,prob) == 1):
        return True
    else:
        return False

client.run(botid)
