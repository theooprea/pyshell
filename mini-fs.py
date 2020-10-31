import os
import socket
import getpass
import shutil
from pathlib import Path

def ls(args):
    if args == []:
        for file in os.listdir():
            print(file, end = " ")
        print('')
    elif args[0] == "-r" or args[0] == "-R":
        for root, dirs, files in os.walk(".", topdown = True):
            print(root, ":")
            for directory in dirs:
                print(directory, end = " ")
            for file in files:
                print(file, end = " ")
            print('')
    else:
        for file in os.listdir(args[0]):
            print(file, end = " ")
        print('')


def cd(args, prev_working_directory, home):
    if args == []:
        prev_working_directory = os.getcwd()
        os.chdir(home)
    elif args[0] == "-":
        if prev_working_directory != "":
            aux = os.getcwd()
            os.chdir(prev_working_directory)
            prev_working_directory = aux
    else:
        if os.path.isdir(args[0]):
            prev_working_directory = os.getcwd()
            os.chdir(args[0])
        else:
            print(args[0], ": No such directory")
    working_directory = os.getcwd()
    startline = getpass.getuser() + "@" + socket.gethostname() + ":" + working_directory + "$ "
    return (prev_working_directory, startline)

def mkdir(args):
    for arg in args:
        if os.path.isdir(arg):
            print(arg, ": directory already exists!")
        else:
            os.mkdir(arg)

def touch(args):
    for arg in args:
        if not os.path.isfile(arg):
            file = open(arg, "w")
            file.close()

def tree(args):
    if args == []:
        for root, dirs, files in os.walk("."):
            level = root.replace(".", '').count(os.sep)
            indent = ' ' * 5 * (level)
            print('{}{}/'.format(indent, os.path.basename(root)))
            subindent = ' ' * 5 * (level + 1)
            for f in files:
                print('{}{}'.format(subindent, f))
    else:
        for root, dirs, files in os.walk(args[0]):
            level = root.replace(args[0], '').count(os.sep)
            indent = ' ' * 5 * (level)
            print('{}{}/'.format(indent, os.path.basename(root)))
            subindent = ' ' * 5 * (level + 1)
            for f in files:
                print('{}{}'.format(subindent, f))

def rm(args):
    if args == []:
        print("rm: missing operand")
    else:
        for arg in args:
            if os.path.isfile(arg):
                os.remove(arg)
            elif os.path.isdir(arg):
                print("rm: cannot remove '", arg, "': Is a directory")
            else:
                print("rm: cannot remove '", arg, "': No such file or directory")

def rmdir(args):
    if args == []:
        print("rmdir: missing operand")
    elif args[0] == "-r" or args[0] == "-R":
        for arg in args[1:]:
            if os.path.isdir(arg):
                shutil.rmtree(arg)
            elif os.path.isfile(arg):
                print("rmdir: failed to remove '", arg, "': Not a directory")
            else:
                print("rmdir: failed to remove '", arg, "': No such file or directory")
    else:
        for arg in args:
            if os.path.isdir(arg):
                subdir = os.listdir(arg)
                if len(subdir) == 0:
                    os.rmdir(arg)
                else:
                    print("rmdir: failed to remove '", arg, "': Directory not empty")
            elif os.path.isfile(arg):
                print("rmdir: failed to remove '", arg, "': Not a directory")
            else:
                print("rmdir: failed to remove '", arg, "': No such file or directory")

def cat(args):
    if args == []:
        print("cat: missing operand")
    else:
        for arg in args:
            if os.path.isfile(arg):
                file = open(arg, "r")
                for line in file:
                    line = line.rstrip()
                    print(line)
            elif os.path.isdir(arg):
                print("cat: ", arg, ": Is a directory")
            else:
                print("cat: ", arg, ": No such file or directory")

working_directory = os.getcwd()
startline = getpass.getuser() + "@" + socket.gethostname() + ":" + working_directory + "$ "

home = str(Path.home())
prev_working_directory = ""

command = input(startline)
args = command.split()[1:]
command = command.split()[0]

while command != "stop" and command != "exit" and command != "quit" and command != "s" and command != "q":
    if command == "pwd":
        print(os.getcwd())
    elif command == "ls":
        ls(args)
    elif command == "cd":
        (prev_working_directory, startline) = cd(args, prev_working_directory, home)
    elif command == "mkdir":
        mkdir(args)
    elif command == "touch":
        touch(args)
    elif command == "tree":
        tree(args)
    elif command == "rm":
        rm(args)
    elif command == "rmdir":
        rmdir(args)
    elif command == "cat":
        cat(args)
    else:
        oscommand = command
        for arg in args:
            oscommand = oscommand + " " + arg
        os.system(oscommand)

    command = input(startline)
    args = command.split()[1:]
    command = command.split()[0]
