from langchain.chat_models import ChatOpenAI
from langchain import LLMChain
from langchain.prompts.chat import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

import time
import pandas as pd
from functools import reduce
from utils.groundtruth_parser import extract_text_from_pdf_as_dict, find_fname
from utils.pdf_helper import is_pdf
from tqdm import tqdm
from pathlib import Path

from dotenv import load_dotenv
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

prompt_self_veri = """
extract the top1 accuracy of ImageNet from the given text and return both the sentence containing the accuracy. 
Answer in a number, eg. 90.2% and the accuracy value in 1 number. 404 if it's not mentioned. Use the examples below as a guide.

Example 1:
Expected Output:
Sentence: "a table showing the Top-1 and Top-5 classification accuracy using a binarized ResNet-18 on Imagenet for various ways of constructing the scaling factor. The method "Case 4: α ⊗β ⊗γ" achieved a Top-1 accuracy of 57.1."
Accuracy: 57.1

Example 2:
Expected Output:
Sentence: "In our experiments, the model reported a top-1 accuracy of 82.1% on Imagenet under the given conditions."
Accuracy: 82.1

Example 3:
Expected Output:
Sentence: "The evaluation results showed a top-1 accuracy of 78.3% on the test data on Imagenet."
Accuracy: 78.3

Example 4:
Expected Output:
Sentence: "Our proposed model achieved a top-1 accuracy of 74.2% when evaluated on the Imagenet dataset."
Accuracy: 74.2

Example 4:
Expected Output:
Sentence: "Our proposed model achieved a top-5 accuracy of 66.2% when evaluated on the Imagenet dataset."
Accuracy: -

Now extract the top1 accuracy of ImageNet from the following texts, {page}

Expected Output:
"""

prompt_vote_accuracy = """Find the accuracy value associated with most common sentences from the list of sentences and accuracies. Only output the accuracy value.

Example 1:
'Sentence: "ImageNet1K Top-1 Accuracy ViT 88.5 89.1 88.6 92.4"\nAccuracy: 92.4', 
'Sentence: "SSv2 Top-1 Accuracy ViViT 65.4 68.6 80.1 85.4 ImageNet1K Top-1 Accuracy ViT 88.5 89.1 88.6 92.4 Sun RGBD Top-1 Accuracy Simple3D-former 57.3 62.4 71.4 74.6"\nAccuracy: 92.4', 
'Sentence: "ImageNet1K Top-1 Accuracy ViT 88.5 89.1 88.6 92.4"\nAccuracy: 92.4', 
'Sentence: "SSv2 Top-1 Accuracy ViViT 65.4 68.6 80.1 85.4 ImageNet1K Top-1 Accuracy ViT 88.5 89.1 88.6 92.4 Sun RGBD Top-1 Accuracy Simple3D-former 57.3 62.4 71.4 74.6"\nAccuracy: 74.6',
Expected Output: 92.4

Example 2:
'Sentence: "SSv2 Top-1 Accuracy ViViT 65.4 68.6 80.1 85.4 ImageNet1K Top-1 Accuracy ViT 88.5 89.1 88.6 92.4 Sun RGBD Top-1 Accuracy Simple3D-former 57.3 62.4 71.4 74.6"\nAccuracy: 74.6',
'Sentence: "ImageNet1K Top-1 Accuracy ViT 88.5 89.1 88.6 82.4"\nAccuracy: 82.4', 
'Sentence: "SSv2 Top-1 Accuracy ViViT 65.4 68.6 80.1 85.4 ImageNet1K Top-1 Accuracy ViT 88.5 89.1 88.6 82.4 Sun RGBD Top-1 Accuracy Simple3D-former 57.3 62.4 71.4 74.6"\nAccuracy: 82.4',
Expected Output: 82.4

Example 3:
'Sentence: "It's not mentioned top-1 accuracy on ImageNet"\nAccuracy: 404',
'Sentence: "-"\nAccuracy: -', 
'Sentence: "It's not mentioned top-1 accuracy on ImageNet"\nAccuracy: 404', 
'Sentence: "-"\nAccuracy: 404', 
Expected Output: -

Example 4:
'Sentence: "It's not mentioned."\nAccuracy: -',
'Sentence: "-"\nAccuracy: -', 
'Sentence: "It's mentioned top-5 accuracy on ImageNet"\nAccuracy: -', 
'Sentence: "Cocoa 23.3 21.2"\nAccuracy: 23.3', 
Expected Output: -

Now extract the accuracy value associated with most common sentences, {sentences_and_accuracies}

Expected Output:
"""

