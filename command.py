import os

count = 0
lines = []

for c in range(36, 207):
    lines.append("opencv_createsamples -img "+str(c)+"img.jpg -num 200 -vec feel"+str(c)+".vec -w 20 -h 20 -bg ../beege.txt -maxxangle 0.6 -maxyangle 0 -maxzangle 0.3 -maxidev 100 -bgcolor 0 -bgthresh 0\n")
#    lines.append(command)
#    file.write("negatives/"+line.rstrip())
with open('command.sh', 'a') as f:
    for l in lines:
        f.write(l)
    f.close()
