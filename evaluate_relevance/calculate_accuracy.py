from promptflow import log_metric, tool
from typing import List


@tool
def calculate_accuracy(grades: List[str]):
    grades = [eval(i) for i in grades]

    accuracy = round((sum(grades) / (len(grades) * 5)), 2)
    log_metric("accuracy", accuracy)

    return [accuracy]
