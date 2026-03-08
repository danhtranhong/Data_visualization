import textdistance as td
import spacy

langara_bioinfo = [
    "General Biology I", "General Chemistry I", "Program Design", "Program Design for Engineers", "Calculus I",
    "Calculus I with application to life sciences", "General Biology II", "General Chemistry II",
    "Algorithms and Data Structures I", "Calculus II", "Calculus II with application to life sciences", "Cell Biology",
    "Organic Chemistry for Life Sciences", "Object-oriented Computing", "Linear Systems", "Linear Algebra",
    "Biochemistry",
    "Introduction to Genetics", "Database Systems", "Descriptive and Elementary Inferential Statistics",
    "Evolution and Phylogenetics", "Cloud and Parallel Computing", "Algorithms and Data Structures II",
    "Statistical Methods for Biological and Health Sciences", "Employment Strategies for Current Labour Market",
    "Molecular Genetics", "Data Transformations", "Probability and Elementary Mathematical Statistics",
    "Genomics, Metagenomics and Transcriptomics", "Molecular Modelling", "Data Mining and Machine Learning",
    "Proteomics and Metabolomics", "Bioinformatics", "Data Visualization", "Capstone I", "Capstone II",
    "Industry Topics"
]


def lexical_jaccard(transcript_courses, langara_courses=langara_bioinfo):
    threshold = 0.5
    matches = {}
    matching_terms = {}

    for course in transcript_courses:
        matched_courses = []
        scores = []

        for langara_course in langara_courses:
            similarity_score = td.jaccard.similarity(course, langara_course)
            if similarity_score >= threshold:
                matched_courses.append(langara_course)
                scores.append(similarity_score)

        if matched_courses:
            matches[course] = matched_courses
            matching_terms[course] = scores

    return matches


nlp = spacy.load("en_core_web_md")
def cal_cosine_similarity(course_a, course_b):
    doc_a = nlp(course_a)
    doc_b = nlp(course_b)
    return doc_a.similarity(doc_b)

def compute_dice_sim(str1, str2):
    a = set(str1.split())
    b = set(str2.split())
    c = a.intersection(b)
    return 2 * float(len(c)) / (len(a) + len(b))



def suggest_course(transcript_courses, langara_courses=langara_bioinfo):
    threshold = 0.7
    matches = {}
    matching_terms = {}

    for course in transcript_courses:
        matched_courses = []
        scores = []

        for langara_course in langara_courses:
            similarity_score = cal_cosine_similarity(course, langara_course)
            if similarity_score >= threshold:
                matched_courses.append(langara_course)
                scores.append(similarity_score)

        if matched_courses:
            matches[course] = matched_courses
            matching_terms[course] = scores

    return matches

def sorense_dice(transcript_courses, langara_courses=langara_bioinfo):
    threshold = 0.7
    matches = {}
    matching_terms = {}

    for course in transcript_courses:
        matched_courses = []
        scores = []

        for langara_course in langara_courses:
            similarity_score = compute_dice_sim(course, langara_course)
            if similarity_score >= threshold:
                matched_courses.append(langara_course)
                scores.append(similarity_score)

        if matched_courses:
            matches[course] = matched_courses
            matching_terms[course] = scores

    return matches
