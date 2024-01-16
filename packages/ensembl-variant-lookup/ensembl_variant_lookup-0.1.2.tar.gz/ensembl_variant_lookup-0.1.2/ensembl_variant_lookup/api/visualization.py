# ensembl_variants_lookup/api/visualization.py
from flask import render_template, request
from utils.gene_helpers import get_gene_coordinates, get_variants_in_region
from api.variant_lookup import visualize_variants

def visualize_gene_variants():
    if request.method == 'POST':
        gene_name = request.form['gene_name']
        coordinates = get_gene_coordinates(gene_name)

        variant_data = get_variants_in_region(coordinates['chrom'], coordinates['start'], coordinates['end'])
        visualize_variants(variant_data, gene_name)

        return "Visualization completed"
    else:
        return render_template('visualization.html')

