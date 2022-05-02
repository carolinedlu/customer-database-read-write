import streamlit as st
import snowflake.connector

PASSWORD = st.secrets["PASSWORD"]
WAREHOUSE = st.secrets["WAREHOUSE"]
USER = st.secrets["USER"]
ACCOUNT = st.secrets["ACCOUNT"]

st.title("Customer Loyalty Program")
st.header("Look up an existing customer")
first_name = st.text_input("Customer's first name", placeholder="Frank")
last_name = st.text_input("Customer's last name", placeholder="Slootman")

st.header("Add a new customer")

conn = snowflake.connector.connect(
    user=USER,
    password=PASSWORD,
    account=ACCOUNT,
    session_parameters={
#         'QUERY_TAG': 'EndOfMonthFinancials',
    }
)

def search_db_for_cust(first_name, last_name):
    cur = conn.cursor()
    cur.execute('select * from customers')
    to_print = cur.fetchmany(3)
    st.write(to_print)

search_for_cust = st.button("Search for customer", on_click=search_, args=(first_name, last_name))
