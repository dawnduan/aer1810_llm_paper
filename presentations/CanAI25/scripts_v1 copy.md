Hi everyone welcome to our recent work on LLM-assisted extraction work. 

Before we starts, let’s think about a scenario where a young CV researcher trying to submit work to top journals. First thing is to figure out SOTA performances from the literatures. Particularly Image Classification on ImageNet datasets has been a popular leaderboard since the start of the AlexNet around 2011. Putting together the leaderboard involves lots of manual efforts to extract, verify and consolidate from literatures and these hasn’t been non-trivial efforts. 

This ties back nicely to our work. Our work focus on the extraction of Top-1 Accuracy reported on ImageNet for Image Recognition tasks. 

We present EXTRACT-AND-VERIFY, an end-to-end large language model (LLM)
pipeline that automatically extracts performance metrics from scientific papers.
We collect a large dataset of publications that report Top-1 Accuracy on the
ImageNet dataset and manually annotate it.
The pipeline consists of a prompt-based EXTRACT-AND-VERIFY loop that
filters and verifies extracted metrics. We report that our system correctly extracts
the Top-1 accuracy in 67% on the development set, outperforming prior work.
By releasing our annotated dataset and extraction pipeline, we aim to provide
a reliable benchmark for future work on LLM-assisted accuracy retrieval from
machine learning publications.