prompt_vote_accuracy = """Find the accuracy value associated with most common sentences from the list of sentences and accuracies. Only output the accuracy value.

Example 1:
'Sentence: "ImageNet1K Top-1 Accuracy ViT 88.5 89.1 88.6 92.4"\nAccuracy: 92.4', 
'Sentence: "SSv2 Top-1 Accuracy ViViT 65.4 68.6 80.1 85.4 ImageNet1K Top-1 Accuracy ViT 88.5 89.1 88.6 92.4 Sun RGBD Top-1 Accuracy Simple3D-former 57.3 62.4 71.4 74.6"\nAccuracy: 92.4', 
'Sentence: "ImageNet1K Top-1 Accuracy ViT 88.5 89.1 88.6 92.4"\nAccuracy: 92.4', 
'Sentence: "SSv2 Top-1 Accuracy ViViT 65.4 68.6 80.1 85.4 ImageNet1K Top-1 Accuracy ViT 88.5 89.1 88.6 92.4 Sun RGBD Top-1 Accuracy Simple3D-former 57.3 62.4 71.4 74.6"\nAccuracy: 74.6',
Expected Output: 92.4

Example 2:
'Sentence: "SSv2 Top-1 Accuracy ViViT 65.4 68.6 80.1 85.4 ImageNet1K Top-1 Accuracy ViT 88.5 89.1 88.6 92.4 Sun RGBD Top-1 Accuracy Simple3D-former 57.3 62.4 71.4 74.6"\nAccuracy: 74.6',
'Sentence: "ImageNet1K Top-1 Accuracy ViT 88.5 89.1 88.6 82.4"\nAccuracy: 82.4', 
'Sentence: "SSv2 Top-1 Accuracy ViViT 65.4 68.6 80.1 85.4 ImageNet1K Top-1 Accuracy ViT 88.5 89.1 88.6 82.4 Sun RGBD Top-1 Accuracy Simple3D-former 57.3 62.4 71.4 74.6"\nAccuracy: 82.4',
Expected Output: 82.4

Example 3:
'Sentence: "It's not mentioned top-1 accuracy on ImageNet"\nAccuracy: 404',
'Sentence: "-"\nAccuracy: -', 
'Sentence: "It's not mentioned top-1 accuracy on ImageNet"\nAccuracy: 404', 
'Sentence: "-"\nAccuracy: 404', 
Expected Output: -

Example 4:
'Sentence: "It's not mentioned."\nAccuracy: -',
'Sentence: "-"\nAccuracy: -', 
'Sentence: "It's mentioned top-5 accuracy on ImageNet"\nAccuracy: -', 
'Sentence: "Cocoa 23.3 21.2"\nAccuracy: 23.3', 
Expected Output: -

Now extract the accuracy value associated with most common sentences, {sentences_and_accuracies}

Expected Output:
"""


def parse_gpt_with_page_prompt(page_with_res, prompt, openai_api_key=OPENAI_API_KEY):
    prompt2 = ChatPromptTemplate.from_template(prompt)
    output_parser = StrOutputParser()
    model = ChatOpenAI(model="gpt-4o", openai_api_key=openai_api_key, temperature=0.0, )

    chain = prompt2 | model | output_parser
    try:
        prompt_value = chain.invoke(
            {'page': page_with_res}
        )
    except Exception as e:
        prompt_value = str(e)
    return prompt_value


def delayed_parse_gpt_with_page_prompt(delays_in_sec, **kwargs):
    time.sleep(delays_in_sec)
    return parse_gpt_with_page_prompt(**kwargs)


