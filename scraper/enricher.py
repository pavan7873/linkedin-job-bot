import re

SKILLS = [
    "Azure Data Factory",
    "ADF",
    "Azure Databricks",
    "Databricks",
    "Microsoft Fabric",
    "Fabric",
    "PySpark",
    "Spark",
    "Spark SQL",
    "SQL",
    "Python",
    "Azure",
    "Synapse",
    "Delta Lake",
    "Power BI",
    "ADF",
    "ETL",
    "Data Engineering"
]


def extract_skills(text):

    found_skills = []

    text_lower = text.lower()

    for skill in SKILLS:

        if skill.lower() in text_lower:
            found_skills.append(skill)

    return sorted(set(found_skills))