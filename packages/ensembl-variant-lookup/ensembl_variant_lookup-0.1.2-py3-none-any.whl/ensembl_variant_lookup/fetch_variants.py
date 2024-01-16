# ensembl_variants_lookup/fetch_variants.py
from flask import Flask, render_template, request, jsonify
import os
import requests
from api.variant_lookup import batch_search, variant_search, get_variants_by_rsid
from api.gene_info import get_gene_coordinates, get_variants_in_region, gene_region_search
from api.visualization import visualize_gene_variants


app = Flask(__name__, template_folder=os.path.abspath('templates'), static_url_path='/static')

@app.route('/', methods=['GET','POST'])
def index_route():
    variant_data = None
    gene_data = None
    error_message = None

    if request.method == 'POST':
        if variant_data != None:
            rsid = request.form['rsid']
            try:
                variant_data = get_variants_by_rsid(rsid)
            except requests.exceptions.RequestException as e:
                error_message = f"Error fetching data: {str(e)}"
                return render_template('templates/index.html', error_message=error_message)
        elif gene_data != None:
            gene_name = request.form['gene_name']
            try:
                gene_coordinates = get_gene_coordinates(gene_name)
                variants_data = get_variants_in_region(gene_coordinates['chrom'], gene_coordinates['start'],
                                                       gene_coordinates['end'])

                return render_template('gene_results.html', gene_name=gene_name, gene_coordinates=gene_coordinates,
                                       variants_data=variants_data)
            except requests.exceptions.RequestException as e:
                error_message = f"Error fetching data: {str(e)}"

    return render_template('index.html', gene_data=gene_data, variant_data=variant_data, error_message=error_message)
@app.route('/batch', methods=['POST'])
def batch_search_route():
    return batch_search()

@app.route('/variant', methods=['GET', 'POST'])
def variant_search_route():
    return variant_search()

@app.route('/gene_region', methods=['GET'])
def gene_region_search_route():
    return gene_region_search()

@app.route('/visualize', methods=['GET', 'POST'])
def visualize_gene_variants_route():
    return visualize_gene_variants()

# Add other routes as needed

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

