#!/usr/bin/env python
# coding: utf-8

# In[1]:



import cv2
import time
import numpy as np
import os
import pandas as pd
from scipy.spatial import distance
import pickle


# In[2]:


from darkflow.net.build import TFNet


# In[3]:


options={
    'model':'cfg/yolo.cfg', 
    'load':'bin/yolov2.weights',
    'threshold':0.2,
    'gpu':1.0
}


# In[4]:


tfnet=TFNet(options)


# In[5]:


def cordinates(img):
    light_cor=[]
    cord=[]
    def mouse_drawing(event,x,y,flags,params):
        if event==cv2.EVENT_LBUTTONDOWN:
            print(x,y)
            light_cor.append((x,y))
        if event==cv2.EVENT_RBUTTONDOWN:
            cord.append(light_cor.copy())
            print(cord)
            light_cor.clear()
    cv2.namedWindow("Frame")
    cv2.setMouseCallback("Frame",mouse_drawing)
    img=cv2.resize(img,(1080,720))
    cv2.imshow('Frame',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cord=[[(429, 347), (651, 207), (826, 327), (544, 458)], [(657, 408), (1077, 198), (1077, 442)], [(247, 415), (304, 274), (429, 347), (544, 459), (323, 561)], [(464, 495), (655, 407), (1075, 442), (1077, 612)], [(323, 561), (247, 415), (133, 299), (3, 329), (34, 694)], [(34, 694), (462, 495), (1077, 612), (1076, 694)]]
    return cord


# In[6]:


def area(coords):
    closed_cor=coords.copy()
    closed_cor.append(coords[0])
    t=0
    for count in range(len(closed_cor)-1):
        y = closed_cor[count+1][1] + closed_cor[count][1]
        x = closed_cor[count+1][0] - closed_cor[count][0]
        z = y * x
        t += z
    return abs(t/2.0)


# In[7]:


def find_region(cor,p):
    for count,i in enumerate(cor):
        area1=area(i)
        area2=0
        for j in range(len(i)):
            area2+=area([i[j],i[(j+1)%len(i)],p])
        if area1==area2: 
            return count+1
    return 0             


# In[8]:


def colour_region(r):
    color_region=np.zeros((720,1080,3))
    def color(p,y,x):
        if p==0:
            color_region[x][y]=[0,0,0]
        if p==1:
            color_region[x][y]=[0,0,255]
        if p==2:
            color_region[x][y]=[0,255,0]
        if p==3:
            color_region[x][y]=[255,0,0]
        if p==4:
            color_region[x][y]=[255,255,0]   
        if p==5:
            color_region[x][y]=[0,255,255]
        if p==6:
            color_region[x][y]=[255,0,255]
        if p==7:
            color_region[x][y]=[255,0,255]
    for x in range(1080):
        for y in range(720):
            color(r[x][y],x,y)
    cv2.imshow('i',color_region)
    cv2.imwrite('color_region.jpg',color_region)
    cv2.waitKey(0)
    cv2.destroyAllWindows() 


# In[9]:


def region(light_cor):
    global r
    r=np.zeros((1080,720))
    for x in range(1080):
        for y in range(720):
            r[x][y]=find_region(light_cor,(x,y))
    colour_region(r)
    with open("region.txt","wb") as myregion:
        pickle.dump(r,myregion)
    return r        


# In[10]:


def partition(link):
    cap =cv2.VideoCapture(link)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,1080)
    while True:
        ret,frame=cap.read()
        frame=cv2.resize(frame,(1080,720))
        cv2.imshow("frame",frame)
        if cv2.waitKey(1)==13:
            #cv2.imwrite("partition1.jpg",frame)
            break
    cap.release()
    cv2.destroyAllWindows()
    global nol,nof
    nol=int(input("Enter no. of lights\n"))
    nof=int(input("Enter no. of fans\n"))
    os.startfile("partition1.jpg")
    wait=input("Waiting for partiton\npress 1 to continue")
    if wait=='1':
        img=cv2.imread("partition1.jpg")
    coord=cordinates(img)
    region(coord)
    return (nol,nof,coord)


# In[11]:


