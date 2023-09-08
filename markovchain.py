import streamlit as st
import numpy as np
import pandas as pd
import schemdraw
from schemdraw import flow
import schemdraw.elements as elm


st.title("Markov Chain model")
st.write("In this example we will consider 3 states:")
st.write("1. Bangalore")
st.write("2. Chennai")
st.write("3. Mumbai")
st.header("Selecting Parameters")


col1, col2, col3 = st.columns(3)

with col1:
   p1=st.slider("prior probability for Bangalore",min_value=0.0,max_value=1.0,step=0.1,value=0.4)
   st.write("---")
   q1 =st.slider("P(Bangalore|Bangalore)",min_value=0.0,max_value=1.0,step=0.1,value=0.3)
   q2 =st.slider("P(Chennai|Bangalore)",min_value=0.0,max_value=1-q1,step=0.1,value=0.4)
   q3 =st.slider("P(Mumbai|Bangalore)",value=round(1-q1-q2,1),disabled=True)
with col2:
   p2=st.slider("prior probability for Chennai",min_value=0.0,max_value=1-p1,step=0.1,value=0.2)
   st.write("---")
   s1 =st.slider("P(Bangalore|Chennai)",min_value=0.0,max_value=1.0,step=0.1,value=0.2)
   s2 =st.slider("P(Chennai|Chennai)",min_value=0.0,max_value=1-s1,step=0.1,value=0.1)
   s3 =st.slider("P(Mumbai|Chennai)",value=round(1-s1-s2,1),disabled=True)
with col3:
   p3=st.slider("Select prior probability for Mumbai",value=round(1-p1-p2,1),disabled=True)
   st.write("---")
   r1 =st.slider("P(Bangalore|Mumbai)",min_value=0.0,max_value=1.0,step=0.1,value=0.4)
   r2 =st.slider("P(Chennai|Mumbai)",min_value=0.0,max_value=1-r1,step=0.1,value=0.4)
   r3 =st.slider("P(Mumbai|Mumbai)",value=round(1-r1-r2,1),disabled=True)

if ((round(p1+p2+p3))==1) and ((round(q1+q2+q3))==1) and ((round(s1+s2+s3))==1) and ((round(r1+r2+r3))==1):
   pass
else:
   raise Exception("Probabilities don't sum up to 1")

index_label = ["Bangalore","Chennai","Mumbai"]
data = {"Bangalore":[q1,s1,r1],"Chennai":[q2,s2,r2],"Mumbai":[q3,s3,r3]}
df1 = pd.DataFrame(data,index=index_label)
st.dataframe(df1,width=300)

data1 = {"Prior Probability":[p1,p2,p3]}
df2 = pd.DataFrame(data1,index=index_label)
st.dataframe(df2,width=200)

n = st.slider("Enter number of time stamps",min_value=1,max_value=25,value=10)

pred = []
first_choice = np.random.choice(index_label,p=df2["Prior Probability"])
pred.append(first_choice)
while (len(pred)<n):
    current_city = pred[-1]
    if current_city=="Bangalore":
        index=0
    elif current_city=="Chennai":
       index=1
    else:
        index=2
    next_city=np.random.choice(index_label,p=df1.iloc[index])
    pred.append(next_city)
with schemdraw.Drawing() as dwg:
  i=0
  for j in range(len(pred)):
    city=pred[j]
    if j==len(pred)-1:
      dwg += (flow.Circle(r=1.0).at((i,0)).label(city).fill('lightblue'))
    else:
      dwg += (flow.Circle(r=1.0).at((i,0)).label(city).fill('lightblue'))
      dwg += (flow.Arrow(l=1.0,color="white"))
      i+=3


dwg.save("ans.png")
st.image("ans.png")

