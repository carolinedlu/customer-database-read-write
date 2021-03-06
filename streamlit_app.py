import streamlit as st
import snowflake.connector

PASSWORD = st.secrets["PASSWORD"]
WAREHOUSE = st.secrets["WAREHOUSE"]
USER = st.secrets["USER"]
ACCOUNT = st.secrets["ACCOUNT"]

st.title("Customer Loyalty Program")
first_name = st.text_input("Customer's first name", placeholder="John")
last_name = st.text_input("Customer's last name", placeholder="Smith")
search_for_cust = st.button("Search for existing customer")
add_new_cust = st.button("Add new customer")
close_snow_conn = st.button("Close Snowflake Connection")
clear_cache_snow_cred = st.button("Clear Snowflake Credentials from Cache")

def connectToSnowflake(c):
    if "snowconn" in st.session_state:
        return st.session_state.get("snowconn")

    con = snowflake.connector.connect(
            user=c["USER"],
            password=c["PASSWORD"],
            account=c["ACCOUNT"],
        );
    st.session_state["snowconn"] = con
    return con

if close_snow_conn and "snowconn" in st.session_state:
    conn = st.session_state["snowconn"]
    conn.close()

if clear_cache_snow_cred:
    del st.session_state["snowconn"]

if search_for_cust:
    conn = connectToSnowflake({
        "USER": USER, 
        "PASSWORD": PASSWORD, 
        "ACCOUNT": ACCOUNT
    })

    cur = conn.cursor()
    cur.execute("SELECT * FROM CUSTOMER_LOYALTY_PROGRAM.PUBLIC.CUSTOMERS WHERE FIRSTNAME=(%s) AND LASTNAME=(%s)", (first_name, last_name))
    results = cur.fetchall()
    st.write(results)
    num_results = cur.rowcount
    ind = 0
    search_results = ""

    if num_results == 0:
        st.info('0️⃣ No such customer exists in the database.')
    elif num_results == 1:      
        for first, last in results:
            search_results += f"{first} {last}."
        full_results = "✅ One customer exists in the database with the same first and last name.\n Here is the customer: " + search_results
        st.success(full_results)
    else:
        search_results = ""
        for first, last in results:
            ind += 1
            if num_results == ind:
                search_results += f"and {first} {last}."
            else:
                search_results += f"{first} {last}, "
        cust_exists_message = "✅ " + str(num_results) + " customers exist in the database with the same first and last names.\n Here they are: "
        full_results = cust_exists_message + search_results
        st.success(full_results)

if add_new_cust:
    conn = snowflake.connector.connect(
        user=USER,
        password=PASSWORD,
        account=ACCOUNT,
    )
    
    cur = conn.cursor()
    cur.execute("INSERT INTO CUSTOMER_LOYALTY_PROGRAM.PUBLIC.CUSTOMERS VALUES (%s, %s)", (first_name, last_name))
    results = cur.fetchall()
    st.write(results)
    
    if cur.rowcount > 0:
        st.success("🥳 Customer was successfully added to the database.")
    else:
        st.error("😬 Whoops! We couldn't add your customer. Try again or check the logs.")
