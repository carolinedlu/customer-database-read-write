import streamlit as st
import snowflake.connector

PASSWORD = st.secrets["PASSWORD"]
WAREHOUSE = st.secrets["WAREHOUSE"]
USER = st.secrets["USER"]
ACCOUNT = st.secrets["ACCOUNT"]

st.title("Customer Loyalty Program")
first_name = st.text_input("Customer's first name", placeholder="Frank")
last_name = st.text_input("Customer's last name", placeholder="Slootman")
search_for_cust = st.button("Search for existing customer")
add_new_cust = st.button("Add new customer")

if search_for_cust:
    conn = snowflake.connector.connect(
    user=USER,
    password=PASSWORD,
    account=ACCOUNT,
    session_parameters={
#         'QUERY_TAG': 'EndOfMonthFinancials',
    }
    )
    
    cur = conn.cursor()
    cur.execute('select * from CUSTOMER_LOYALTY_PROGRAM.PUBLIC.CUSTOMERS')
    st.write(cur.fetchall())
    
    if cur.rowcount==0:
        st.error('No such customer exists in the database')

#     to_print = cur.fetchmany(3)
#     st.write(to_print)

if add_new_cust:
    conn = snowflake.connector.connect(
    user=USER,
    password=PASSWORD,
    account=ACCOUNT,
    session_parameters={
#         'QUERY_TAG': 'EndOfMonthFinancials',
    }
    )
    
    cur = conn.cursor()
    cursor.execute("INSERT INTO CUSTOMER_LOYALTY_PROGRAM.PUBLIC.CUSTOMERS VALUES (%s, %s)", (first_name, last_name))
#     cur.execute(f"INSERT INTO CUSTOMER_LOYALTY_PROGRAM.PUBLIC.CUSTOMERS" \
#                 f"VALUES ({first_name}, {last_name})")
    st.write(cur.fetchall())
    
    if cur.rowcount==0:
        st.error('No such customer exists in the database')

#     to_print = cur.fetchmany(3)
#     st.write(to_print)
    
