# ensembl_variants_lookup/api/gene_info.py
from flask import jsonify, request, render_template
import requests
from utils.gene_helpers import get_variants_in_region

def gene_region_search():
    variant_data = None
    error_message = None

    if request.method == 'GET':
        chrom = request.args.get('chrom')
        start = request.args.get('start')
        end = request.args.get('end')

        try:
            variant_data = get_variants_in_region(chrom, start, end)
        except requests.exceptions.RequestException as e:
            error_message = f"Error fetching data: {str(e)}"

    return render_template('gene_region_results.html', variant_data=variant_data, error_message=error_message)


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