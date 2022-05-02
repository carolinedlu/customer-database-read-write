import streamlit as st
import snowflake.connector

PASSWORD = st.secrets["snowflake_password"]
WAREHOUSE = st.secrets["warehouse"]
USER = st.secrets["user"]
ACCOUNT = st.secrets("account")

st.title("Customer Loyalty Program")
st.header("Look up an existing customer")
st.header("Add a new customer")

con = snowflake.connector.connect(
    user=USER,
    password=PASSWORD,
    account=ACCOUNT,
    session_parameters={
#         'QUERY_TAG': 'EndOfMonthFinancials',
    }
)
