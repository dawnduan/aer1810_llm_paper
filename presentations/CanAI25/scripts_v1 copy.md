> **Hi everyone—thanks for joining.** Welcome to our recent work on LLM-assisted extraction work. 
> Our project asks a simple question: *Can a large-language model read computer-vision papers and pull out the numbers we care about?*

---

### 1  Motivation
Imagine you are a new CV student preparing a submission.
To show progress you need yesterday’s state-of-the-art—Top-1 ImageNet accuracy. Those values are scattered across tables, main contents, and sometimes only in figures. Collecting them by hand is slow and error-prone.

Particularly Image Classification on ImageNet datasets has been a popular leaderboard since the start of the AlexNet around 2011.


---

### 2  Problem statement
This ties back nicely to our work. 

We focus on one concrete task:
**extracting the Top-1 accuracy reported for ImageNet classification.**

---

### 3  Our approach: **EXTRACT-AND-VERIFY**

* **Data.** 100 ImageNet papers, each page manually labelled with the correct Top-1 number.
* **Pipeline.**

  1. Table-aware PDF parser
  2. Prompt ensemble that proposes ⟨sentence, value⟩ pairs
  3. *Verify* step that votes across prompts and converts error rates to accuracies

---

### 4  Results

*Exact-match accuracy* on the dev set

| Method                 | Exact match ↑ | MAE ↓       |
| ---------------------- | ------------- | ----------- |
| SCILEAD (baseline)     | 27 %          | 21.3 pp     |
| **EXTRACT-AND-VERIFY** | **67 %**      | **0.64 pp** |

So the system finds the right Top-1 value two times out of three and is **30×** more precise than prior work when it misses.

---

### 5  Contribution

* First publicly released, page-level ImageNet extraction dataset
* End-to-end pipeline that others can reuse or benchmark against

---

### 6  Take-away

Automatic SOTA tracking is now practical for a large slice of CV literature, and the tools and data are available on GitHub for anyone who wants to push the numbers higher.

> **Thank you—happy to take questions.**