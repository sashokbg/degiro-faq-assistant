from promptflow.core import tool
from sentence_transformers import CrossEncoder

encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2', max_length=512, device='cpu')


def deduplicate(data: list[dict]) -> list[dict]:
    unique_items = dict()

    for entry in data:
        unique_items[entry['title']] = entry

    return list(unique_items.values())


@tool
def rerank(vector_results: list[dict], keyword_results: list[dict], question, max) -> list[dict]:
    results = vector_results + keyword_results
    results = deduplicate(results)

    return results

    # scores = encoder.predict([[question, item['title'] + " " + item['content']] for item in results])
    # sorted_top = sorted(zip(scores, results), reverse=True)[:max]
    #
    # filtered_top = []
    #
    # for element in sorted_top:
    #     # if element[0] > 0:
    #     element[1]['score'] = element[0]
    #     filtered_top.append(element[1])
    #
    # return filtered_top
