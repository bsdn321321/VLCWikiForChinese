import os
filelist=os.popen('find -name \'*.md\'').readlines()
cmd1=''
cmd2=''
cmd3=''
#os.system('echo "all:\\n" > makefile')
file_make=open('makefile','w')
file_make.write('all:')
for filename in filelist:
    filename=filename[2:-4]
    cmd1='echo "<html><head><meta http-equiv=\\"Content-Type\\" content=\\"text/html; charset=UTF-8\\"></head><body>\\n" > '+filename+'.html'
    cmd2='markdown '+filename+'.md >>'+filename+'.html'
    cmd3='echo "\\n</body></html>" >> '+filename+'.html'
    #print cmd1
    #print cmd2
    #print cmd3
    file_make.write('\n\t@'+cmd1+';'+cmd2+';'+cmd3)
#file_make.write('\n')

file_make.write('\nclean:\n\t@find -name \'*.html\' -exec rm {} \\;')

