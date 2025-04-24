import streamlit as st
import psycopg2
from psycopg2 import Error
import pandas as pd
import io

# Database connection parameters for AWS RDS
db_params = {
    "host": "dmqlproject.ccv00icswcgq.us-east-1.rds.amazonaws.com",
    "database": "postgres",
    "user": "dmqlRdsLogin",
    "password": "dmqlRdsPassword",
    "port": "5432"
}

# Function to connect to PostgreSQL
def connect_to_db():
    try:
        connection = psycopg2.connect(**db_params)
        return connection
    except Error as e:
        st.error(f"Error connecting to PostgreSQL: {e}")
        return None

# Function to execute query and fetch results
def run_query(connection, query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        
        # Check if the query returns results (e.g., SELECT)
        if cursor.description:
            columns = [desc[0] for desc in cursor.description]
            results = cursor.fetchall()
            df = pd.DataFrame(results, columns=columns)
            return df
        else:
            # For non-SELECT queries (e.g., INSERT, UPDATE)
            connection.commit()
            return pd.DataFrame({"Message": ["Query executed successfully."]})
    except Error as e:
        st.error(f"Error executing query: {e}")
        return None
    finally:
        cursor.close()

# Function to convert DataFrame to Excel
def to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Query_Results')
    excel_data = output.getvalue()
    return excel_data

# Streamlit app
def main():
    st.title("PostgreSQL Query Runner")
    st.write("Enter a SQL query to run against the DMQL_Project database.")

    # Initialize session state for query
    if "query" not in st.session_state:
        st.session_state.query = "SELECT * FROM Arrests LIMIT 10;"

    # Text area for query input
    query = st.text_area("SQL Query", value=st.session_state.query, height=150)

    # Update session state when query changes
    if query != st.session_state.query:
        st.session_state.query = query

    # Run query button
    if st.button("Run Query"):
        # Connect to database
        connection = connect_to_db()
        if connection:
            # Execute query
            result_df = run_query(connection, st.session_state.query)
            if result_df is not None:
                st.dataframe(result_df, use_container_width=True)
                
                # Provide download button for Excel
                excel_data = to_excel(result_df)
                st.download_button(
                    label="Download Results as Excel",
                    data=excel_data,
                    file_name="query_results.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            connection.close()
        else:
            st.error("Failed to connect to the database.")

if __name__ == "__main__":
    main()