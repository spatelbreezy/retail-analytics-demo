import streamlit as st
import pandas as pd
import pymysql
import plotly.express as px
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection function
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
    "Give details about all stores with shrinkage rate greater than or equal to 3": "SELECT s.Store_ID, s.Store_Location_Type, s.Shrinkage_Rate, s.`Store-Specific_Shrinkage_Reduction_Strategies`\nFROM shrinkageStores s\nWHERE s.Shrinkage_Rate >= 3\nORDER BY s.Store_ID ASC",
    "Give details about all products with shrinkage rates more than 4.9": "SELECT s.Product_ID, s.Shrinkage_Rate, s.Root_Cause_Analysis, s.Loss_Prevention_Measures\nFROM shrinkageAndLossPrevention s\nWHERE s.Shrinkage_Rate > 4.9\nORDER BY s.Shrinkage_Rate DESC",
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

else:
    st.write("Please select a query from the dropdown menu.")