import os

print('what resource?')
resource = input()

cmd_parts = ['oc set env '+resource]

with open('.env', 'r') as reader:
    for line in reader.readlines():
        if (line == "\n"):
            continue
        
        if (line.strip()[0] == '#'):
            continue

        cmd_parts.append(line.strip())
        # [key, value] = line.split('=')
        # print(key+' : '+value)
        
command = ' '.join(cmd_parts)

print('executing "'+command+'"')
os.system(command)

