import json
from shlex import shlex
import re
import sys

def parse_kv_pairs(text, item_sep=" ", value_sep="="):
    lexer = shlex(text, posix=True)
    lexer.whitespace = item_sep
    lexer.wordchars += value_sep + ":().{}\"'_-/"
    d = {}
    for w in lexer:
        try:
            a,b =  w.split(value_sep, maxsplit=1)
            if(a == 'msg' and not b.startswith("audit")):
                d[a] = parse_kv_pairs(b)
            else:
                d[a] = b
        except:
            pass
    return d
    #return dict(word.split(value_sep, maxsplit=1) for word in lexer)


# file = open("aduitdemo.txt","r")


'''
Method 1 || Drawback :: msg gets overwritten
for line in file.readlines():
    line = line.strip();
    print(parse_kv_pairs(line))
file.close()
'''

# msg gets overwritten 
def parse1(fname):
    file = open(fname,"r")
    for line in file.readlines():
        line = line.strip();
        line.replace('\x1d',' ')
        print(parse_kv_pairs(line))
    file.close()


# override fixed
def parse2(fname):
    file = open(fname,"r")
    for line in file.readlines():
        line = line.strip();
        line.replace('\x1d',' ')
        tkns = line.split('):')
        tt = re.findall(r'type=(.*) msg=audit\((\d*.\d*):(\d*)',tkns[0])
        
        j = {}
        j['srn'] = tt[0][2]
        j['ts'] = tt[0][1]
        j['type'] = tt[0][0]
        j['data'] = parse_kv_pairs(tkns[1])
        print(j)
        #print(parse_kv_pairs(tkns[1]))
    file.close()

# parse2('audit_1625813282.log')

if __name__ == '__main__':
    if(len(sys.argv) > 1):
        parse2(sys.argv[1])
    else:
        print("Please provide the log file in the cmdline")
    # parse2("aduitdemo.txt")
    # main()