import streamlit as st
import requests

st.set_page_config(page_title="Admin", page_icon="📈")

st.markdown("Admin Page")


server_url = "http://server:8000"

with st.form("List Shops"):
    st.write("List")
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write(requests.get(f"{server_url}/list").json())

with st.form("List Bonus Programs"):
    st.write("List Bonus Programs")
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write(requests.get(f"{server_url}/listBonusPrograms").json())


with st.form("List Cashback Programs"):
    st.write("List Cashback Programs")
    submitted = st.form_submit_button("Submit")
    if submitted:
        cashback_programs = requests.get(f"{server_url}/listCashbackPrograms").json()
        st.write(cashback_programs)
        #if cashback_programs:
        #    st.table(cashback_programs)
        #else:
        #    st.write("No cashback programs found.")


with st.form("Add Shop"):
    st.write("shop Form")
    shop = st.text_input("Shop", '')

    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:
        
        shop = {
                "shop_name": shop
            }

        requests.post(f"{server_url}/add/Shop", json=shop)


with st.form("Add Bonus Program"):
    st.write("Bonus Program Form")
    program_name = st.text_input("Program Name", '')

    submitted = st.form_submit_button("Submit")
    if submitted:
        bonus_program = {
            "bonus_program_name": program_name,  
        }
        requests.post(f"{server_url}/add/BonusProgram", json=bonus_program)
        st.write("Bonus program added successfully!")


with st.form("Add Cashback Program"):
    st.write("Cashback Program Form")

    shops = requests.get(f"{server_url}/list").json()['list']
    selected_shop = st.selectbox("Shop", shops)
    shop_id = selected_shop["_id"]
    
    bonus_programs = requests.get(f"{server_url}/listBonusPrograms").json()['list']
    selected_bonusprogram = st.selectbox("Bonusprogram", bonus_programs)
    bonus_program_id = selected_bonusprogram["_id"]

    program_percentage = st.number_input("Program Percentage", min_value=0.0, max_value=100.0, step=0.1)


    submitted = st.form_submit_button("Submit")
    if submitted:
        cashback_program = {
            "cashbackrate": program_percentage,
            "shop_id": shop_id,
            "bonus_program_id": bonus_program_id
        }
        requests.post(f"{server_url}/addCashbackProgram", json=cashback_program)
        st.write("Cashback program added successfully!")


