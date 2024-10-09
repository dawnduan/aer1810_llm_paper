### preprocess for groundtruths, relevant result page parsing
import pandas as pd
import fitz  # PyMuPDF

fn = './data/groundtruth_table.csv'
groundtruth_df = pd.read_csv(fn)

from pathlib import Path
folder_path = '/Users/dawn.duan/Library/CloudStorage/OneDrive-CanadianTire/Documents/tetris/ivado_or/tetris-api-worker/optimization/local_experiments/aer1810/10_benchmark_datasets/all_papers/'
is_pdf = lambda pdf_path: str(pdf_path).split('.')[-1] == 'pdf'
sorted_pdf_paths = sorted([path for path in Path(folder_path).iterdir() if is_pdf(path)])


find_fname = lambda pdf_path: str(pdf_path).split('/')[-1]

def extract_text_from_pdf_as_dict(pdf_path):
    """
    Extract text from a PDF at the specified path using PyMuPDF.
    """
    with fitz.open(pdf_path) as doc:
        return {
            i+1:page.get_text() # starting from 1
            for i,page in enumerate(doc)
        }


key_indices = groundtruth_df.page_key.values
accuracies = groundtruth_df['Top-5 Accuracy'].values

# first key is file nm; second is page number for answer
ground_truths = {
    idx: [find_fname(path), key_indices[idx]]
    for idx, path in enumerate(sorted_pdf_paths)
}
ground_truths
pdf_keys = {
    path : key_indices[idx]
    for idx, path in enumerate(sorted_pdf_paths)
}
pdf_page_lengths = {
    idx: [path, key_indices[idx], max(extract_text_from_pdf_as_dict(path))]
    for idx, path in enumerate(sorted_pdf_paths)
}


# pdf_page_lengths
sorted_pdf_key_page = {
    idx: [path, key_indices[idx], extract_text_from_pdf_as_dict(path)[key_indices[idx]] if key_indices[idx]>0 else '']
    for idx, path in enumerate(sorted_pdf_paths)
}

# sorted_pdf_key_page
#
# folder_path_20 = '/Users/dawn.duan/Library/CloudStorage/OneDrive-CanadianTire/Documents/tetris/ivado_or/tetris-api-worker/optimization/local_experiments/aer1810/10_benchmark_datasets/all_papers_20/'
# sorted_pdf_paths_20 = sorted([path for path in Path(folder_path_20).iterdir() if is_pdf(path)])
# sorted_pdf_key_page_20 = {
#         idx: [find_fname(path), path]
#         for idx, path in enumerate(sorted_pdf_paths_20)
#     }
# df_20 = pd.DataFrame.from_dict(
#     sorted_pdf_key_page_20,orient='index',
#     columns=['file_name', 'path',]
# )
# from functools import reduce
# fn = '/Users/dawn.duan/Library/CloudStorage/OneDrive-CanadianTire/Documents/tetris/ivado_or/tetris-api-worker/optimization/local_experiments/aer1810/10_benchmark_datasets/groundtruth_table.csv'
# groundtruth_df = pd.read_csv(fn)
# # groundtruth_df
# template = groundtruth_df.copy()[['file_name', 'Paper Name', 'Model', 'Top-1 Accuracy']]
# reduce(lambda l, r: pd.merge(l, r, on=['file_name'],how='right'), [template, df_20])
#
#
#
#
# folder_path_100 = '/Users/dawn.duan/Library/CloudStorage/OneDrive-CanadianTire/Documents/tetris/ivado_or/tetris-api-worker/optimization/local_experiments/aer1810/10_benchmark_datasets/all_papers_100/'
# sorted_pdf_paths_100 = sorted([path for path in Path(folder_path_100).iterdir() if is_pdf(path)])
# sorted_pdf_key_page_100 = {
#         idx: [find_fname(path), path]
#         for idx, path in enumerate(sorted_pdf_paths_100)
#     }
# df_100 = pd.DataFrame.from_dict(
#     sorted_pdf_key_page_100,orient='index',
#     columns=['file_name', 'path',]
# )
# reduce(lambda l, r: pd.merge(l, r, on=['file_name'],how='outer'), [template, df_100])



