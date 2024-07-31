import streamlit as st
import pandas as pd
import pymysql
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection function
def connect_to_db():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),  # Convert port to integer
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )

# Execute query function
def execute_query(query):
    conn = connect_to_db()
    try: #not sure if this works?
        with conn.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
        return pd.DataFrame(result, columns=columns)
    finally:
        conn.close()

# Streamlit app
st.title("Retail Analytics Dashboard")

# Question 1
if st.button("List Regular customers aged over 50 who spent more than $15,000"):
    #Take query & excute and post to streamlit dataframe
    st.dataframe("Working #1")

# Question 2
if st.button("Top 10 suppliers by order picking accuracy"):
    st.dataframe("Working #2")

# Question 3
if st.button("Allocation strategies and safety stocks for products with lowest inventory turnover"):
    st.dataframe("Working #3")

# Question 4
if st.button("Products with shrinkage rates higher than 4.9%"):
    st.dataframe("Working #4")

# Question 5
if st.button("Loss prevention audit findings for high-shrinkage, low-efficiency stores"):
    st.dataframe("Working #5")

# Question 6
if st.button("Rural and suburban stores with high shrinkage rates"):
    st.dataframe("Working #6")