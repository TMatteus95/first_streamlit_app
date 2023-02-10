import streamlit as st 
import pandas as pd 
st.title("Main Page")


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
st.dataframe(my_fruit_list)




if st.button("My Button"):
    my_input = st.text_input("Input a text here")
    _, center, _ = st.columns([3, 1, 3])
    submit = center.button("Submit")
    if submit:
        st.write("You have entered: ", my_input)
