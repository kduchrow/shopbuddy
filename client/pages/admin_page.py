import streamlit as st
import requests

st.set_page_config(page_title="Admin", page_icon="📈")

st.markdown("Admin Page")

with st.form("Insert fruit"):
    st.write("Fruit form")
    shop = st.text_input("Shop", '')

    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:
        
        shop = {
                "shop_name": shop
            }

        requests.post(f"http://server:8000/", json=shop)

        st.write(requests.get("http://server:8000/list"))