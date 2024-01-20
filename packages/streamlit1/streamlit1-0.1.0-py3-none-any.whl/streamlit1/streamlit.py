import streamlit as st
import psycopg2

# Modify these parameters with your PostgreSQL database details
db_params = {
    'host': '10.0.0.112',
    'database': 'postgres',
    'user': 'postgres',
    'password': 'postgres',
    'port': '5432',
}

def connect_to_database():
    # Create a connection to the database
    connection = psycopg2.connect(**db_params)
    return connection

def create_table(connection):
    # Open a cursor to perform database operations
    with connection.cursor() as cursor:
        # Create a simple table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vcluster (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100)
            )
        """)

    # Commit the changes
    connection.commit()

def insert_data_into_table(connection, name):
    # Open a cursor to perform database operations
    with connection.cursor() as cursor:
        # Insert data into the table
        cursor.execute("""
            INSERT INTO vcluster (name) VALUES (%s)
        """, (name,))

    # Commit the changes
    connection.commit()

def main():
    st.title("PostgreSQL Streamlit App")

    # Connect to the PostgreSQL database
    connection = connect_to_database()

    # Create a table (if not exists)
    create_table(connection)

    # Streamlit UI
    operation = st.sidebar.selectbox("Select Operation", ["Create Table", "Insert Data"])

    if operation == "Create Table":
        st.header("Create Table")

        # Display information about the table
        st.write("The 'vcluster' table has columns:")
        st.write("- id (auto-incrementing primary key)")
        st.write("- name (a variable character field)")

    elif operation == "Insert Data":
        st.header("Insert Data")

        # Get user input for data insertion
        name = st.text_input("Enter Name:")
        if st.button("Insert Data"):
            # Insert data into the table
            insert_data_into_table(connection, name)
            st.success("Data inserted successfully!")

    # Close the database connection
    connection.close()

if __name__ == "__main__":
    main()




