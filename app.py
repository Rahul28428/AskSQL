import streamlit as st
import os
import sqlite3
import google.generativeai as genai
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
import pandas as pd

# Load environment variables
load_dotenv()

# Configure Google Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini Model and provide queries as response
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    return response.text.strip()

# Function to retrieve query from the database
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    col_names = [description[0] for description in cur.description]
    conn.commit()
    conn.close()
    return col_names, rows

# Define your prompt
prompt_template = """
You are an expert in converting English questions to SQL query!
The SQL database has the name {table_name} and has the following columns - {columns}
For example,
Example 1 - How many entries of records are present?, the SQL command will be something like this: SELECT COUNT(*) FROM {table_name};
Example 2 - Tell me all the students studying in Data Science class?, the SQL command will be something like this: SELECT * FROM {table_name} WHERE CLASS="Data Science";
also the SQL code should not have 
in the beginning or end and the word 'sql' should not be in the output.
"""

# Streamlit App
st.set_page_config(page_title="SQL Query Retriever", layout="wide")
st.header("Gemini App To Retrieve SQL Data")

# Sidebar for database configuration
with st.sidebar:
    st.title("Database Configuration")
    db_file = st.file_uploader("Upload your SQLite Database", type="db")
    table_name = st.text_input("Enter the table name")
    column_names = st.text_input("Enter the column names (comma-separated)")

    if st.button("Submit & Process"):
        if db_file and table_name and column_names:
            st.session_state.db_file = db_file
            st.session_state.table_name = table_name
            st.session_state.column_names = [col.strip() for col in column_names.split(",")]
            st.success("Database configuration saved!")
        else:
            st.warning("Please provide all required inputs.")

# Instructions for the user
st.markdown("""
Welcome to the SQL Query Retriever! You can ask questions about the data, and the app will convert your question into an SQL query and fetch the relevant data. For example:
- "How many records are present?"
- "Tell me all the students studying in Data Science class."
""")

# Check if database configuration is available
if "db_file" in st.session_state and "table_name" in st.session_state and "column_names" in st.session_state:
    # Initialize conversation memory
    if "memory" not in st.session_state:
        st.session_state.memory = ConversationBufferMemory(memory_key="history", input_key="question")

    if "chat_history" in st.session_state:
        chat_history = st.session_state["chat_history"]
    else:
    # Initialize chat history if not present
        chat_history = []
        st.session_state["chat_history"] = chat_history

    # Display chat history
    for message in chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["text"])

    # User input for questions
    user_question = st.chat_input("Ask a question about your database")
    if user_question:
        st.session_state.get("chat_history", []).append({"role": "user", "text": user_question})
        st.chat_message("user").markdown(user_question)

        # Process the user question
        with st.spinner("Processing your query..."):
            try:
                # Generate SQL query from user question
                context = prompt_template.format(
                    table_name=st.session_state.table_name,
                    columns=", ".join(st.session_state.column_names)
                )
                response = get_gemini_response(user_question, [context])
                st.subheader("Generated SQL Query:")
                st.code(response, language='sql')

                # Execute the SQL query
                col_names, result = read_sql_query(response, st.session_state.db_file.name)
                if result:
                    df = pd.DataFrame(result, columns=col_names)
                    assistant_response = f"Query Results:\n{df.to_markdown()}"
                    st.subheader("Query Results:")
                    st.dataframe(df)
                else:
                    assistant_response = "No results found."
                    st.warning(assistant_response)

                # Append assistant response to chat history without displaying it again
                chat_history.append({"role": "assistant", "text": assistant_response})
                st.session_state["chat_history"] = chat_history

            except Exception as e:
                st.error(f"An error occurred: {e}")

else:
    st.warning("Please configure the database settings in the sidebar.")
