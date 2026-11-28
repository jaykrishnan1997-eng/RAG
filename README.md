*This project has been created as part of the 42 curriculum by jkrishna.*
 
# RAG against the machine
 
## Description
 
A Retrieval-Augmented Generation (RAG) system that answers questions about the
vLLM 0.10.1 codebase. It indexes the repository, retrieves the most relevant
snippets for a question with a hand-written BM25, and gives them to a small
local model (`Qwen/Qwen3-0.6B`) that writes an answer grounded in those
snippets. Retrieval quality is measured with recall@k.
 
**Goal:** a model only knows what it was trained on. Instead of retraining it,
we let it look up the right pages of a "manual" (the vLLM repo) at answer time.
 
**Overview of the features**
- Two chunking strategies (Python code, Markdown/text), max 2000 characters.
- BM25 retrieval implemented from scratch (no retrieval library).
- Persistent index under `data/processed/`.
- Fire CLI: `index`, `search`, `search_dataset`, `answer`, `answer_dataset`,
  `evaluate`.
- pydantic models for every structure exchanged between stages.
- `tqdm` progress bars for long operations.
## Instructions
 
**Requirements:** Python 3.10 to 3.12, [uv](https://docs.astral.sh/uv/).
Free disk space: about 2 GB for the environment (CPU-only torch) and about
1.5 GB for the model weights, downloaded on the first `answer` run.
 
```
make install                      # or: uv sync
uv run python -m src index --max_chunk_size 2000
```
 
The project layout expected by the evaluation:
 
```
src/                              Python module
data/raw/vllm-0.10.1/             indexed sources
data/processed/                   index written by `index`
data/datasets/UnansweredQuestions/ and AnsweredQuestions/
data/output/search_results/<DatasetScope>/
data/output/search_results_and_answer/<DatasetScope>/
```
 
**Makefile rules:** `install`, `run` (`make run ARGS='<command> ...'`, default
`index`), `debug`, `clean`, `fclean`, `lint`, `lint-strict`.
 
**Disk-space notes**
- The model is cached in `.hf-cache/` next to the project. On a machine with a
  small home quota (for example 42 campus accounts), symlink it to a bigger
  disk: `ln -s /goinfre/$USER/hf-cache .hf-cache`.
- The Makefile detects `/goinfre` and moves the venv and caches there
  automatically when you use `make`.
### Example usage
 
```
# 1. Index the corpus (once, and again after any chunker/tokenizer change)
uv run python -m src index --max_chunk_size 2000
 
# 2. Single query
uv run python -m src search "How to configure OpenAI server?" --k 10
uv run python -m src answer "How to configure OpenAI server?" --k 5
 
# 3. Whole dataset
uv run python -m src search_dataset \
  --dataset_path data/datasets/UnansweredQuestions/dataset_docs_public.json \
  --k 10 \
  --save_directory data/output/search_results/UnansweredQuestions
 
# 4. Own recall@k (the official score comes from the moulinette)
uv run python -m src evaluate \
  --student_search_results_path data/output/search_results/UnansweredQuestions/dataset_docs_public.json \
  --dataset_path data/datasets/AnsweredQuestions/dataset_docs_public.json
 
# 5. Generate answers from the saved search results
uv run python -m src answer_dataset \
  --student_search_results_path data/output/search_results/UnansweredQuestions/dataset_docs_public.json \
  --save_directory data/output/search_results_and_answer/UnansweredQuestions
```
 
Edge cases (empty query, `k=0`, missing file, malformed JSON, nonsense query)
print a one-line error or "No results found" and never a traceback.
 
## System architecture
 
```
Corpus (data/raw)
   |  os.walk, .py / .md / .txt
   v
Chunking  (Python: AST split-then-merge | Markdown/text: separators)
   |  chunks <= 2000 characters, each with file_path + character range
   v
Tokenizer --> vocabulary (token -> id) --> BM25 statistics
   |  persisted to data/processed/ (pickle + vocab JSON)
   v
Retrieve top-k chunks  --> StudentSearchResults JSON
   |
   v
Augment: re-read each source range from disk, build the context
   |
   v
Generate: Qwen3-0.6B (chat template, greedy) --> StudentSearchResultsAndAnswer JSON
```
 
Two commands are intentionally separate. `search_dataset` writes the search
results file, the moulinette scores that same file, and `answer_dataset`
reads it. The answers are therefore built from exactly the sources that were
scored.
 
| Module | Role |
|---|---|
| `src/__main__.py` | Fire CLI and the generation helper |
| `src/Base/model.py` | pydantic models, path table |
| `src/Base/parser.py` | dataset loaders |
| `src/Engine/python_chunking.py` | AST-based Python chunker |
| `src/Engine/md_text_chunking.py` | Markdown/text chunker |
| `src/Engine/tokenizer.py` | tokenizer and vocabulary |
| `src/Engine/retrieval.py` | BM25 |
| `src/Engine/recall.py` | IoU and recall@k |
 
## Chunking strategy
 
Chunk size is set by `--max_chunk_size` (default 2000 characters). No chunk is
ever longer than that, because the moulinette rejects any longer source.
 
**Python files: AST split-then-merge.**
1. Parse the file with `ast`. Use the AST only to find node boundaries; the
   chunk text always comes from the original source, so the character offsets
   stay exact.
2. A node that fits is kept whole. A function/class/`if`/`try` that is too big
   is split recursively: its header line (and decorators) becomes its own
   piece, then its `body`, `orelse`, `handlers` and `finalbody` are split in
   source order.
3. Neighbouring small pieces are merged while the real span in the source
   (gaps and comments included) stays below the limit.
4. A single leaf that is still too long falls back to fixed-size splitting.
**Markdown and text files.** Split on structural separators (`---` blocks for
`.md`, blank lines for `.txt`). A section that fits becomes a chunk; a longer
one is split into fixed windows with a 15% overlap.
 
**Effect of chunk size.** Too small: the answer is cut across chunks, the
context loses its surroundings, and the index gets larger and slower. Too
large: one chunk mixes many topics, so BM25 scores get diluted, and the
overlap with a small reference range (IoU >= 0.05) can fail. The 2000
character default is also the hard cap of the moulinette.
 
## Retrieval method
 
**BM25, written by hand.**
 
```
score(q, d) = sum over query terms t of
    IDF(t) * tf(t, d) * (k1 + 1) / (tf(t, d) + k1 * (1 - b + b * |d| / avgdl))
IDF(t) = ln(1 + (N - n_t + 0.5) / (n_t + 0.5))
```
 
- A "document" is one chunk (not one file), so the hit is a precise range.
- Parameters: `k1 = 0.5`, `b = 0.75`.
- The query is tokenized with the same function as the chunks, and duplicate
  query tokens are removed so a repeated word is not counted twice.
- Chunks are ranked by score and the top `k` are returned.
**BM25 vs TF-IDF.** TF-IDF grows linearly with term frequency and ignores
document length. BM25 saturates the term frequency (`k1`) and normalizes by
chunk length (`b`), so a long chunk that repeats a word does not beat a short,
focused one.
 
**Tokenizer (what the index keeps).** Questions paraphrase ideas or quote
identifiers, so both forms must match:
- `camelCase` is split before lowercasing, and `snake_case` splits on `_`
  (`trust_remote_code` gives `trust`, `remote`, `code`).
- Punctuation tokens, stopwords and one-letter tokens are dropped.
- Simple suffix stems are added for longer words.
## Performance analysis
 
Recall@k on the public datasets, measured with the moulinette
(`--k 10 --max_context_length 2000`):
 
| Dataset | Recall@1 | Recall@3 | Recall@5 | Recall@10 | Required @5 |
|---|---|---|---|---|---|
| Docs (100 q) | 0.58 | 0.79 | **0.83** | 0.86 | 0.80 |
| Code (99 q) | 0.364 | 0.535 | **0.606** | 0.677 | 0.50 |
 
Measured on a 42 campus machine:
- Indexing the whole corpus: about 1 minute (limit: 5 minutes).
- Searching 99 questions with the saved index: about 5 seconds, including
  loading the index (limit: 90 seconds for 200 questions).
- Answer generation: about 10 to 16 seconds per question on CPU. On a slower
  home CPU in bfloat16 it was 48 to 63 seconds per question; loading the model
  in float32 brought it to about 24 seconds, because that CPU has no fast
  bfloat16.
Retrieval history (docs recall@5 / code recall@5): the first version found the
right file for only about 2 of 5 test questions. The tokenizer work
(camelCase splitting, stopword and punctuation filtering, a suffix-loop fix)
and the exact chunk offsets brought it to the numbers above.
 
Effect of chunk size: the reported numbers use the default 2000. <!-- Add
your own results for smaller sizes here, e.g. 1000 and 1500, as the subject
asks. -->
 
## Answer generation
 
- Model: `Qwen/Qwen3-0.6B` (default and only model), run locally on CPU.
- Prompt built with the model's chat template; thinking mode disabled
  (`enable_thinking=False`); greedy decoding; at most 120 new tokens.
- The context is the text of the retrieved ranges, labelled
  `[Source i: path]`, capped at 4000 characters so it stays inside the token
  budget and keeps CPU time reasonable.
- The system prompt tells the model to use only the context and to reply with
  a fixed refusal sentence otherwise. A small grounding check then compares the
  answer's words with the context; if fewer than half appear, the answer is
  replaced by the refusal. This catches answers the 0.6B model invents from its
  own knowledge (for example "The capital of France is Paris").
## Design decisions
 
- **BM25 only, no embeddings.** The subject requires one lexical method;
  identifiers in code are matched well by lexical search, and the index builds
  in about a minute on CPU.
- **Own BM25 and tokenizer.** No retrieval library, so every choice (stemming,
  camelCase, parameters) can be explained and tuned.
- **AST for structure, source for text.** Keeps character offsets exact, which
  is what the recall metric compares.
- **Persisted index (pickle).** `search` loads it instead of re-chunking, which
  is what makes the 90-second throughput limit easy to meet.
- **Search and answer as separate commands** that exchange a JSON file, as the
  subject defines.
- **Grounding check plus refusal.** A BM25 score threshold could not tell junk
  queries from real ones (the scores overlap), so refusal relies on the prompt
  and the post-generation check.
- **float32 on CPU.** Slightly more RAM, but much faster than emulated
  bfloat16 on CPUs without native support.
- **CPU-only torch** (`pyproject.toml`), to avoid several GB of CUDA wheels.
## Challenges faced
 
- **Offsets that did not match the text.** Merged chunks were built by joining
  node texts, so the text and the `first/last_character_index` disagreed.
  Fix: build every chunk from the source slice. Also fixed decorators, headers
  of split functions, `else/except/finally` blocks and an off-by-one in the
  fixed-size splitter.
- **Questions vs code vocabulary.** Identifiers like `trust_remote_code` or
  `BatchedExperts` rarely look like the question. Fix: tokenizer changes.
- **A dataset label that did not point at the answer** (the reference range was
  in a different part of the file). Always check a label before tuning
  retrieval for it.
- **Slow BM25.** Recomputing statistics per query was too slow. Fix: compute
  chunk statistics once, and persist the index.
- **Small hallucination-prone model.** Handled with the strict prompt and the
  grounding check.
- **Disk space and memory.** A small home quota broke the model download, and
  an editor language server once used 16 GB of RAM and made generation 5 times
  slower. Fix: cache directory next to the project (symlinkable), CPU-only
  torch, and closing the editor during long runs.

 
## Resources


### 1. Understanding RAG

- **Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP
  Tasks"** (https://arxiv.org/pdf/2005.11401): the original paper. It
  introduced the idea of combining a model's own knowledge with an external
  source.
- **IBM, "What is retrieval-augmented generation"**
  (https://www.ibm.com/think/topics/retrieval-augmented-generation) and
  **Fraunhofer IESE, RAG blog**
  (https://www.iese.fraunhofer.de/blog/retrieval-augmented-generation-rag/):
  simple explanations of the four stages (indexing, retrieving, augmenting,
  generating) and why RAG is cheaper than retraining a model.
- **Parametric vs non-parametric memory**
  (https://lawrence-emenike.medium.com/a-straightforward-explanation-of-parametric-vs-non-parametric-memory-in-llms-f0b00ac64167):
  knowledge stored in the weights compared with knowledge fetched at answer
  time. This explains why the model is allowed to answer only from the context.
- **IBM, "RAG vs fine-tuning"**
  (https://www.ibm.com/think/topics/rag-vs-fine-tuning) and **"Fine-tuning
  RAG"** (https://arxiv.org/pdf/2505.10792): when to retrieve and when to
  retrain.
- **Learn RAG From Scratch, LangChain tutorial**
  (https://www.youtube.com/watch?v=sVcwVQRHIc8) and the
  **rag-from-scratch repository**
  (https://github.com/langchain-ai/rag-from-scratch): a full walk-through of
  the pipeline that I used as a mental model.
- **RAG series by j13mehul**
  (https://medium.com/@j13mehul/rag-part-1-from-naive-to-advanced-cb40674a7738,
  part 4 on indexing): a clear explanation of naive vs advanced RAG and of how
  an index is organised for fast access.
- **Springer, "Retrieval-Augmented Generation (RAG)"**
  (https://link.springer.com/article/10.1007/s12599-025-00945-3) and
  **Red Hat, "What is vLLM"**
  (https://www.redhat.com/en/topics/ai/what-is-vllm): background on the
  article-level concepts and on the codebase I was indexing.

### 2. Chunking

- **Jillani Soft Tech, "Optimizing chunking strategies for RAG with Python"**
  (https://jillanisofttech.medium.com/optimizing-chunking-strategies-for-retrieval-augmented-generation-rag-applications-with-python-c3ab5060d3e4):
  my starting point for comparing fixed-size, recursive and structure-aware
  chunking.
- **Weaviate, "Chunking strategies for RAG"**
  (https://weaviate.io/blog/chunking-strategies-for-rag) and **Databricks,
  "The ultimate guide to chunking strategies"**
  (https://community.databricks.com/t5/technical-blog/the-ultimate-guide-to-chunking-strategies-for-rag-applications/ba-p/113089):
  the trade-offs between chunk size and overlap, and why different file types
  need different strategies.
- **"What is chunk size and chunk overlap"**
  (https://dev.to/tak089/what-is-chunk-size-and-chunk-overlap-1hlj): the
  reason I used a 15% overlap in the fixed-size splitter.
- **LangChain, RecursiveCharacterTextSplitter**
  (https://docs.langchain.com/oss/python/integrations/splitters/recursive_text_splitter,
  https://dev.to/eteimz/understanding-langchains-recursivecharactertextsplitter-2846)
  and **"Recursive chunking in RAG"**
  (https://oneuptime.com/blog/post/2026-01-30-rag-recursive-chunking/view):
  the idea of a hierarchy of separators and "split, then merge". I chose not
  to depend on LangChain and implemented the idea myself.
- **Supermemory, "Building code-chunk: AST-aware code chunking"**
  (https://supermemory.ai/blog/building-code-chunk-ast-aware-code-chunking/):
  the main inspiration for the Python chunker, which splits along the syntax
  tree instead of cutting through functions.
- **GeeksforGeeks, "Splitting and merging chunks"**
  (https://www.geeksforgeeks.org/nlp/nlp-splitting-and-merging-chunks/): the
  merge step that joins small neighbouring pieces up to the size limit.
- **Python `ast` documentation**
  (https://docs.python.org/3/library/ast.html), **Green Tree Snakes**
  (https://greentreesnakes.readthedocs.io/), **Earthly, "Python AST"**
  (https://earthly.dev/blog/python-ast/), and the introductions by
  pybit.es, DeepSource and Real Python: how node types and attributes work
  (`lineno`, `col_offset`, `body`, `orelse`, `decorator_list`). This was the
  hardest part to get right, because attribute types differ between nodes.
- **Markdown chunkers** (https://github.com/ghostfix-pm/rag-chunker,
  https://pypi.org/project/markdown-chunker/) and **Microsoft MarkItDown**
  (https://github.com/microsoft/markitdown): I studied structure-aware
  Markdown chunking. I implemented the simpler separator-based version.

### 3. Tokenization and retrieval

- **Introduction to Information Retrieval** (Manning, Raghavan, Schutze,
  https://nlp.stanford.edu/IR-book/pdf/irbookonlinereading.pdf): the
  theory behind term frequency, inverse document frequency and ranking.
- **GeeksforGeeks, "What is BM25"**
  (https://www.geeksforgeeks.org/nlp/what-is-bm25-best-matching-25-algorithm/),
  **kmwllc, "Understanding TF-IDF and BM25"**
  (https://kmwllc.com/index.php/2020/03/20/understanding-tf-idf-and-bm-25/):
  how BM25 improves on TF-IDF with term-frequency saturation (`k1`) and
  length normalisation (`b`). I implemented the formula myself.
- **bm25s** (https://github.com/xhluca/bm25s) and the `BM25` package: read to
  understand existing implementations, not used in the project.
- **Hugging Face, "Tokenizer summary"**
  (https://huggingface.co/transformers/v3.5.1/tokenizer_summary.html),
  **"Transformers 101: tokens, attention and beyond"**
  (https://medium.com/@mayanksultania/transformers-101-tokens-attention-and-beyond-b080a900ca6c),
  and the **OpenAI tiktoken cookbook**
  (https://developers.openai.com/cookbook/examples/how_to_count_tokens_with_tiktoken):
  what tokens and a vocabulary are. I first tried a BERT tokenizer and later
  wrote my own.
- **OpenAI GPT-2 `encoder.py`**
  (https://github.com/openai/gpt-2/blob/master/src/encoder.py) and
  **Python Tutorial, "regex split"**
  (https://www.pythontutorial.net/python-regex/python-regex-split/): the
  regex pattern and structure for splitting text into words and sub-words.
- **Python `collections.Counter`**
  (https://www.geeksforgeeks.org/python/counters-in-python-set-1/): used for
  term frequencies and document frequencies. Precomputing these once per chunk
  removed my slow first BM25 version.
- **Understanding precision, recall and F-score at k**
  (https://krishnapullak.medium.com/understanding-precision-recall-and-f-score-at-k-in-recommender-systems-7146a0dce68e):
  how recall@k is defined, which I later reproduced in the `evaluate` command
  with the IoU >= 0.05 rule from the subject.
- **Hybrid retrieval video**
  (https://www.youtube.com/watch?v=r0Dciuq0knU) and **"Improving RAG"**
  (https://www.youtube.com/watch?v=smGbeghV1JE): read as future improvements
  (combining lexical and semantic rankings), not implemented.

### 4. Generation with Qwen

- **Qwen3-0.6B model card and Qwen quickstart**
  (https://qwen.readthedocs.io/en/latest/getting_started/quickstart.html):
  loading the model, the chat template and `enable_thinking`.
- **Hugging Face Transformers docs** (chat templating, text generation): why
  an instruct model needs its template, and how greedy decoding and
  `max_new_tokens` work.
- **Sentence Transformers** (https://www.sbert.net/) and **NLTK**
  (https://www.nltk.org/): explored for embeddings and text processing, not
  used in the final project.

### 5. Python tooling and implementation

- **Python Fire guide**
  (https://github.com/google/python-fire/blob/master/docs/guide.md): turning
  a class into a command-line interface.
- **Pydantic JSON validation**
  (https://pydantic.dev/docs/validation/dev/concepts/json/) and
  **PyNative, "Python JSON validation"**
  (https://pynative.com/python-json-validation/): validating the search
  results file with `model_validate_json`.
- **Reading JSON and handling errors**
  (https://www.geeksforgeeks.org/python/read-json-file-using-python/).
- **`os.walk`** (https://www.geeksforgeeks.org/python/os-walk-python/,
  https://www.tutorialspoint.com/python/os_walk.htm, and a Stack Overflow
  answer on getting paths): walking the vLLM tree (about 2,874 files of many
  types) and keeping only `.py`, `.md` and `.txt`. Paths are relative to the
  working directory.
- **`os.makedirs`** (https://www.w3schools.com/python/ref_os_makedirs.asp)
  and **tqdm** (https://tqdm.github.io/): output folders and progress bars.
- **TOML** (https://toml.io/en/) and **uv docs, "Using uv with PyTorch"**
  (https://docs.astral.sh/uv/guides/integration/pytorch/): the
  `pyproject.toml` and the CPU-only torch index.
- **MIT 15.773, "Hands-on deep learning"**
  (https://ocw.mit.edu/courses/15-773-hands-on-deep-learning-spring-2024/pages/syllabus/):
  background on how language models work.

### How AI was used

I wrote the code by hand first, then debugged it and made sure it worked. I
started using AI (Claude) after about half of the important work was done, for further
improvements and efficiency. Important AI usage areas:

* Choosing the best chunking strategy for Python files (AST split-then-merge)
  and finding bugs in the recursive splitter, after debugging them myself first.
* Diagnosing retrieval quality: tokenizer improvements, BM25 review, and
  checking dataset labels against the files.
* Learning Fire and structuring the CLI.
* Persisting the index, the Qwen prompt and grounding check, the `evaluate`
  command, performance debugging (float32, memory, disk space), the Makefile
  and `pyproject.toml`.
* Writing and structuring this README.