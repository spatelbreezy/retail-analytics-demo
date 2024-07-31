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
    "Regular customers aged over 50 who spent more than $15,000": """
    SELECT c.Customer_ID, c.Customer_Name, c.Age, c.Total_Spent
    FROM customers c
    WHERE c.Age > 50 AND c.Total_Spent > 15000 AND c.Loyalty_Status = 'Regular'
    ORDER BY c.Total_Spent DESC
    """,

    "Top 10 suppliers by order picking accuracy": """
    SELECT sm.Supplier_Name, sm.Supplier_ID, sm.Supplier_Performance_Evaluation, opf.Order_Picking_Accuracy
    FROM supplierMetrics sm
    JOIN orderPickingAndFulfillment opf ON sm.Supplier_ID = opf.Supplier_ID
    ORDER BY opf.Order_Picking_Accuracy DESC
    LIMIT 10
    """,

    "Allocation strategies and safety stocks for products with lowest inventory turnover": """
    SELECT p.Inventory_Allocation_Strategy, i.Safety_Stock_Levels
    FROM promotionalAndMarketData p
    JOIN inventoryMetrics i ON p.Product_ID = i.Product_ID
    ORDER BY i.Inventory_Monthly_Turnover_Rate ASC
    LIMIT 100
    """,

    "Products with shrinkage rates higher than 4.9%": """
    SELECT s.Product_ID, s.Shrinkage_Rate, s.Root_Cause_Analysis, s.Loss_Prevention_Measures
    FROM shrinkageAndLossPrevention s
    WHERE s.Shrinkage_Rate > 4.9
    ORDER BY s.Shrinkage_Rate DESC
    """,

    "Loss prevention audit findings for high-shrinkage, low-efficiency stores": """
    SELECT s.Store_ID, s.LossPreventionAudit_Findings
    FROM shrinkageStores s
    JOIN storeEfficiency se ON s.Store_ID = se.Store_ID
    WHERE s.Shrinkage_Rate > 2 AND se.Sales_per_SquareFoot < 200
    """,

    "Rural and suburban stores with high shrinkage rates": """
    SELECT s.Store_ID, s.Store_Location_Type, s.Shrinkage_Rate
    FROM shrinkageStores s
    WHERE s.Store_Location_Type IN ('rural', 'suburban')
    AND s.Shrinkage_Rate >= 3
    ORDER BY s.Shrinkage_Rate DESC
    """
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