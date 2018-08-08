#!/usr/bin/python
#-*-coding:utf-8-*-

# /**
#  * ================================================
#  * 作    者：若云
#  * 版    本：1.0.0
#  * 更新日期： 2018年02月28日
#  * 邮    箱：zyhdvlp@gmail.com
#  * ================================================
#  */

import os
import sys
from config import config
import platform
import shutil

#创建文件
def crateFile(path):
    #创建目录
    if not os.path.exists(path):
        os.mkdir(path)
    else:
        shutil.rmtree(path)               # 删除文件夹及其下所有文件
        os.mkdir(path)

#获取脚本文件的当前路径
def curFileDir():
     #获取脚本路径
     path = sys.path[0]
     #判断为脚本文件还是py2exe编译后的文件，
     #如果是脚本文件，则返回的是脚本的目录，
     #如果是编译后的文件，则返回的是编译后的文件路径
     if os.path.isdir(path):
         return path
     elif os.path.isfile(path):
         return os.path.dirname(path)

#判断当前系统
def isWindows():
  sysstr = platform.system()
  if("Windows" in sysstr):
    return 1
  else:
    return 0

#兼容不同系统的路径分隔符
def getBackslash():
	if(isWindows() == 1):
		return "\\"
	else:
		return "/"  

#当前脚本文件所在目录
parentPath = curFileDir() + getBackslash()
tempPath = parentPath+"temp" +getBackslash()#临时文件保存目录

libPath = parentPath + "lib" + getBackslash()
keystorePath = config.keystorePath
keyAlias = config.keyAlias
keystorePassword = config.keystorePassword
keyPassword = config.keyPassword
buildToolsPath =  config.sdkBuildToolPath + getBackslash()
checkAndroidV2SignaturePath = libPath + "CheckAndroidV2Signature.jar"
walleChannelWritterPath = libPath + "walle-cli-all.jar"

t = []#创建一个唯一字符的集合
#读文件，判断是否之后一个后缀为apk的文件
apkFiles= os.listdir(parentPath) #得到文件夹下的所有文件名称
print ("**** 正在检测目录apk数量 ****")
for apkFile in apkFiles:
    if  "apk" in apkFile :
        t.append(apkFile)
        
if len(t) == 0:
    print ("**** 未发现apk，请把apk放入到当前目录中 ****")
elif len(t) > 1:
    print ("**** 请删除多余的apk文件，仅保留现有的apk ****")
else:
    print ("**** 正常执行代码 ****")
    protectedSourceApkName = t[0]
    protectedSourceApkPath = parentPath + protectedSourceApkName

    crateFile(tempPath)
    
    zipalignedApkPath = tempPath + protectedSourceApkName[0 : -4] + "_aligned.apk"
    #对齐
    zipalignShell = buildToolsPath + "zipalign -v 4 " + protectedSourceApkPath + " " + zipalignedApkPath
    os.system(zipalignShell)

    signedApkPath = zipalignedApkPath[0 : -4] + "_signed.apk"

    #签名
    signShell = buildToolsPath + "apksigner sign --ks "+ keystorePath + " --ks-key-alias " + keyAlias + " --ks-pass pass:'" + keystorePassword + "' --key-pass pass:'" + keyPassword + "' --in " + zipalignedApkPath + " --out " + signedApkPath
    os.system(signShell)

    #检查V2签名是否正确
    checkV2Shell = "java -jar " + checkAndroidV2SignaturePath + " " + signedApkPath;
    os.system(checkV2Shell)

    channelFilePath = parentPath+"config"+getBackslash()+"channel.txt"

    moveApkOutResGuardPath = parentPath+"out"+getBackslash()#输出文件
    crateFile(moveApkOutResGuardPath)
    
    #写入渠道
    writeChannelShell = "java -jar " + walleChannelWritterPath + " batch -f " + channelFilePath + " " + signedApkPath + " " + moveApkOutResGuardPath
    os.system(writeChannelShell)

    #读文件
    apkFiles= os.listdir(moveApkOutResGuardPath) #得到文件夹下的所有文件名称
    print ("\n**** 渠道号为： ****\n")
    for apkFile in apkFiles:
        if  "apk" in apkFile :
            showChannelShell = "java -jar " + walleChannelWritterPath + " show " + moveApkOutResGuardPath  + apkFile
            os.system(showChannelShell)

    print ("\n**** Finish! Please Check the 'out' Folder in your root Floder ! ****\n")

    #删除无用文件
    shutil.rmtree(tempPath)               # 删除文件夹及其下所有文件
    #删除多余文件
    #os.remove(path)





