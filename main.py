import curses
from curses import wrapper
import argparse
import os
import json

#necessary arguments
parser = argparse.ArgumentParser()
parser.add_argument('--id', type=str, required=False, help='Load flash cards using an ID')
parser.add_argument('--file', type=str, required=False, help='Load flash cards using a JSON file')
args = parser.parse_args()
size = os.get_terminal_size()

#def mac win size = 80x24

def fetchlist(info, forid):
    if forid == 'id' and info == 'debug':
        list = [
            ["word1", "this is the definition for word one"],
            ["word2", "this is the definition for word two"],
            ["word3", "this is the definition for word three"],
            ["word4", "this is the definition for word four"]
        ]
        return list
    if forid == 'file':
        jsonlist = open(info)
        jsonlist2 = json.loads(jsonlist.read())
        jsonlist.close()
        list = []
        for k, v in jsonlist2.items():
            list.append([k, v])
        return list

def renderinpad(pad, string):
    for char in string:
        pad.addstr(char)

def rendermain(stdscr, string):
    stdscr.clear()
    stdscr.addstr(0, 0, 'q to leave')
    stdscr.addstr(22, 24, '<- Go left - |_| Flip - Go right -> ')
    stdscr.refresh()
    winone = curses.newwin(20, 78, 2, 1)
    pad = curses.newpad(18, 73)
    #refresh(pad xpos for text, pad ypos for text, 1cornery, 1cornerx, 2cornery, 2cornerx)
    winone.border()
    #pad.addstr(string)# {}'.format(x))
    renderinpad(pad, string)
    winone.refresh()
    pad.refresh(0, 0, 3, 2, 24, 74)

def mainhelp(stdscr):
    # Clear screen
    rendermain(stdscr,'                                                       _\n              _                                       | |\n             | |_   ____  _   _  ____  ____   ____  _ | |  ___\n             |  _) / _  )( \ / )/ ___)/ _  | / ___)/ || | /___)\n             | |__( (/ /  ) X (( (___( ( | || |   ( (_| ||___ |\n              \___)\____)(_/ \_)\____)\_||_||_|    \____|(___/ \n\n\n                   to load cards: texcards --id [id]\n                to load JSON file: texcards --file [file]\n\n                        press any key to quit\n')
    stdscr.getch()
    quit()


def main(stdscr):
    #flippedefault = false
    state = False
    pos = 0
    if args.id != None:
        list = fetchlist(args.id, 'id')
    elif args.file != None:
        list = fetchlist(args.file, 'file')
    while True:
        if not state:
            rendermain(stdscr, list[pos][0])
        elif state:
            rendermain(stdscr, list[pos][1])
        t = stdscr.getch()
        if t == 81 or t == 113:
            break
        elif t == 32:
            state = not state
        elif t == curses.KEY_RIGHT and pos < len(list) - 1:
            pos += 1
            state = False
        elif t == curses.KEY_RIGHT and pos == len(list) - 1:
            pos = 0
            state = False
        elif t == curses.KEY_LEFT and pos > 0:
            pos -= 1
            state = False
        elif t == curses.KEY_LEFT and pos == 0:
            pos = len(list) - 1
            state = False

            

    

if size[0] < 80 or size[1] < 24:
    print('Program unable to launch, Reqired size for this program is 80 columns by 24 rows')
    quit()
if size[0] > 80 or size[1] > 24:
    inp = str(input("Recommended size for this program is 80 columns and 24 rows, proceed? Y/n"))
if args.id == None and args.file == None:
    wrapper(mainhelp)
else:
    wrapper(main)
