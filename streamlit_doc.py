import streamlit as st
import pandas as pd
from streamlit import image
import time

## Text Utility
st.title('Startup Dashboard')
st.header('I am learning Streamlit')
st.subheader('And I am loving Streamlit')

st.write('This is a normal text')

st.markdown("""
### My favorite movies
- Race 3
- Humshakals
- Housefull
""")

st.code("""
def foo(input):
    return foo**2

x = foo(2)
""")

st.latex('x^2 + y^2 + 2 = 0')


## Display Elements
df = pd.DataFrame({
    'name':['Nitish','Ankit','Anupam'],
    'marks':[50,60,70],
    'package':[10,12,14]
})

st.dataframe(df)

st.metric('Revenue','Rs 3L','3%')
st.metric('Revenue','Rs 3L','-3%')

st.json({
    'name':['Nitish','Ankit','Anupam'],
    'marks':[50,60,70],
    'package':[10,12,14]
})

## Displaying Media
st.image('img.png')
# st.video('')

## Creating Layouts
st.sidebar.title('Sidebar ka title')

col1, col2 = st.columns(2)

with col1:
    st.image('img.png')

with col2:
    st.image('img.png')

## Showing status
st.error('Login Failed')
st.success("Login Successful")
st.info('Information')
st.warning('Warning')

bar = st.progress(0)

for i in range(1,101):
    #time.sleep(0.1)
    bar.progress(i)

## taking user input

# Text input
emails = st.text_input("Enter email")
number = st.number_input("Enter age")
date = st.date_input("Enter Date")



file = st.file_uploader('Upload a csv file')

if file is not None:
    df = pd.read_csv(file)
    st.dataframe(df.describe())




