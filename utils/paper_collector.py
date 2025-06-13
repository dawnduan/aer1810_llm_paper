# download_pdf_from

import requests
import os
from paperswithcode import PapersWithCodeClient
import pandas as pd
from pathlib import Path

def download_pdf_from(url, destination_folder):
  # Send a GET request to the URL to download the PDF
  response = requests.get(url)
  # Check if the request was successful
  if response.status_code == 200:
      # Construct the destination path by joining the destination folder and the filename from the URL
      destination_path = os.path.join(destination_folder, url.split("/")[-1])
      print()
      # Open the destination file for writing in binary mode
      with open(destination_path, "wb") as output_file:
          # Write the downloaded PDF content to the destination file
          output_file.write(response.content)

      print(f"PDF downloaded to: {destination_path}")
  else:
      print(f"Error downloading PDF. Status code: {response.status_code}")

def download_pdf(arxiv_id, save_path):
    """
    Download a PDF from arXiv given the arXiv ID and save to the specified path.
    """
    url = f'https://arxiv.org/pdf/{arxiv_id}.pdf'
    response = requests.get(url)
    save_path = Path(save_path) 
    if not os.path.isdir(save_path):
        print(f"Creating directory: {save_path}")
        os.makedirs(save_path)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded PDF to {save_path}")
    else:
        print(f"Failed to download PDF. Status code: {response.status_code}")

# def _get_imagenet_paper():
#     #!pip install paperswithcode-client
#     from paperswithcode import PapersWithCodeClient
#     client = PapersWithCodeClient()

#     imagenet_id = client.dataset_get('imagenet').id
#     print(imagenet_id)
#     # client.paper_dataset_list(imagenet_id)
#     task_id = "image-classification"
#     client.task_get(task_id)
#     # client.paper_dataset_list('')
#     imagenet_id

#     for idx, paper in enumerate(papers.results):

#         if idx>50:
#             break
#         if any(dataset.name.lower()==imagenet_id for dataset in client.paper_dataset_list(paper.id).results):
#             print('Found paper with imagenet')
#             # save and download
#             url = paper.url_pdf
#             print(paper.id, paper.published)

def imagenet_paper_collector(num_papers=1000, destination_folder = "../exp_1000_papers"):
    client = PapersWithCodeClient()
    imagenet_id = client.dataset_get('imagenet').id
    task_id = "image-classification"
    # client.task_get(task_id)
    papers = client.task_paper_list("image-classification")

    # check if the paper is already in the dev labels
    dev_labvels = set(pd.read_csv("/data/dev_labels/dev_labels.csv")["arxiv_name"])
    is_paper_in_dev_labels = lambda paper: paper.arxiv_id in dev_labvels
    cnts = 0
    for idx, paper in enumerate(papers.results):

        if cnts>num_papers:
            break
        if is_paper_in_dev_labels(paper):
            continue
        if any(dataset.name.lower()==imagenet_id for dataset in client.paper_dataset_list(paper.id).results):
            cnts += 1
            print('Found paper with imagenet')
            # save and download
            download_pdf_from(paper.url_pdf, destination_folder)
    
    import pandas as pd
    desired_arxiv_ids = [paper.arxiv_id for paper in papers.results if is_paper_in_dev_labels(paper)]

def main():
    print(os.getcwd())
    destination_folder = '/Users/dawn.duan/Library/CloudStorage/OneDrive-CanadianTire/Documents/hr_related/School/PhD_Direct/uoft/MIE/MIE_Guerzhoy/aer1810_llm_paper/data/exp_1000_papers'
    # destination_folder = Path("/Users/dawn.duan/Library/CloudStorage/OneDrive-CanadianTire/Documents/hr_related/School/PhD_Direct/uoft/MIE/MIE_Guerzhoy/aer1810/exp_1000_papers")
    print(destination_folder)
    ## test downloading

    # Example usage
    arxiv_id = '1512.03385v1'  # Replace with your arXiv ID
    folder_path = "/Users/dawn.duan/Library/CloudStorage/OneDrive-CanadianTire/Documents/tetris/ivado_or/tetris-api-worker/optimization/local_experiments/aer1810/10_benchmark_datasets"
    fn = "1512.03385v1.pdf"
    pdf_path = Path(folder_path)/fn 
    # Download the PDF
    download_pdf(arxiv_id, destination_folder)
    # imagenet_paper_collector(num_papers=3, destination_folder=destination_folder)


if __name__ == "__main__":
    main()
