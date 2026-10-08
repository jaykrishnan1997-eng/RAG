# RAG

# Day 0

## RAG-basics:
1. Res from git: https://arxiv.org/pdf/2005.11401
2. What is LLM: https://www.iese.fraunhofer.de/blog/retrieval-augmented-generation-rag/
3. What is LLM: https://www.ibm.com/think/topics/retrieval-augmented-generation
4. Parametric and non-parametric memory: https://lawrence-emenike.medium.com/a-straightforward-explanation-of-parametric-vs-non-parametric-memory-in-llms-f0b00ac64167
5. Fine-tuning RAG: https://arxiv.org/pdf/2505.10792
6. RAG vs Finetuning: https://www.ibm.com/think/topics/rag-vs-fine-tuning
7. Understanding Recall@k: https://krishnapullak.medium.com/understanding-precision-recall-and-f-score-at-k-in-recommender-systems-7146a0dce68e
8. RAG Indexing: https://medium.com/@j13mehul/rag-part-4-indexing-1985f4000f72
9. Chunking and types of chunking :https://community.databricks.com/t5/technical-blog/the-ultimate-guide-to-chunking-strategies-for-rag-applications/ba-p/113089
10. Retrieval methods: TF-IDF vs BM25: https://kmwllc.com/index.php/2020/03/20/understanding-tf-idf-and-bm-25/


### What is RAG:
1. Retrieval Augmented Generation is an architecture for optimizing the performance of an AI model by connecting it to external knowledge bases: databases, document collections etc.[2][3]

### Benefits of RAG:[3]
1. Larger information pool availablilty so more relevant data source.
2. Access to current domain-specific data

### Types of memory:[4]
1. Parametric memory: Knowledge hard-coded directly into the LLM's weights during training.
2. Non-parametric memory: Retrieving\storing external knowledge using RAG and Vector databases.

# NOTE: 
The difference between Parametric and non-Parametric memory is available in [4].

### What is indexing in RAG:
Organizing a vast amount of text data in a way that allows RAG system to quickly access the most relevant piece of information for given query.[6]

### Chunking stratergies:
Subject requires two distinct chunking stratergies:
1. Python code chunking
2. Markdown / text chunking

A good resource for chunking:[9]. Also contain different methods of chunking.


### Retrieval methods:
1. TFT-IDF
2. BM25
# NOTE:
At least one of this must be implemented.
 