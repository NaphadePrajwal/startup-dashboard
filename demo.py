import streamlit as st

email = st.text_input('Enter email')
password = st.text_input('Enter password')
gender = st.selectbox('Select gender',['male','female','others'])

btn = st.button('Login Karo')

# if the button is click
if btn:
    if email == 'prajwal@gmail.com' and password == '1234':
        st.balloons()
        st.success("Login Successful")
        st.write(gender)
    else:
        st.error('Login Failed')