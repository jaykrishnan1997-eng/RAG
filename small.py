import json
p = "data/output/search_results/UnansweredQuestions/dataset_docs_public.json"
d = json.load(open(p))
d["search_results"] = d["search_results"][:5]
json.dump(d, open("/tmp/small.json", "w"))
