import streamlit as st
import ast
import traceback

def check_errors(code):
    try:
        # Try parsing the code to detect syntax errors
        ast.parse(code)
        return "✅ No syntax errors detected!", "success", None
    except SyntaxError as e:
        error_message = f"Syntax Error: {e.msg} at line {e.lineno}, column {e.offset}"
        suggestion = suggest_fix(e)
        return error_message, "error", suggestion
    except Exception as e:
        error_message = f"Runtime Error: {str(e)}"
        return error_message, "error", None

def suggest_fix(error):
    if "expected ':'" in error.msg:
        return "You forgot the colon (:) after the function or loop definition.\nExample Fix: def my_function():"
    elif "unexpected EOF while parsing" in error.msg:
        return "Your code might be incomplete or missing a closing bracket."
    elif "invalid syntax" in error.msg:
        return "Check for typos or missing symbols like parentheses, commas, or quotes."
    return "No specific suggestion found. Review the error message carefully."

# Streamlit UI
st.set_page_config(page_title="Error Resolver Tool", page_icon="🔍")
st.title("🔍 Error Resolver Tool")
st.write("Enter your Python code below to check for errors and get suggestions.")

code = st.text_area("Write your Python code here:")

if st.button("Check & Fix Errors"):
    if code.strip():
        error_message, msg_type, suggestion = check_errors(code)
        
        if msg_type == "error":
            st.error(error_message)
            if suggestion:
                st.info(f"💡 Suggestion: {suggestion}")
        else:
            st.success(error_message)
    else:
        st.warning("Please enter some code before checking!")
