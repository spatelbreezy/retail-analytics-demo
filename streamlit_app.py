import streamlit as st
import pandas as pd
import pymysql
import plotly.express as px
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# AWS database credentials
DB_HOST = "tellmoredb.cd24ogmcy170.us-east-1.rds.amazonaws.com"
DB_USER = "admin"
DB_PASS = "2yYKKH8lUzaBvc92JUxW"
DB_PORT = "3306"
DB_NAME = "retail_panopticon"


# def connect_to_db():
#     return pymysql.connect(
#         host=DB_HOST,
#         port=int(DB_PORT),
#         user=DB_USER,
#         password=DB_PASS,
#         db=DB_NAME
#     )

def connect_to_db():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        db=os.getenv("DB_NAME")
    )


def execute_query(query):
    conn = connect_to_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            getResult = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
        return pd.DataFrame(getResult, columns=columns)
    finally:
        conn.close()


st.subheader("Hey Store Manager!")
st.title("Store Analytics Dashboard")

queries = {
    "Select a query": None,
    "Give details about all stores with shrinkage rate greater than or equal to 3": "SELECT s.Store_ID, s.Store_Location_Type, s.Shrinkage_Rate, s.`Store-Specific_Shrinkage_Reduction_Strategies`\nFROM shrinkageStores s\nWHERE s.Shrinkage_Rate >= 3\nORDER BY s.Store_ID ASC;",
    "Give details about all products with shrinkage rates more than 4.9": "SELECT s.Product_ID, s.Shrinkage_Rate, s.Root_Cause_Analysis, s.Loss_Prevention_Measures\nFROM shrinkageAndLossPrevention s\nWHERE s.Shrinkage_Rate > 4.9\nORDER BY s.Shrinkage_Rate DESC;",
    "List all customers aged over 50 who have spent more than $15000": "SELECT c.Customer_ID, c.Customer_Name, c.Age, c.Total_Spent, c.Gender, c.Loyalty_Status\nFROM customers c\nWHERE c.Age > 50 AND c.Total_Spent > 15000\nORDER BY c.Total_Spent DESC;",
    "Give the performance evaluation of the suppliers with the top 25 order picking accuracies": "SELECT sm.Supplier_Name, sm.Supplier_Performance_Evaluation, opf.Order_Picking_Accuracy\nFROM supplierMetrics sm\nJOIN orderPickingAndFulfillment opf ON sm.Supplier_ID = opf.Supplier_ID\nORDER BY opf.Order_Picking_Accuracy DESC\nLIMIT 25;",
    "List the allocation strategies for products with the 30 lowest inventory turnover rates": "SELECT p.Product_ID, p.Inventory_Allocation_Strategy, i.Safety_Stock_Levels, i.Inventory_Monthly_Turnover_Rate\nFROM promotionalAndMarketData p\nJOIN inventoryMetrics i ON p.Product_ID = i.Product_ID\nORDER BY i.Inventory_Monthly_Turnover_Rate DESC\nLIMIT 30;",
    "Give the loss prevention audit findings of all stores with sales per square foot below 300": "SELECT s.Store_ID, s.LossPreventionAudit_Findings, se.Sales_per_SquareFoot\nFROM shrinkageStores s\nJOIN storeEfficiency se ON s.Store_ID = se.Store_ID\nWHERE se.Sales_per_SquareFoot < 300\nORDER BY s.Store_ID ASC;",
}

selected_query = st.selectbox("Select a query", list(queries.keys()))

