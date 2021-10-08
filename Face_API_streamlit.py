#!/usr/bin/env python
# coding: utf-8

# In[173]:


import streamlit as st
from PIL import Image
from PIL import ImageDraw
#from PIL import ImageFont
import json
import requests
import pandas as pd
import io


# In[174]:


KEY = "d4ef8b3f9eff4006a6cf145c50b41995"
assert KEY

ENDPOINT = "https://face-ai-uz.cognitiveservices.azure.com/face/v1.0/detect"


# In[175]:


headers = {
    "Content-Type":"application/octet-stream",
    'Ocp-Apim-Subscription-Key':KEY}


# In[176]:


# パラメーターの設定
params = {
    'returnFaceId': True,
    'returnFaceLandmarks': False,
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
}


# In[177]:


st.title("FACE AI")
st.title("UZのAI顔認識アプリ")


# In[178]:


upload_file = st.file_uploader("※人物の画像を選択してください")
if upload_file is not None:
    img = Image.open(upload_file)
    with io.BytesIO() as output:
        img.save(output,format="JPEG")
        binary_img = output.getvalue()
    r = requests.post(ENDPOINT,params=params,headers=headers,data=binary_img)
    for i in range(len(r.json())):
        rect = r.json()[i]["faceRectangle"]
        gender = r.json()[i]['faceAttributes']['gender']
        age = int(r.json()[i]['faceAttributes']["age"])
        smile = r.json()[i]['faceAttributes']['smile']
        draw = ImageDraw.Draw(img)
        #font = ImageFont.truetype("arial.ttf",size=14)
        draw.rectangle([(rect["left"],rect["top"]),(rect["left"]+rect["width"],rect["top"]+rect["height"])],fill=None,outline="green",width=2)
        draw.rectangle([(rect["left"],rect["top"]-25),(rect["left"]+rect["width"],rect["top"])],fill="green",outline="green")
        draw.text((rect["left"]+5,rect["top"]-20),text=gender+"/"+"Age:"+str(age),align="mm",fill="white")#,font=font
    st.image(img,caption="アップロード画像",use_column_width=True)
    st.text("■AIによる感情分析の結果")
    for j in range(len(r.json())):
        a = r.json()[j]['faceAttributes']['emotion']
        a["gender"] =r.json()[j]['faceAttributes']['gender']
        a["age"] =r.json()[j]['faceAttributes']['age']
        st.dataframe(pd.DataFrame([a]).T)
        
        
#         df = pd.DataFrame([r.json()[j]['faceAttributes']['emotion']],index=[f"Image_{j}"]).T
#         df.loc["gender"] = r.json()[j]['faceAttributes']["gender"]
#         df.loc["age"] = r.json()[j]['faceAttributes']["age"]
#         st.dataframe(df)


# In[190]:


a = r.json()[0]['faceAttributes']['emotion']


# In[192]:


a["gender"] =r.json()[0]['faceAttributes']['gender']
a["age"] =r.json()[0]['faceAttributes']['age']


# In[196]:


pd.DataFrame([a]).T


# In[ ]:




