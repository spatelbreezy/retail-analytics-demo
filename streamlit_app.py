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
    try:
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
    query = """
    SELECT c.Customer_ID, c.Customer_Name, c.Age, c.Total_Spent
    FROM customers c
    WHERE c.Age > 50 AND c.Total_Spent > 15000 AND c.Loyalty_Status = 'Regular'
    ORDER BY c.Total_Spent DESC
    """
    result = execute_query(query)
    st.dataframe(result)

# Question 2
if st.button("Top 10 suppliers by order picking accuracy"):
    query = """
    SELECT sm.Supplier_Name, sm.Supplier_ID, sm.Supplier_Performance_Evaluation, opf.Order_Picking_Accuracy
    FROM supplierMetrics sm
    JOIN orderPickingAndFulfillment opf ON sm.Supplier_ID = opf.Supplier_ID
    ORDER BY opf.Order_Picking_Accuracy DESC
    LIMIT 10
    """
    result = execute_query(query)
    st.dataframe(result)

# Question 3
if st.button("Allocation strategies and safety stocks for products with lowest inventory turnover"):
    query = """
    SELECT p.Inventory_Allocation_Strategy, i.Safety_Stock_Levels
    FROM promotionalAndMarketData p
    JOIN inventoryMetrics i ON p.Product_ID = i.Product_ID
    ORDER BY i.Inventory_Monthly_Turnover_Rate ASC
    LIMIT 100
    """
    result = execute_query(query)
    st.dataframe(result)

# Question 4
if st.button("Products with shrinkage rates higher than 4.9%"):
    query = """
    SELECT s.Product_ID, s.Shrinkage_Rate, s.Root_Cause_Analysis, s.Loss_Prevention_Measures
    FROM shrinkageAndLossPrevention s
    WHERE s.Shrinkage_Rate > 4.9
    ORDER BY s.Shrinkage_Rate DESC
    """
    result = execute_query(query)
    st.dataframe(result)

# Question 5
if st.button("Loss prevention audit findings for high-shrinkage, low-efficiency stores"):
    query = """
    SELECT s.Store_ID, s.LossPreventionAudit_Findings
    FROM shrinkageStores s
    JOIN storeEfficiency se ON s.Store_ID = se.Store_ID
    WHERE s.Shrinkage_Rate > 2 AND se.Sales_per_SquareFoot < 200
    """
    result = execute_query(query)
    st.dataframe(result)

# Question 6
if st.button("Rural and suburban stores with high shrinkage rates"):
    query = """
    SELECT s.Store_ID, s.Store_Location_Type, s.Shrinkage_Rate
    FROM shrinkageStores s
    WHERE s.Store_Location_Type IN ('rural', 'suburban')
    AND s.Shrinkage_Rate >= 3
    ORDER BY s.Shrinkage_Rate DESC
    """
    result = execute_query(query)
    st.dataframe(result)