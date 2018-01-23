# -*- coding: utf-8 -*-
#****************************************************************************
#*                                                                          *
#*  StepZ Import Export compressed STEP files for FreeCAD                   *
#*  Copyright (c) 2018                                                      *
#*  Maurice easyw@katamail.com                                              *
#*                                                                          *
#*                                                                          *

import FreeCAD,FreeCADGui
import gzip, shutil
import sys, os
import ImportGui
import PySide
from PySide import QtGui, QtCore
import tempfile

___stpZversion___ = "1.1"

try:
    import __builtin__ as builtin #py2
except:
    import builtins as builtin  #py3

# import stepZ; reload(stepZ)

def mkz_string(input):
    if (sys.version_info > (3, 0)):  #py3
        if isinstance(input, str):
            return input
        else:
            input =  input.encode('utf-8')
            return input
    else:  #py2
        if type(input) == unicode:
            input =  input.encode('utf-8')
            return input
        else:
            return input
####
def sayz(msg):
    FreeCAD.Console.PrintMessage(msg)
    FreeCAD.Console.PrintMessage('\n')
####
def sayzw(msg):
    FreeCAD.Console.PrintWarning(msg)
    FreeCAD.Console.PrintWarning('\n')
####
def sayzerr(msg):
    FreeCAD.Console.PrintError(msg)
    FreeCAD.Console.PrintWarning('\n')
####
def open(filename):

    sayz("stpZ version "+___stpZversion___)
    with gzip.open(filename, 'rb') as f:
        file_content = f.read()

    ext = os.path.splitext(os.path.basename(filename))[1]
    fname=os.path.splitext(os.path.basename(filename))[0]
    basepath=os.path.split(filename)[0]
    filepath = os.path.join(basepath,fname + u'.stp')

    tempdir = tempfile.gettempdir() # get the current temporary directory
    tempfilepath = os.path.join(tempdir,fname + u'.stp')

    with builtin.open(tempfilepath, 'w') as f: #py3
        f.write(file_content)
    #ImportGui.insert(filepath)
    ImportGui.open(tempfilepath)
    try:
        os.remove(tempfilepath)
    except OSError:
        sayzerr("error on removing "+tempfilepath+" file")
        pass
####

def insert(filename,doc):

    sayz("stpZ version "+___stpZversion___)
    with gzip.open(filename, 'rb') as f:
        file_content = f.read()

    ext = os.path.splitext(os.path.basename(filename))[1]
    fname=os.path.splitext(os.path.basename(filename))[0]
    basepath=os.path.split(filename)[0]
    filepath = os.path.join(basepath,fname + u'.stp')

    tempdir = tempfile.gettempdir() # get the current temporary directory
    tempfilepath = os.path.join(tempdir,fname + u'.stp')
    
    with builtin.open(tempfilepath, 'w') as f: #py3
        f.write(file_content)
    ImportGui.insert(tempfilepath, doc)
    #ImportGui.open(tempfilepath)
    try:
        os.remove(tempfilepath)
    except OSError:
        sayzerr("error on removing "+tempfilepath+" file")
        pass
####

def export(objs,filename):
    #export(__objs__,u"C:/Cad/Progetti_K/ksu-test/c1.stp.z")
    
    #sayz(filename)
    sayz("stpZ version "+___stpZversion___)
    ext = os.path.splitext(os.path.basename(filename))[1]
    fname=os.path.splitext(os.path.basename(filename))[0]
    basepath=os.path.split(filename)[0]
    tempdir = tempfile.gettempdir() # get the current temporary directory
    filepath = os.path.join(basepath,fname + u'.stp')
    tempfilepath = os.path.join(tempdir,fname + u'.stp')
    
    namefpath = os.path.join(basepath,fname)
    tempnamefpath = os.path.join(tempdir,fname)
    
    outfpath = os.path.join(basepath,fname + u'.stpZ')
    
    if 0: #os.path.exists(filepath):
        sayzw("File cannot be compressed because a file with the same name exists '"+ filepath +"'")
        QtGui.qApp.restoreOverrideCursor()
        reply = QtGui.QMessageBox.information(None,"info", "File cannot be compressed because\na file with the same name exists\n'"+ filepath + "'")
    else:    
        ImportGui.export(objs,tempfilepath)
        if 0: #os.path.exists(namefpath):
            sayzw("File cannot be compressed because a file with the same name exists '" + namefpath + "'")
            QtGui.qApp.restoreOverrideCursor()
            reply = QtGui.QMessageBox.information(None,"info", "File cannot be compressed because\na file with the same name exists\n'"+ namefpath+ "'")
        else:
            with builtin.open(tempfilepath, 'rb') as f_in, gzip.open(tempnamefpath, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
            if 0: #os.path.exists(outfpath):
                sayzw("File cannot be compressed because a file with the same name exists '"+ outfpath + "'")
                QtGui.qApp.restoreOverrideCursor()
                reply = QtGui.QMessageBox.information(None,"info", "File cannot be compressed because\na file with the same name exists\n'"+outfpath+ "'")
            else:
                try:
                    os.remove(outfpath)
                except OSError:
                    sayzerr("error on removing "+outfpath+" file")
                    pass        
                os.rename(tempnamefpath, outfpath)  
                try:
                    os.remove(tempfilepath)
                except OSError:
                    sayzerr("error on removing "+tempfilepath+"file")
                    pass        
####