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
    cur.execute("SELECT * FROM CUSTOMER_LOYALTY_PROGRAM.PUBLIC.CUSTOMERS WHERE FIRSTNAME=(%s) AND LASTNAME=(%s)", (first_name, last_name))
    results = cur.fetchall()
    num_results = cur.rowcount
    ind = 0

    if num_results == 0:
        st.info('No such customer exists in the databas.')
    else: 
        search_results = ""
        for first, last in results:
            ind += 1
            if num_results == ind:
                search_results += f"and {first} {last}."
            else:
                search_results += f"{first} {last}, "

        cust_exists_message = "One or more customer(s) exist in the database with the same first and last names. Here they are: "
        full_results = cust_exists_message + search_results
        st.write(full_results)

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
    cur.execute("INSERT INTO CUSTOMER_LOYALTY_PROGRAM.PUBLIC.CUSTOMERS VALUES (%s, %s)", (first_name, last_name))
    
    if cur.rowcount > 0:
        st.success("Customer was successfully added to the database.")
