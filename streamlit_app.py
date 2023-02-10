import streamlit as st 

st.title("Main Page")


if st.button("My Button"):
    my_input = st.text_input("Input a text here")
    _, center, _ = st.columns([3, 1, 3])
    submit = center.button("Submit")
    if submit:
        st.write("You have entered: ", my_input)
