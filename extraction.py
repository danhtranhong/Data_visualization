import pdfplumber
import re


def extract_text_with_pdfplumber(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text


def extract_table_from_pdf_v2(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        final_text = ''
        for page in pdf.pages:
            if page.extract_tables():
                # Extract tables if present
                rows = []
                for table in page.extract_tables():
                    for row in table:
                        combined_text = ' '.join(
                            [str(element).replace('\n', ' ') for element in row if element is not None])
                        rows.append(combined_text)
                final_text = final_text + ('\n'.join(rows))
            else:
                # Extract text if no tables are detected
                text = page.extract_text()
                final_text = final_text + text
        return final_text


def courses_for_matching(text):
    # course_pattern = r'[A-Z]{2,5}\s*\d{3,4}\s*[\w\s&/-]+(?=\s*[^\d\s])'
    # course_pattern = r'[A-Z]{2,5}\s*\d{3,4}\s*[\w\s-]+(?=\s*[^\d\s])'
    # course_pattern = r'[A-Z]{2,5}\s*\d{3,4}\s*[\w\s&/-]+(?:\.\s*)?(?=\s*[^\d\s])'
    course_pattern = r'[A-Z]{2,5}\s*\d{3,4}\s*[\w\s&/-]*(?:\.\s*(?!\d)[\w\s&/-]*)?'
    courses = re.findall(course_pattern, text)

    # Pattern to capture the course title while accounting for optional credit numbers
    pattern = re.compile(r'\b\d*\s*[A-Z]{2,5}\s*\d{3,4}[A-Z]*\s(.*?)(?:\s\d+)?\s*$')

    # Extract course titles from each item in the list
    course_titles = []
    for course in courses:
        matches = pattern.findall(course)
        course_titles.extend([match.strip() for match in matches])

    items_to_remove = ['or', 'and']
    filtered_list = filter_list(course_titles, items_to_remove)

    return filtered_list


def filter_list(input_list, items_to_remove):
    # Create a new list excluding the items to remove
    filtered_list = [item for item in input_list if item not in items_to_remove]
    return filtered_list


def extract_courses_from_pdf(pdf_file):
    pdf_text = extract_table_from_pdf_v2(pdf_file)
    courses = courses_for_matching(pdf_text)
    return courses


# import pdfplumber
# import re
#
# def extract_text_with_pdfplumber(pdf_file):
#     text = ""
#     with pdfplumber.open(pdf_file) as pdf:
#         for page in pdf.pages:
#             text += page.extract_text()
#     return text
#
# def courses_for_matching(text):
#     course_pattern = r'[A-Z]{2,5}\s*\d{3,4}\s*[\w\s-]+(?=\s*[^\d\s])'
#     courses = re.findall(course_pattern, text)
#     return courses
#
# def extract_courses_from_pdf(pdf_file):
#     pdf_text = extract_text_with_pdfplumber(pdf_file)
#     courses = courses_for_matching(pdf_text)
#     return courses