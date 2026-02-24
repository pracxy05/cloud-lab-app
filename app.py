import streamlit as st

st.title("☁️ Cloud Web App - Lab Experiment")
st.subheader("Deployed on Streamlit Community Cloud")

name = st.text_input("Enter your name:")
if name:
    st.success(f"Hello, {name}! Welcome to Community Cloud 🚀")

st.write("This web application is developed and deployed using **Streamlit Community Cloud**.")
st.info("Community Cloud is a shared cloud platform where anyone can deploy Python web apps for free.")
