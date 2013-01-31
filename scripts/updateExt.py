#!/usr/bin/python2
#coding: UTF-8

import subprocess, os, shutil
import urllib
import zipfile

from optparse import OptionParser

arch = "win32"
ext = "ext"
downloadDir = ext + "/download"

extDirs = ["include", "lib", "bin"]

dependencies = {
  "glew" : {
    "git" : ("git://glew.git.sourceforge.net/gitroot/glew/glew", "glew-1.9.0",),
    "source": "http://sourceforge.net/projects/glew/files/glew/1.9.0/glew-1.9.0.zip",
    "win32" : "http://sourceforge.net/projects/glew/files/glew/1.9.0/glew-1.9.0-win32.zip",
    "win64" : "http://sourceforge.net/projects/glew/files/glew/1.9.0/glew-1.9.0-win64.zip"
  },
  "glfw" : {
    #"git" : ("git://git.code.sf.net/p/glfw/code", "master",),
    "source": "http://sourceforge.net/projects/glfw/files/glfw/2.7.7/glfw-2.7.7.zip",
    "win32" : "http://sourceforge.net/projects/glfw/files/glfw/2.7.7/glfw-2.7.7.bin.WIN32.zip",
    "win64" : "http://sourceforge.net/projects/glfw/files/glfw/2.7.7/glfw-2.7.7.bin.WIN64.zip"
  },
  "glm" : {
    "git" : ("git://github.com/g-truc/glm.git", "0.9.4.1",),
    "win32" : "http://sourceforge.net/projects/ogl-math/files/glm-0.9.4.1/glm-0.9.4.1.zip"
  },
  "assimp" : {
    #"git" : ("git://github.com/assimp/assimp.git", "master",),
    "win32" : "http://sourceforge.net/projects/assimp/files/assimp-3.0/assimp--3.0.1270-full.zip",
    "source": "http://sourceforge.net/projects/assimp/files/assimp-3.0/assimp--3.0.1270-source-only.zip"
  }
}

def makeDir(dir):
  if not os.path.exists(dir):
      os.makedirs(dir)


def downloadZips():

  for dependency in dependencies.values():
    url = dependency[arch]
    name = url.split("/")[-1]
    if not os.path.exists(name):
      print ("Downloading", url)
      subprocess.call(["curl", "-L", url, "-o", name])
      #urllib.urlretrieve (url, name)

def removeUnpack():
  filelist = [ f for f in os.listdir(".") if not f.endswith(".zip") ]
  for f in filelist:
    if os.path.isdir(f):
      shutil.rmtree(f)
    elif os.path.isfile(f):
      os.remove(f)

def unPack():
  filelist = [ f for f in os.listdir(".") if f.endswith(".zip") ]
  for f in filelist:
    subprocess.call(["unzip", f])

def copy(src, dst):
  if os.path.isdir(src):
    shutil.copytree(src, dst)
  else:
    shutil.copy(src, dst)

def copyFiles(source, destination):
  for f in os.listdir(source):
    sourcePath = source + "/" + f
    try:
      copy(sourcePath, destination)
    #except FileExistsError:
    except OSError:
        try:
          copy(sourcePath, destination + f)
    #    except FileExistsError:
        except OSError:
          copyFiles(sourcePath, destination + f)

def install(src, dest):
  copyFiles("download/%s/%s" % (src, dest), "%s/" % dest)

def installPack(name):
  for dir in extDirs:
    install(name, dir)

def installFiles():
  for dir in extDirs:
    if os.path.exists(dir):
      shutil.rmtree(dir)
    makeDir(dir)

  installPack("assimp--3.0.1270-sdk")
  installPack("glew-1.9.0")
  
  install("glfw-2.7.7.bin.WIN32", "include")
  
  copy("download/glfw-2.7.7.bin.WIN32/lib-mingw", "lib/mingw")
  copy("download/glfw-2.7.7.bin.WIN32/lib-msvc110", "lib/msvc110")
  copy("download/glfw-2.7.7.bin.WIN32/lib-msvc100", "lib/msvc100")
  copy("download/glm", "include/glm")
  
  
def msvcDeps():  
  makeDir(downloadDir)
  os.chdir(downloadDir)
  downloadZips()
  removeUnpack()
  unPack()
  os.chdir("..")
  installFiles()

def mingwDeps():
  makeDir(downloadDir)
  os.chdir(downloadDir)
  for dependency in dependencies:
    name = dependency
    
    if dependencies[dependency].has_key("git"):
      url = dependencies[dependency]["git"][0]
      tag = dependencies[dependency]["git"][1]
      if not os.path.exists(name):
        subprocess.call(["git", "clone", url, name])
        os.chdir(name)
        subprocess.call(["git", "checkout", tag])
        os.chdir("..")
    else:
      print dependency, name
      url = dependencies[dependency]["source"]
      name = url.split("/")[-1]
      if not os.path.exists(name):
        subprocess.call(["curl", "-L", url, "-o", name])
  unPack()
      

parser = OptionParser()
parser.add_option("--msvc10", action="store_true", dest="msvc10", help="Get VC10 Dependencies")
parser.add_option("--mingw", action="store_true", dest="mingw", help="Get MinGW Dependencies")

(options, args) = parser.parse_args()

hasNeededOption = False
mandatories = ['msvc10', 'mingw']
for m in mandatories:
  if options.__dict__[m]:
    hasNeededOption = True
        
if not hasNeededOption:
  print("A mandatory option is missing.")
  parser.print_help()
  exit(-1)

if options.msvc10:
  msvcDeps()
elif options.mingw:
  mingwDeps()

#os.chdir("download")
#removeUnpack()

