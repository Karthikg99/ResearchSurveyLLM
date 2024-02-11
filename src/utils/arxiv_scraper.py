from datetime import datetime
from tqdm import tqdm
import arxiv


def query_papers(topic, save_folder, start_date=None, end_date=None, max_count=None):
    """
    Given a topic, and optionally start_date, end_Date and max_count, returns the corresponding
    list of papers. 
    arguments:
        topic: string
            The topic for which the papers need to be queried
        save_folder: string
            The path to the folder where th papers need to be downloaded to
        start_date: string
            The start date from which you want to gather papers related to the topic. 
            It is in the format - "yyyymmddhhmmss"
        end_date: string
            The end date from which you want to gather papers related to the topic. 
            It is in the format - "yyyymmddhhmmss"
        max_count:
            The upper limit to the number of papers to retreive
    """
    client = arxiv.Client(num_retries=10, page_size=500)
    search_query = arxiv.Search(query = topic,
                                sort_by = arxiv.SortCriterion.Relevance
                                )
    start_date = datetime.strptime(start_date, "%Y%m%d%H%M%S")
    end_date = datetime.strptime(end_date, "%Y%m%d%H%M%S")
    results = client.results(search_query)
    current_paper_count = 0
    for r in tqdm(results):
        if start_date.timestamp() <= r.published.timestamp() <= end_date.timestamp():
            r.download_pdf(save_folder)
            current_paper_count += 1
            if current_paper_count == max_count:
                break


if __name__ == "__main__":
    start_date = "20220101000000" 
    end_date = "20240131235959"    
    topic = "Denoising Diffusion models"
    save_folder = r"C:\Users\sumuk\OneDrive\Desktop\GitHub\ResearchSurveyLLM\delete"
    max_count = 50
    query_papers(topic, save_folder, start_date, end_date, max_count)