def pre(img,nol,nof,off):
    global light,fan
    if off==1:
        light=np.zeros(int(nol>0),dtype='int')
        fan=np.zeros(int(nof),dtype='int')
    count=0
    result=tfnet.return_predict(img)
    for i,res in enumerate(result):
        tl=(res['topleft']['x'],res['topleft']['y'])
        br=(res['bottomright']['x'],res['bottomright']['y'])
        inter=(tl[0],br[1])
        cx=int((br[0]+tl[0])/2)
        cy=int((br[1]+tl[1])/2)
        #print("tl = {} br = {} c={},{}".format(tl,br,cx,cy))
        label=res['label']
        if label=='person':
            light=1
            count=count+1
            re=int(r[cx][cy])
            if re!=0 and re<7:
                fan[re-1]=1
            #cv2.rectangle(img,tl,br,(0,0,255),2)
            cv2.circle(img,(cx,cy),2,(0,0,255),2)
            length=distance.euclidean(inter,tl)
            breadth=distance.euclidean(inter,br)
            area=length*breadth
            #cv2.putText(img,str(area),(cx,cy+10),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
    cv2.putText(img,'No. of people:'+str(count),(10,20),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
    cv2.putText(img,'Lights :'+str(light),(782,48),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
    j=0
    with open("test.txt","a") as li:
        li.truncate(0)
        b=fan
        j=j+1
        for i,c in enumerate(b):
            if c==1:
                li.write(str(i+1)+',')
    
        #y=y+30
        #cv2.putText(img,'Fan{} :'.format(i+1)+str(fan[i]),(782,y),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
    return (img,count,light,fan) 


# In[ ]:


def predict_img(frame):
    with open("myvariables.txt","rb") as myfile:
        myvariables=pickle.load(myfile)
        nol=myvariables['nol']
        nof=myvariables['nof']
    with open("region.txt","rb") as reg:
        r=pickle.load(reg)
    frame,count,light,fan=pre(frame,nol,nof,1)
    y=48
    for i in range(6):
        y=y+30
        cv2.putText(frame,'Fan{} :'.format(i+1)+str(fan[i]),(782,y),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
    return frame


# In[12]:


def run_algo(nol,nof,r,link):
    cap =cv2.VideoCapture(link)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,1080)
    i=1
    st=time.time()
    start=0
    off=1
    sum=0
    while True:
        s=time.time()
        ret,frame=cap.read()
        frame=cv2.resize(frame,(1080,720))
        #cv2.imwrite("test.jpg",frame)
        en=time.time()
        if (int(en-start))>=5:
            if sum%5==0:
                off=1
                sum=0
            else:
                off=0
            sum=sum+5
            frame,count,light,fan=pre(frame,nol,nof,off)
            start=time.time() 
        #print("time"+str(en-st))
        cv2.putText(frame,'No. of people:'+str(count),(10,20),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
        cv2.putText(frame,'Lights :'+str(light),(782,48),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
        y=48
        for i in range(6):
            y=y+30
            cv2.putText(frame,'Fan{} :'.format(i+1)+str(fan[i]),(782,y),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
        cv2.imshow("YOLO",frame)
        fps=1/(time.time()-s)
        print("fps"+str(fps))
        if cv2.waitKey(1)==13:
            with open("test.txt","a") as li:
                li.truncate(0)
                li.write("0")
            break
    cap.release()
    cv2.destroyAllWindows()


# In[61]:


choice=int(input("1.Setup\n2.Run existing Setup\n"))
link="rtsp://root:thingQbator%40123@192.168.1.13:554/live.sdp"
if choice==1:
    link=int(input("Establish the link\n"))
    link="rtsp://root:thingQbator%40123@192.168.1.13:554/live.sdp"
    nol,nof,coord=partition(link)
    variables={'nol':nol,'nof':nof,'coord':coord}
    with open("myvariables.txt","wb") as myfile:
        pickle.dump(variables,myfile)    
    if nol>0:
        lights=1
    fan=np.ones(nof,dtype='int') 
if choice==2:
    with open("myvariables.txt","rb") as myfile:
        myvariables=pickle.load(myfile)
        nol=myvariables['nol']
        nof=myvariables['nof']
    with open("region.txt","rb") as reg:
        r=pickle.load(reg)
run_algo(nol,nof,r,link)

