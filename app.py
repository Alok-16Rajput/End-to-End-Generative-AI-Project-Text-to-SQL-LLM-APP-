from dotenv import load_dotenv
import streamlit as st
import os
import sqlite3
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load Google Gemini Model and provide SQL query as response
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt, question]).text.strip()
    
    # Remove Markdown formatting if present
    response = response.replace("```sql", "").replace("```", "").strip()
    response = response.replace("\n", " ")  # Convert multi-line SQL into a single line

    return response
  # Strip whitespace or newlines

## Function to retrieve query results from the SQL database
def read_sql_query(sql, db):
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()  # Fetch all results
        conn.close()
        return rows
    except sqlite3.Error as e:
        return [("Error:", str(e))]  # Return error as response

## Define the Prompt
prompt = """
You are an expert in converting English questions to SQL queries.
The SQL database is named 'STUDENT' and contains the following columns: NAME, CLASS, SECTION, and MARKS.

Example 1:
- Question: How many records are present?
- SQL: SELECT COUNT(*) FROM STUDENT;

Example 2:
- Question: Tell me all students studying in data science class?
- SQL: SELECT * FROM STUDENT WHERE CLASS='Data Science'';

- SQLite **DOES NOT** support "OFFSET ... ROWS FETCH NEXT ...".
- Instead, use "LIMIT 1 OFFSET X" when retrieving specific rows.
    
Example 3:
Question: Find the student with the third-highest marks.
SQL: SELECT NAME, MARKS FROM STUDENT ORDER BY MARKS DESC LIMIT 1 OFFSET 2;

Ensure the output is only the SQL query with no additional text, comments, or formatting.
"""

## Streamlit App
st.set_page_config(page_title="Retrieve Any SQL Query")
st.header("Gemini App to Retrieve SQL Data")

# User input
question = st.text_input("Enter your question:", key="input")
submit = st.button("Generate SQL Query and Retrieve Data")

## If submit is clicked
if submit:
    if question:
        response = get_gemini_response(question, prompt)
        
        st.subheader("Generated SQL Query:")
        st.code(response, language="sql")  # Display query in SQL format
        
        # Fetch data from database
        data = read_sql_query(response, "student.db")

        st.subheader("Query Results:")
        if data:
            for row in data:
                st.write(row)
        else:
            st.write("No data found.")
    else:
        st.warning("Please enter a question.")
