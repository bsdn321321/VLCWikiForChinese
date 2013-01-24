import os
filelist=os.popen('find -name \'*.md\'').readlines()
cmd1=''
cmd2=''
cmd3=''
for filename in filelist:
    filename=filename[2:-4]
    cmd1='echo "<html><head><meta http-equiv=\\"Content-Type\\" content=\\"text/html; charset=UTF-8\\"></head><body>\\n" > '+filename+'.html'
    cmd2='markdown '+filename+'.md >>'+filename+'.html'
    cmd3='echo "\\n</body></html>" >> '+filename+'.html'
    #print cmd1
    #print cmd2
    #print cmd3
    os.system(cmd1)
    os.system(cmd2)
    os.system(cmd3)
