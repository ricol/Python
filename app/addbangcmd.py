#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os

# traverse root directory, and list directories as dirs and files as files

CMD = '#!/usr/bin/python'
CMD_LOCAL = '#!/usr/local/bin/python'
TO = "#!/usr/bin/env python"
CMD_CODING_UTF_8 = "#-*- coding: utf-8 -*-"
CMD_CODING_UTF = "#-*- coding:utf -*-"

def getListOfFiles(dir, filetype):
    result = []
    for root, dirs, files in os.walk(dir):
        path = root.split(os.sep)
        p = '/'.join(path)
        for file in files:
            f = "%s/%s" % (p, file)
            filename, fileextension = os.path.splitext(f)
            if "addbangcmd" in filename: continue
            if fileextension == filetype:
                result.append(f)
    return result

def remove(data):
    lines = data.split('\n')
    bProcessed = False
    while len(lines) > 0 and \
        (lines[0] == CMD or
         lines[0] == CMD_LOCAL or
		 lines[0] == TO or
         ("coding" in lines[0] and "utf" in lines[0]) or
         "usr/bin/" in lines[0] or "#!" in lines[0] or
         lines[0] == ''):
        lines.remove(lines[0])
        bProcessed = True
    #remove unnecessary blank lines
    new_lines = []
    bEmptyLine = False
    bSecondEmptyLine = False
    for line in lines:
        compact_line = line.strip()
        if compact_line == "":
            if bEmptyLine: bSecondEmptyLine = True
            bEmptyLine = True
        else:
            bEmptyLine = False
            bSecondEmptyLine = False
        if not bSecondEmptyLine:
            if bEmptyLine:
                new_lines.append("")
            else:
                new_lines.append(line)
    if bProcessed:
        return '\n'.join(new_lines), True
    return data, False

def process(dir, data, add=True):
    if add:
        lines = data.split('\n')
        if len(lines) > 0 and \
        lines[0] == TO and \
        lines[1] == CMD_CODING_UTF_8 and \
        lines[2] == '':
            return False
        new_data, _ = remove(data)
        lines = new_data.split('\n')
        lines.insert(0, TO)
        lines.insert(1, CMD_CODING_UTF_8)
        lines.insert(2, '')
        return save('\n'.join(lines))
    else:
        new_data, bProcessed = remove(data)
        if bProcessed: return save(new_data)
    return False

def save(content):
    try:
        with open(dir, 'w') as myFile:
            myFile.writelines(content)
    except e:
        print("Error[%s]: %s" % (dir, e))
        return False
    return True

if __name__ == "__main__":
    dir = "./"
    filetype = ".py"
    if len(os.sys.argv) <= 2:
        print("Usage: addbangcmd.py --add|--remove <directory>")
        exit()
    option = os.sys.argv[1]
    if option not in ["--add", "--remove"]:
        print("invalid operation!")
        exit()
    dir = os.sys.argv[2]
    print("searching for %s files in %s" % (filetype, dir))
    files = getListOfFiles(dir, filetype)
    total = len(files)
    ignored = 0
    updated = 0
    for dir in files:
        with open(dir, "r") as myfile:
            data = myfile.read()
            print("Processing...%s" % dir)
            if process(dir, data, add=option == "--add"):
                updated += 1
            else:
                ignored += 1
    print("Result:")
    print("Total[%s]: %d" % (filetype, total))
    print("updated: %d" % updated)
    print("ignored: %d" % ignored)
