**KDD Author responses**


---

###  Dataset bias and difficulty distribution
The sources papers were **randomly sampled from the first 100 Paper‑with‑Code API hits *after shuffling***; we could
1. add this random‑seed line and publish the shuffle list for transparency. 
2. using heuristic sorting like publish year

> R2C1: Dev set is retrieved through the order of API results and is not fully clear if it introduces any bias. There is no analysis on the distribution of difficulty levels in the input dataset.

---

###  Multiple proposed models in one paper
Our current work select the **maximum Top‑1 accuracy** among models that the paper itself calls “ours,” to match common leaderboard practice. We will:
* clarify the writing in §3.2 Label-Verification Protocol

"fig 8 does not corresponds to anything valid."

> R2C3 Also it is not clear for papers with multiple proposed methods which final metrics need to be selected. E.g. fig 8 it mentions should flag for ambiguity.

---

### Failure analysis (why 67, not 100)
We will


> R2C5 No analysis on the final accuracy 67 / why it is unable to retrieve scores from other papers?
---

###  Regression metrics justification
While we agree that exact match is ultimately required, near‑miss values reveal whether the model “looked in the right place.” We will add more clarifications on the necessisty of the regression metrics as it provides a quantitive measurement how further apart the extracted values from the groundtruth values.

> R2C6 Also regression metrics do not really make sense given we want the LLM to extract the correct value and not credit for picking some nearby value which is usually in a similar range as a lot of metric tables have similar values.
---

###  Writing and placement issues
We will fix §3.3 and §4 paragraph order, remove redundant phrases.
> R2C4 Weak paper writing: In Section 3.3, starting sentences need to be modified/removed. In section 4, the first paragraph seems to be misplaced or needs to occur after paragraph 2.


---

### Test set/Dev set split
We will firstlty have exsisting 100 dev set and test it on additional 100 sets. Working towards 1000 labelled paper.

> R1C3: Both the evaluation and some post-processing steps depend on manual annotation and rule-based heuristics which limits scalability and generalizability to other domains or metrics
Extraction pipeline’s performance failing on one-third of cases(just 67) underscores the limitations of current LLM-based approaches for fully automated scientific metric extraction, especially in the face of real-world reporting diversity.

> R2C2: Proposed pipeline measures the accuracy on dev set which is already known to have the top1 accuracy; however for a full end-to-end setup the pipeline needs to also have a component to identify if the paper actually has the score or not and then extract it. The precision is 1 for this set which is not a real-world setup.

---
Unaddressable

> R1C1: "The paper’s “iterative self-verification” approach is little more than repeated prompting and majority voting, which, while conceptually reasonable, does not fundamentally address the underlying limitations of LLMs in reasoning about document structure or resolving ambiguity."

> R1C2: While the methodology and error analysis are explained in detail, the technical novelty is limited, as the core approach relies on prompt engineering, iterative self-verification, and majority voting, which are incremental extensions of existing LLM prompting techniques rather than fundamentally new algorithms

--- 





