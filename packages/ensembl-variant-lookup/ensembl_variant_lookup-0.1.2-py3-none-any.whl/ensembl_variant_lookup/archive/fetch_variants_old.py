from flask import Flask, render_template, request, jsonify
import requests
import json
import os
import pandas as pd
import plotly.express as px
from rpy2.robjects import pandas2ri

app = Flask(__name__, template_folder=os.path.abspath('templates'), static_url_path='/static')

def get_variants_by_rsid(rsid):
    # Set the url/endpoint provided by Ensembl database
    server = "https://rest.ensembl.org/variation/human/"
    
    # Add the rsid for the SNP of interest
    extension = f"{rsid}?"
    
    # Add the extension/rsid to complete the endpoint
    full_url = server + extension

    # Provide Content Type
    result = requests.get(full_url, headers={"Content-Type": "application/json"})
    
    # Check the request http status
    result.raise_for_status()

    return result.json()



def get_variants_by_rsid_list(variant_ids):
    server = "https://rest.ensembl.org"
    endpoint = "/variation/human"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    payload = {"ids": variant_ids}

    try:
        response = requests.post(server + endpoint, headers=headers, json=payload)
        response.raise_for_status()
        decoded = response.json()
        
        # Create a DataFrame from the decoded JSON response
        df = pd.DataFrame(decoded)
        
        # Print the DataFrame
        print(df)

        return df
    except requests.exceptions.RequestException as e:
        print(f"Error fetching variant data: {e}")
        return None



# Updated Flask route
@app.route('/batch', methods=['POST'])
def batch_search():
    variant_data = None
    error_message = None

    if request.method == 'POST':
        rsid_list = request.form.get('rsid_list')

        if rsid_list:
            # Split the input string into a list of rsids
            rsid_list = [rsid.strip() for rsid in rsid_list.split(',')]

            try:
                # Obtain the results of the SNP using the new function
                variant_data_df = get_variants_by_rsid_list(rsid_list)
                variant_data = variant_data_df.to_dict(orient='dict')
            except requests.exceptions.RequestException as e:
                # Return error in case of a bad request or any other issue
                error_message = f"Error fetching data: {str(e)}"

    return render_template('batch_results.html', variant_data=variant_data, error_message=error_message)
    
    

@app.route('/variant', methods=['GET', 'POST'])
def variant_search():
    variant_data = None

    if request.method == 'POST':
        rsid = request.form['rsid']
        try:
            # Obtain the results of the SNP using function get_variants_by_rsid
            variant_data = get_variants_by_rsid(rsid)
        except requests.exceptions.RequestException as e:
            # Return error in case of a bad request or any other issue
            error_message = f"Error fetching data: {str(e)}"
            return render_template('variant_results.html', error_message=error_message)

    elif request.method == 'GET':
        rsid = request.args.get('id')
        try:
            # Obtain the results of the SNP using function get_variants_by_rsid
            variant_data = get_variants_by_rsid(rsid)
        except requests.exceptions.RequestException as e:
            # Return error in case of a bad request or any other issue
            error_message = f"Error fetching data: {str(e)}"
            return render_template('variant_results.html', error_message=error_message)

    return render_template('variant_results.html', variant_data=variant_data)

    
# Use HTTP requests
@app.route('/', methods=['GET', 'POST'])
def index():
    variant_data = None
    gene_data = None
    error_message = None

    if request.method == 'POST':
        if variant_data != None: 
            rsid = request.form['rsid']
            try:
                # Obtain the results of the SNP using function get_variants_by_rsid
                variant_data = get_variants_by_rsid(rsid)
            except requests.exceptions.RequestException as e:
            
                # Return error in case of bad request or any other issue
                error_message = f"Error fetching data: {str(e)}"
                return render_template('index.html', error_message=error_message)
        elif gene_data!= None:
            gene_name = request.form['gene_name']
            try:
                gene_coordinates = get_gene_coordinates(gene_name)
                print(gene_coordinates)
                variants_data = get_variants_in_region(gene_coordinates['chrom'], gene_coordinates['start'],
                                                       gene_coordinates['end'])
                print(variants_data)
    
                return render_template('gene_results.html', gene_name=gene_name, gene_coordinates=gene_coordinates,
                                       variants_data=variants_data)
    
            except requests.exceptions.RequestException as e:
                error_message = f"Error fetching data: {str(e)}"

    return render_template('index.html', gene_data=gene_data, variant_data=variant_data, error_message=error_message)
       
       
    
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


@app.route('/gene_region', methods=['GET'])
def gene_region_search():
    variant_data = None
    error_message = None

    if request.method == 'GET':
        chrom = request.args.get('chrom')
        start = request.args.get('start')
        end = request.args.get('end')

        try:
            # Obtain the results of the gene region search using the new function
            variant_data = get_variants_in_region(chrom, start, end)
        except requests.exceptions.RequestException as e:
            # Return error in case of a bad request or any other issue
            error_message = f"Error fetching data: {str(e)}"

    return render_template('gene_region_results.html', variant_data=variant_data, error_message=error_message)

# R visualization function
def visualize_variants(variant_data, gene_name):
    # Convert variant_data list to a DataFrame
    column_names = ['id', 'consequence_type']
    plot_data = pd.DataFrame(variant_data, columns=column_names)

    # Count the occurrences of each variant consequence
    variant_counts = plot_data['consequence_type'].value_counts()

    # Convert to data frame for plotting
    plot_df = pd.DataFrame({'consequence': variant_counts.index, 'count': variant_counts.values})

    # Create a bar plot using plotly
    fig = px.bar(plot_df, x='count', y='consequence', orientation='h',
                 title=f"Genetic Variants in {gene_name}",
                 labels={'count': 'Count', 'consequence': 'Variant Consequence'},
                 height=400)

    # Remove legend
    fig.update_layout(showlegend=False)

    # Show the plot
    fig.show()

# New Flask routes
@app.route('/gene_info', methods=['GET'])
def gene_info():
    try:
        # Get the gene_name from the query parameters
        gene_name = request.args.get('gene_name')

        if gene_name:
            # Call the function to get gene coordinates
            gene_coordinates = get_gene_coordinates(gene_name)

            # Return the gene coordinates as JSON
            return jsonify(gene_coordinates)
        else:
            # If gene_name is not provided in the query parameters
            return jsonify({"error": "Gene name not provided"}), 400
    except Exception as e:
        # Handle exceptions, log the error, and return an error response
        return jsonify({"error": str(e)}), 500

@app.route('/variants_in_region/<chrom>/<start>/<end>', methods=['GET'])
def variants_in_region(chrom, start, end):
    variant_data = get_variants_in_region(chrom, start, end)
    return jsonify(variant_data)

@app.route('/visualize', methods=['GET', 'POST'])
def visualize_gene_variants():
    if request.method == 'POST':
        gene_name = request.form['gene_name']
        coordinates = get_gene_coordinates(gene_name)
        print(coordinates)
        variant_data = get_variants_in_region(coordinates['chrom'], coordinates['start'], coordinates['end'])
        visualize_variants(variant_data, gene_name)
        return "Visualization completed"
    else:
        # Handle GET requests for visualization page
        return render_template('visualization.html')

    

if __name__ == '__main__':
    # Run the app with your host ip and port
    app.run(host='0.0.0.0', port=5000, debug=True)