if selected_query and selected_query != "Select a query":
    query_sql = queries[selected_query]
    result = execute_query(query_sql)
    # st.dataframe(result, height = 300)

    if not result.empty:
        st.subheader("Visualizations")

        if selected_query == "Give details about all products with shrinkage rates more than 4.9":
            root_cause_counts = result['Root_Cause_Analysis'].value_counts().reset_index()
            root_cause_counts.columns = ['Root_Cause_Analysis', 'Count']
            st.title("Count of Product by Root Cause Analysis")
            fig = px.bar(
                root_cause_counts,
                x = 'Root_Cause_Analysis',
                y = 'Count',
            )
            st.plotly_chart(fig)

            measures_counts = result.groupby(['Root_Cause_Analysis', 'Loss_Prevention_Measures']).size().reset_index(name = 'Count')
            pivot_df = measures_counts.pivot(index = 'Root_Cause_Analysis', columns = 'Loss_Prevention_Measures', values = 'Count').fillna(0)
            st.title("Loss Prevention Measures by Root Cause Analysis")
            plotly_fig = px.bar(
                measures_counts,
                x = "Root_Cause_Analysis",
                y = "Count",
                color = "Loss_Prevention_Measures",
                barmode = "group",
                labels = {"Root_Cause_Analysis": "Root Cause Analysis", "Count": "Count of Loss Prevention Measures"}
            )
            st.plotly_chart(plotly_fig)

        elif selected_query == "Give details about all stores with shrinkage rate greater than or equal to 3":
            location_counts = result['Store_Location_Type'].value_counts().reset_index()
            location_counts.columns = ['Store_Location_Type', 'Count']
            st.title("Store Location Types")
            pie_fig = px.pie(
                location_counts,
                names = 'Store_Location_Type',
                values = 'Count',
            )
            st.plotly_chart(pie_fig)

            strategy_counts = result['Store-Specific_Shrinkage_Reduction_Strategies'].value_counts().reset_index()
            strategy_counts.columns = ['Store-Specific_Shrinkage_Reduction_Strategies', 'Count']
            st.title("Shrinkage Reduction Strategies")
            bar_fig = px.bar(
                strategy_counts,
                x = 'Store-Specific_Shrinkage_Reduction_Strategies',
                y = 'Count',
            )
            st.plotly_chart(bar_fig)

        elif selected_query == "List all customers aged over 50 who have spent more than $15000":
            gender_spent = result.groupby('Gender')['Total_Spent'].sum().reset_index()
            st.title("Total Sum of Money Spent by Customers of Each Gender")
            pie_fig_gender = px.pie(
                gender_spent,
                names = 'Gender',
                values = 'Total_Spent',
                title = 'Total Spending by Gender'
            )
            st.plotly_chart(pie_fig_gender)

            result['Age_Group'] = pd.cut(result['Age'], bins=range(50, 100, 5))
            result['Age_Group'] = result['Age_Group'].astype(str)
            age_spent = result.groupby('Age_Group')['Total_Spent'].sum().reset_index()
            st.title("Total Sum of Money Spent by Age Group")
            bar_fig_age = px.bar(
                age_spent,
                x = 'Age_Group',
                y = 'Total_Spent',
                title = 'Total Spending by Age Group'
            )
            st.plotly_chart(bar_fig_age)

            loyalty_spent = result.groupby('Loyalty_Status')['Total_Spent'].sum().reset_index()
            st.title("Total Sum of Money Spent by Loyalty Status")
            pie_fig_loyalty = px.pie(
                loyalty_spent,
                names = 'Loyalty_Status',
                values = 'Total_Spent',
                title = 'Total Spending by Loyalty Status'
            )
            st.plotly_chart(pie_fig_loyalty)

        elif selected_query == "Give the performance evaluation of the suppliers with the top 25 order picking accuracies":
            evaluation_counts = result['Supplier_Performance_Evaluation'].value_counts().reset_index()
            evaluation_counts.columns = ['Supplier_Performance_Evaluation', 'Count']
            st.title("Performance Evaluation of Suppliers")
            pie_fig_evaluation = px.pie(
                evaluation_counts,
                names = 'Supplier_Performance_Evaluation',
                values = 'Count',
                title = 'Supplier Performance Evaluation'
            )
            st.plotly_chart(pie_fig_evaluation)

        elif selected_query == "List the allocation strategies for products with the 30 lowest inventory turnover rates":
            turnover_by_strategy = result.groupby('Inventory_Allocation_Strategy')['Inventory_Monthly_Turnover_Rate'].sum().reset_index()
            st.title("Sum of Inventory Turnover Rates by Allocation Strategy")
            bar_fig_turnover = px.bar(
                turnover_by_strategy,
                x = 'Inventory_Allocation_Strategy',
                y = 'Inventory_Monthly_Turnover_Rate',
                title = 'Sum of Inventory Turnover Rates by Allocation Strategy'
            )
            st.plotly_chart(bar_fig_turnover)

            safety_stock_by_strategy = result.groupby('Inventory_Allocation_Strategy')['Safety_Stock_Levels'].sum().reset_index()
            st.title("Sum of Safety Stock Levels by Allocation Strategy")
            bar_fig_safety_stock = px.bar(
                safety_stock_by_strategy,
                x = 'Inventory_Allocation_Strategy',
                y = 'Safety_Stock_Levels',
                title = 'Sum of Safety Stock Levels by Allocation Strategy'
            )
            st.plotly_chart(bar_fig_safety_stock)

        elif selected_query == "Give the loss prevention audit findings of all stores with sales per square foot below 300":
            audit_counts = result['LossPreventionAudit_Findings'].value_counts().reset_index()
            audit_counts.columns = ['LossPreventionAudit_Findings', 'Count']
            st.title("Count of Store IDs for Each Loss Prevention Audit Finding")
            pie_fig_audit = px.pie(
                audit_counts,
                names = 'LossPreventionAudit_Findings',
                values = 'Count',
                title = 'Loss Prevention Audit Findings'
            )
            st.plotly_chart(pie_fig_audit)

            avg_sales = result.groupby('Store_ID')['Sales_per_SquareFoot'].mean().reset_index()
            st.title("Average Sales per Square Foot by Store ID")
            line_fig_sales = px.line(
                avg_sales,
                x = 'Store_ID',
                y = 'Sales_per_SquareFoot',
                title='Average Sales per Square Foot by Store ID'
            )
            st.plotly_chart(line_fig_sales)

else:
    st.write("Please select a query from the dropdown menu.")
