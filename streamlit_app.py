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

# Define queries
queries = {
    "Regular customers aged over 50 who spent more than $15,000": """insert sql here?""",

    "Top 10 suppliers by order picking accuracy": """insert sql here?""",

    "Allocation strategies and safety stocks for products with lowest inventory turnover": """insert sql here?""",

    "Products with shrinkage rates higher than 4.9%": """insert sql here?""",

    "Loss prevention audit findings for high-shrinkage, low-efficiency stores": """insert sql here?""",

    "Rural and suburban stores with high shrinkage rates": """insert sql here?"""
}

# Create a button for each query
for query_name, query_sql in queries.items():
    if st.button(query_name):
        if 'active_query' in st.session_state and st.session_state.active_query == query_name:
            # If the same button is clicked again, clear the results
            st.session_state.active_query = None
            st.session_state.query_result = None
        else:
            # Execute the query and store the results
            st.session_state.active_query = query_name
            st.session_state.query_result = execute_query(query_sql)

# Display the results if a query is active
if 'active_query' in st.session_state and st.session_state.active_query:
    st.subheader(f"Results for: {st.session_state.active_query}")
    st.dataframe(st.session_state.query_result)