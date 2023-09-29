import streamlit as st
import graphviz

st.title("Computational Graphs")
if 'string' not in st.session_state:
    st.session_state.string=""
st.session_state.string=""
st.header("Add operators and numbers")
n=st.number_input(min_value=0,max_value=10,label="Enter number")
a=st.button(label="multiply",type="primary")
b=st.button(label="Add",type="primary")
c=st.button(label="log",type="primary")
d=st.button(label="sin",type="primary")

if a:
    st.session_state.string+="x"
if b:
    st.session_state.string+="+"
if c:
    st.session_state.string+="log"
if d:
    st.session_state.string+="sin"

st.write(st.session_state.string)



