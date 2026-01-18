from query import get_section_using_llm
import json
QUESTIONS_FOR_LLM=[
    "who can develop android app",
    "who is intrested in sports",
    "who can play football",
    "who worked on lambdazen",
    "any android developer who is intrested in sports"
]
def main():
    result=[]
    for ques in QUESTIONS_FOR_LLM:
        section=get_section_using_llm(ques)
        result.append({
            "question":ques,
            "section":section
        })
    with open("test_results.json", "w") as f:
        json.dump(result, f, indent=4)
    print(result)


if __name__ == "__main__":
    main()
