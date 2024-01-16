# ensembl_variants_lookup/utils/gene_helpers.py
import requests

def get_gene_coordinates(gene_name):
    server = "https://rest.ensembl.org/lookup/symbol/human/"
    full_url = f"{server}{gene_name}?expand=1"
    result = requests.get(full_url, headers={"Content-Type": "application/json"})
    result.raise_for_status()
    gene_data = result.json()

    coordinates = {
        'chrom': gene_data['seq_region_name'],
        'start': gene_data['start'],
        'end': gene_data['end']
    }

    return coordinates

def get_variants_in_region(chrom, start, end, output_file=None):
    region = f"{chrom}:{start}-{end}"
    server = "https://rest.ensembl.org/overlap/region/human/"
    extension = "?feature=variation"
    full_url = f"{server}{region}{extension}"
    
    result = requests.get(full_url, headers={"Content-Type": "application/json"})
    result.raise_for_status()
    variant_data = result.json()

    if output_file:
        with open(output_file, 'w') as file:
            json.dump(variant_data, file)

    return variant_data   
