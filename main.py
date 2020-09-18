# coding=UTF-8
from tkinter import *
from client import *
from server import *

root=Tk()

#
duText=None
dfText=None
dStatus=None
suText=None
sfText=None
sStatus=None

portText=None
uplineState=None
#

def setLabelText(lab,txt):
    lab["text"]=txt


def startServer():
    port=portText.get()
    server(int(port))
    uplineState["text"]="成功上线！"


def down():
    filename=dfText.get()
    url=duText.get()
    url+="/jsonrpc"
    print(url)
    print(filename)
    setLabelText(dStatus,"正在下载中...")
    if downloadFile(filename,url):
        setLabelText(dStatus,"下载完成。")
    else :
        setLabelText(dStatus,"下载失败。")

    

def send():
    filename=sfText.get()
    url=suText.get()
    url+="/jsonrpc"

    setLabelText(sStatus,"正在发送中...")

    sendFile(filename,url)

    setLabelText(sStatus,"发送完成。")


def getDownloadUI():

    global duText,dfText,dStatus

    ret=Frame(root)
    label=Label(ret,text="下载")
    label.pack()

    dUrlFrame=Frame(ret)
    Label(dUrlFrame,text="URL").pack(side=LEFT)
    duText=Entry(dUrlFrame,bd=2)
    duText.pack(side=RIGHT)
    dUrlFrame.pack()

    dFileFrame=Frame(ret)
    Label(dFileFrame,text="文件名").pack(side=LEFT)
    dfText=Entry(dFileFrame,bd=2)
    dfText.pack(side=RIGHT)
    dFileFrame.pack()

    Button(ret,text="下载",command=down).pack()
    dStatus=Label(ret)
    dStatus.pack()

    return ret
    

def getSendUI():
    global suText,sfText,sStatus

    ret=Frame(root)
    label=Label(ret,text="发送")
    label.pack()

    sUrlFrame=Frame(ret)
    Label(sUrlFrame,text="URL").pack(side=LEFT)
    suText=Entry(sUrlFrame,bd=2)
    suText.pack(side=RIGHT)
    sUrlFrame.pack()

    sFileFrame=Frame(ret)
    Label(sFileFrame,text="文件名").pack(side=LEFT)
    sfText=Entry(sFileFrame,bd=2)
    sfText.pack(side=RIGHT)
    sFileFrame.pack()

    Button(ret,text="发送",command=send).pack()
    sStatus=Label(ret)
    sStatus.pack()

    return ret


def getUplineUI():
    global portText,uplineState
    f=Frame(root)
    Label(f,text="监听端口:").pack(side=LEFT)

    uplineState=Label(f)
    uplineState.pack(side=RIGHT)

    onlineBtn=Button(f,text="上线",command=startServer)
    onlineBtn.pack(side=RIGHT)

    portText=Entry(f,bd=2)
    portText.pack(side=RIGHT)

    return f

def main():
    root.title("安全传输工具")

    uplineUI=getUplineUI()
    uplineUI.pack()

    downloadUI=getDownloadUI()
    sendUI=getSendUI()
    downloadUI.pack(side=LEFT)
    sendUI.pack(side=RIGHT)
    root.mainloop()


if __name__ =='__main__':
    main()

