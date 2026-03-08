import streamlit as st
import pandas as pd
from extraction import extract_courses_from_pdf
from recommendations import lexical_jaccard, suggest_course, sorense_dice


def run_lexical_similarity():
    st.subheader("Lexical Similarity")
    st.write("""
        ### Upload your Transcript
        Please upload your transcript in PDF format. The application will extract the courses and compare them with the Bioinformatics BSc program requirements using lexical similarity.
        """)

    uploaded_file = st.file_uploader("Choose a file", type="pdf")
    option = st.selectbox(
        "Method to suggest?",
        ("lexical_jaccard", "cosine_similarity", "sorense_dice"))
    st.write("You selected:", option)
    if st.button("See Recommendation"):
        if uploaded_file is not None:
            st.write("Processing your transcript...")
            try:
                courses = extract_courses_from_pdf(uploaded_file)
                st.write("Courses extracted from the PDF:")
                st.write(courses)

                if option == "lexical_jaccard":
                    recommended_courses = lexical_jaccard(courses)
                elif option == "sorense_dice":
                    recommended_courses = sorense_dice(courses)
                else:
                    recommended_courses = suggest_course(courses)

                st.write(f"Recommended Courses by {option}")
                if recommended_courses:
                    for course, matches in recommended_courses.items():
                        st.write(f"**{course}**")
                        st.table(pd.DataFrame(matches, columns=["Matching Courses"]))
                else:
                    st.write("No matching courses found.")
            except Exception as e:
                st.write("An error occurred while processing the PDF file.")
                st.write(str(e))
        else:
            st.write("Please upload a PDF file to see recommendations.")


def run_semantic_similarity():
    st.subheader("Semantic Similarity")
    st.write("""
        ### Upload your Transcript
        Please upload your transcript in PDF format. The application will extract the courses and compare them with the Bioinformatics BSc program requirements using semantic similarity.
        """)

    st.write("Semantic similarity model will be added here.")
