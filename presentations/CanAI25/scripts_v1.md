> **Hi everyone—thanks for joining.** Welcome to our recent work on LLM-assisted extraction work. 
> Our project asks a simple question: *Can a large-language model read computer-vision papers and pull out the numbers we care about?*


### 1  Motivation
Imagine you are a new CV student preparing a submission.
To show progress you need yesterday’s state-of-the-art—Top-1 accuracy from ImageNet . Those values are scattered across tables, main contents, and sometimes only in figures. Collecting them by hand is slow and error-prone.


 First thing is to figure out SOTA performances from the literatures. Particularly Image Classification on ImageNet datasets has been a popular leaderboard since the start of the AlexNet around 2011. Putting together the leaderboard involves lots of manual efforts to extract, verify and consolidate from literatures and these hasn’t been non-trivial efforts. 

This ties back nicely to our work. Our work focus on the extraction of Top-1 Accuracy reported on ImageNet for Image classification tasks. 

We present EXTRACT-AND-VERIFY, an end-to-end large language model (LLM)
pipeline that automatically extracts performance metrics from scientific papers.
We collect a large dataset of publications that report Top-1 Accuracy on the
ImageNet dataset and manually annotate it.

We report that our system correctly extracts
the Top-1 accuracy in 67% on the development set, outperforming prior work.

Trends of literature has influenced our work.
SCILEAD, accpted in Nov 24 EMNLP, contributes a manual curated scientific leaderboard datsets (around 40 papers). They method is LLM –based method that automatically construct scientific leaderboard.

We are also influenced by recent trends of prompting techiqnues. Famour few shot manner, self-critique and self-refine are the major ones.

Without further do, lets jump into our work. The construction of our development set is through – an automated
crawling pipeline that fetched candidate PDF. Then we manual annotation protocol based on the chosen performance metrics Top-1 Accuracy. Please note that
There are lots of dataset-subset alignment and situations requriers further efforts. Here we leave as a preshadowing to our qualitative analysis in the last piece of our presentation.


We will walk through our EXTRACT_AND_VERIFY method in a flow-chart manner and present a glance of our prompt template.

-Lets’s dive into our system. The input to our system is a set of paper and the output to it is simply a number, the extracted Top-1 accuracy.

-We Leverages a loop: the model first extracts potential accuracy metrics and cites the source sentence for various chunk/slice of PDF, then re‐examines its own outputs to confirm consistency or highlight omissions.

-This verification step forces the LLM to reflect on potential errors—especially when multiple snippet extractions conflict. Its simple but robust in practice.

We present the main extraction prompt here. Similar to what we see previously, here the prompt template highlight a few more source sentence and accuracy tuples in a few shot manner. As we see a fair datasets consists entries with omissions and top-1 accuracies.

The exciting part is coming – how well we did?
We evaluate our proposed EXTRACT-AND-VERIFY system against SCILEAD on our 100-paper
development set. Two types of evaluation are conducted: (i) classification accuracy—assessing
whether the predicted Top-1 value exactly matches the annotated ground-truth, and (ii) regression-
based metrics—quantifying how close the extracted values are numerically.

So how extractly the predicted Top-1 value matches with Groundtruth? This brings us back to NLP101 where accuracy precision recall F1 scores are used given an extraction vs groundtruth.

Our EXTRACT-AND-VERIFY pipeline correctly extracts the Top-1 accuracy in 67 out of 100 papers,
compared to 63 by SCILEAD. However, our method yields higher recall and F1 score, reflecting
better overall coverage and extraction consistency. These classification-based findings align with
our regression analysis discussed below.

Now we are interested in  quantifying how close the extracted values are numerically. (finding out how further our extracted values apart from the GT.

Our system shows a lower MAE and RMSE (Mean Absolute Error (MAE) and Root Mean Squared Error (RMSE).
 compared to SCILEAD, indicating tighter
alignment with the annotated ground-truth values. The high Pearson correlation (r = 0.971) also
suggests that our method better preserves the relative ranking of performance metrics across papers,
whereas SCILEAD shows weak and even negative correlation.

We are done with numbers for now.
We illustrate our results with a qualitative analysis of easy and difficult cases.