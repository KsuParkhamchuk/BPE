import requests
import dis

import pyarrow as pa
import pyarrow.parquet as pq
from datasets import clean_pubmed


def get_pubmed_ids():
    terms = [
        "workout",
        "sport",
        "resistance training",
        "fitness",
        # Medical specific terms
        "exercise physiology",
        "physical therapy",
        "sports medicine",
        "rehabilitation",
        "muscle hypertrophy",
        "cardiovascular fitness",
        "athletic performance",
        "strength training",
        "metabolic health",
        "exercise prescription",
        "movement disorders",
        "physical rehabilitation",
        # Medical conditions
        "obesity treatment",
        "diabetes exercise",
        "hypertension management",
        "orthopedic rehabilitation",
        "cardiac rehabilitation",
        "pulmonary rehabilitation",
        # Research oriented terms
        "clinical exercise trials",
        "exercise biochemistry",
        "sports nutrition",
        "exercise endocrinology",
        "neuromuscular adaptation",
        "biomechanics",
    ]
    search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    base_params = {
        "db": "pubmed",
        "retmax": 500,
        "retmode": "json",
        "sort": "relevance",
    }

    ids = []

    for term in terms:
        params = base_params.copy()
        params["term"] = term
        response = requests.get(search_url, params=params)
        data = response.json()
        ids.extend(data["esearchresult"]["idlist"])

    return ids


def get_records():
    ids = get_pubmed_ids()
    fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?"
    params = {"db": "pubmed", "id": ids, "rettype": "abstract", "retmode": "text"}

    batch_size = 100
    all_text = ""

    for i in range(0, len(ids), batch_size):
        batch_ids = ids[i : i + batch_size]
        ids_str = ",".join(batch_ids)

        params = {
            "db": "pubmed",
            "id": ids_str,
            "rettype": "abstract",
            "retmode": "text",
        }

        response = requests.get(fetch_url, params=params)
        if response.status_code == 200:
            print(f"Retrieved batch {i//batch_size + 1}/{(len(ids)-1)//batch_size + 1}")
            all_text += response.text
        else:
            print(f"Error retrieving batch {i//batch_size + 1}: {response.status_code}")

    # response = requests.get(fetch_url, params=params)
    cleaned_data = clean_pubmed(all_text)
    table = pa.table({"articles": [cleaned_data]})
    pq.write_table(table, "datasets/pubmed/pubmed_sport.parquet")
