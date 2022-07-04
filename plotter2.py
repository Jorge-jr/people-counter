devices = []

with open('captures.txt') as caps:
    lines = caps.readlines()
    for line in lines:
        #print(line.split(' ')[2])
        if line.split(' ')[2] not in devices:
            devices += [line.split(' ')[2]]


print(devices)
print(len(devices))