def parse_gpt_with_vote(sentences_and_accuracies, prompt, openai_api_key = OPENAI_API_KEY):
    model = ChatOpenAI(model="gpt-4o", openai_api_key=openai_api_key, temperature=0.0, max_tokens=5)

    chain = ChatPromptTemplate.from_template(prompt) | model | StrOutputParser()
    try:
        prompt_value = chain.invoke(
            {'sentences_and_accuracies': sentences_and_accuracies}
        )
    except Exception as e:
        prompt_value = str(e)
    return prompt_value



def chunk_text_keys(keys, stepsize):
    lis = []
    sublis = []
    for k in keys:
        sublis += [k]
        if k % 3 == 0:
            lis.append(sublis)
            sublis = []
    return lis


def _vote_emsemble_across_paper(idx, pdf_path, prompt_self_veri, prompt_vote_accuracy,):
    '''
    Input: 
    Output:
    '''
    # print('expect ', groundtruth_df[['Paper Name','Model','Top-1 Accuracy']].iloc[idx].values)
    text_dict = extract_text_from_pdf_as_dict(pdf_path)
    chunked_texts = chunk_text_keys(text_dict.keys(), stepsize=4)
    avg_section_lenth = sum(len(v) for v in text_dict.values())/len(text_dict)*4
    # Calculate the delay based on your rate limit
    token_limit_per_minute = 10000
    delay = 60.0 / token_limit_per_minute * avg_section_lenth / 3

    # compose sublist: verify prompt
    responses_lis = []
    for _, sublis in enumerate(chunked_texts):
        rel_page = ''.join([texts for pg_num, texts in text_dict.items() if pg_num in sublis])
        print(sublis, len(rel_page) / 4)
        responses = [delayed_parse_gpt_with_page_prompt(delays_in_sec=delay, page_with_res=rel_page, prompt=prompt_self_veri) for i in
                     range(5)]
        responses_lis.append(responses)
        print(responses)

    # assumption is that the vote_ensemble will consistently return NA or Results try voting
    relevant_response = [parse_gpt_with_vote(res, prompt_vote_accuracy, openai_api_key) for res in responses_lis]
    rel_res = [ans for ans in relevant_response if ans != '404']
    final_res = parse_gpt_with_vote(rel_res, prompt_vote_accuracy) if rel_res else '404'
    print('#### EOD #####')
    return final_res


def main():
    # Load the .env file located in the root directory
    load_dotenv()

    # Now you can access your variables
    openai_api_key = os.getenv("OPENAI_API_KEY")
    print(f"Your OpenAI API key is obtained!")
    fn = './data/groundtruth_table.csv'
    groundtruth_df = pd.read_csv(fn)
    template = groundtruth_df.copy()[['file_name', 'Paper Name', 'Model', 'Top-1 Accuracy']]
    folder_path_100 = './data/all_papers_100/'
    sorted_pdf_paths_100 = sorted([path for path in Path(folder_path_100).iterdir() if is_pdf(path)])
    sorted_pdf_key_page_100 = {
            idx: [find_fname(path), path]
            for idx, path in enumerate(sorted_pdf_paths_100)
        }
    df_100 = pd.DataFrame.from_dict(
        sorted_pdf_key_page_100,orient='index',
        columns=['file_name', 'path',]
    )
    reduce(lambda l, r: pd.merge(l, r, on=['file_name'],how='outer'), [template, df_100])


    # main method for vote_emsemble
    res_df_whole_paper = pd.DataFrame(data=[
        [idx, find_fname(pdf_path),
         _vote_emsemble_across_paper(idx, pdf_path, prompt_self_veri, prompt_vote_accuracy,)] \
        for idx, (fname, pdf_path) in tqdm(sorted_pdf_key_page_100.items())], \
                                      columns=['file_idx', 'file_name', 'gpt_vote_ensemble_whole_paper'])

    res_100 = reduce(lambda l, r: pd.merge(l, r, on=['file_name'], how='outer'), [template, res_df_whole_paper])
    dest_fn = './logs/res_100.csv'
    res_100.to_csv(dest_fn, index=False)


if __name__ == "__main__":
    main()