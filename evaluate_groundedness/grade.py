from promptflow.core import tool


@tool
def grade(link: str, answer: str):
    print(f"Ground truth {link}")
    print(f"Grading answer {answer}")

    return "Correct" if link in answer else "Incorrect"
