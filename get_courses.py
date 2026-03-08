import pdfplumber
import os
import re
import pandas as pd
from fuzzywuzzy import fuzz, process

import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import spacy
import textdistance as td

progression_map_courses = [
    "BIOL 1115 General Biology I",
    "BIOL 1215 General Biology II",
    "BIOL 2415 Cell Biology",
    "BIOL 2315 Biochemistry",
    "BIOL 3315 Evolution and Phylogenetics",
    "BIOL 3430 Molecular Genetics",
    "BIOL 4315 Genomics, Metagenomics and Transcriptomics",
    "BIOL 4415 Proteomics and Metabolomics",
    "CHEM 1120 General Chemistry I",
    "CHEM 1220 General Chemistry II",
    "CHEM 2216 Organic Chemistry for Life Sciences",
    "BIOL 2330 Introduction to Genetics",
    "CPSC 3280 Cloud and Parallel Computing",
    "CPSC 3260 Data Transformations",
    "CPSC 1150 Program Design",
    "CPSC 1160 Algorithms and Data Structures I",
    "CPSC 1181 Object-oriented Computing",
    "CPSC 2221 Database Systems",
    "CPSC 2150 Algorithms and Data Structures II",
    "MATH 1252 Linear Systems",
    "STAT 1181 Descriptive and Elementary Inferential Statistics",
    "STAT 3225 Statistical Methods for Biological and Health Sciences",
    "STAT 2281 Probability and Elementary Mathematical Statistics",
    "BINF 4125 Capstone I",
    "BINF 4225 Capstone II",
    "EXPE 2300 Employment Strategies for Current Labour Market"
]

matches = []
threshold = 0.1
nlp = spacy.load("en_core_web_md")


# Using Spacy model
def cal_cosine_similarity(course_a, course_b):
    doc_a = nlp(course_a)
    doc_b = nlp(course_b)
    return doc_a.similarity(doc_b)


# By function sklearn
def compute_vectors(*strs):
    text = [t for t in strs]
    vectorizer = CountVectorizer()
    vectorizer.fit(text)
    return vectorizer.transform(text).toarray()


def compute_cosine_sim(str1, str2):
    vectors = compute_vectors(str1, str2)
    similarity_matrix = cosine_similarity(vectors)
    return similarity_matrix[0, 1]


def compute_jaccard_sim(str1, str2):
    a = set(str1.split())
    b = set(str2.split())
    c = a.intersection(b)
    return float(len(c)) / (len(a) + len(b) - len(c))


def compute_dice_sim(str1, str2):
    a = set(str1.split())
    b = set(str2.split())
    c = a.intersection(b)
    return 2 * float(len(c)) / (len(a) + len(b))


def suggest_course(trans_course):
    with open(trans_course, 'r') as file:
        for line in file:
            best_match = None
            best_score = 0
            for course in progression_map_courses:
                #    print(course)
                similarity_score = cal_cosine_similarity(line, course)
                # print(similarity_score)
                if similarity_score >= threshold:
                    best_score = similarity_score
                    best_match = (line, course, best_score)
            if best_match:
                matches.append(best_match)
        print("Matched Courses:")
        for match in matches:
            print(f"Learned course: {match[0]}  Suggest Course: {match[1]} ")


## SFU courses
def suggest_course_sklearn(trans_course):
    with open(trans_course, 'r') as file:
        # Read each line in the file
        for line in file:
            for course in progression_map_courses:
                comp_cs = compute_cosine_sim(line, course)
                if comp_cs >= threshold:
                    a = (line, course)
                    matches.append(a)
    for match_course in matches:
        print(f"Learned course: {match_course[0]}  Suggest Course: {match_course[1]} ")


def suggest_course_jaccard_sim(trans_course):
    with open(trans_course, 'r') as file:
        # Read each line in the file
        for line in file:
            for course in progression_map_courses:
                comp_cs = compute_jaccard_sim(line, course)
                if comp_cs >= threshold:
                    a = (line, course)
                    matches.append(a)
    for match_course in matches:
        print(f"Learned course: {match_course[0]}  Suggest Course: {match_course[1]} ")
