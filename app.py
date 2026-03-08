import streamlit as st 
import streamlit.components.v1 as stc 
from recommendation_app import run_lexical_similarity, run_semantic_similarity
import pandas as pd

html_temp = """
    <div style="background-color:#3872fb;padding:10px;border-radius:10px">
    <h1 style="color:white;text-align:center;">Course Recommendation Web App</h1>
    <h4 style="color:white;text-align:center;">Bioinformatics BSc Program</h4>
    </div>
    """

def display_program_curriculum():
    # Load curriculum data from CSV
    df_curriculum = pd.read_csv('bioinformatics_curriculum.csv')
    st.subheader("Program Curriculum Overview")
    st.table(df_curriculum)

def main():
    stc.html(html_temp)

    # Sidebar navigation
    st.sidebar.title("Navigation")
    menu = ["Home", "Lexical Similarity", "Semantic Similarity"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    if choice == "Home":
        st.subheader("Home")
        st.write("""
            ### Welcome to the Course Recommendation Web App
            This application helps students assess how well their GPA transcripts match the qualifications for the Bioinformatics BSc program at Langara College.
        """)
        display_program_curriculum()
    
    elif choice == "Lexical Similarity":
        run_lexical_similarity()
        
    elif choice == "Semantic Similarity":
        run_semantic_similarity()

if __name__ == '__main__':
    main()
