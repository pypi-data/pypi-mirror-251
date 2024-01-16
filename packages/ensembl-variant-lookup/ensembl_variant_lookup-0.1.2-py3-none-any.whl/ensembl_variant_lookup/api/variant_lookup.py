# ensembl_variants_lookup/api/variant_lookup.py
from flask import jsonify, request, render_template
from utils.variant_helpers import get_variants_by_rsid, get_variants_by_rsid_list

def batch_search():
    variant_data = None
    error_message = None

    if request.method == 'POST':
        rsid_list = request.form.get('rsid_list')

        if rsid_list:
            rsid_list = [rsid.strip() for rsid in rsid_list.split(',')]

            try:
                variant_data_df = get_variants_by_rsid_list(rsid_list)
                variant_data = variant_data_df.to_dict(orient='dict')
            except requests.exceptions.RequestException as e:
                error_message = f"Error fetching data: {str(e)}"

    return render_template('batch_results.html', variant_data=variant_data, error_message=error_message)


def variant_search():
    variant_data = None

    if request.method == 'POST':
        rsid = request.form['rsid']
        try:
            variant_data = get_variants_by_rsid(rsid)
        except requests.exceptions.RequestException as e:
            error_message = f"Error fetching data: {str(e)}"
            return render_template('variant_results.html', error_message=error_message)

    elif request.method == 'GET':
        rsid = request.args.get('id')
        try:
            variant_data = get_variants_by_rsid(rsid)
        except requests.exceptions.RequestException as e:
            error_message = f"Error fetching data: {str(e)}"
            return render_template('variant_results.html', error_message=error_message)

    return render_template('variant_results.html', variant_data=variant_data)


def visualize_variants(variant_data, gene_name):
    column_names = ['id', 'consequence_type']
    plot_data = pd.DataFrame(variant_data, columns=column_names)
    variant_counts = plot_data['consequence_type'].value_counts()
    plot_df = pd.DataFrame({'consequence': variant_counts.index, 'count': variant_counts.values})
    fig = px.bar(plot_df, x='count', y='consequence', orientation='h',
                 title=f"Genetic Variants in {gene_name}",
                 labels={'count': 'Count', 'consequence': 'Variant Consequence'},
                 height=400)

    fig.update_layout(showlegend=False)
    fig.show()
