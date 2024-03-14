import streamlit as st
import requests

st.set_page_config(page_title="Admin", page_icon="📈")

st.markdown("Admin Page")

with st.form("Insert fruit"):
    st.write("Fruit form")
    fruit = st.text_input("Fruit", '')

    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:
        # Add new fruit 
        requests.post(f"http://server:8000/add/{fruit}")

        # get all fruits
        fruits = requests.get("http://server:8000/list")
        st.write(fruits.json())