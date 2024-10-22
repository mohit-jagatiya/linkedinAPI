from flask import Flask, request, jsonify
from linkedin_api import Linkedin
# from waitress import serve

# Initialize Flask app
app = Flask(__name__)

# Initialize LinkedIn API with your credentials
api = Linkedin("ratheepranjal449@gmail.com","Welcome@2?")
# Create an endpoint to get the company details
@app.route('/get_company_details', methods=['POST'])
def get_company_details() -> tuple:
    """
    Endpoint to get the company information based on the company name provided in the request body.
    
    Request body should contain the following JSON:
    {
        "company_name": str
    }
    
    Returns the company information as a JSON response.
    
    :return: A tuple containing the JSON response and the HTTP status code.
    """
    try:
        # Get the company name from the request body
        data: dict = request.get_json()
        company_name: str = data.get('company_name')

        # If company_name is not provided, return an error
        if not company_name:
            return jsonify({"error": "company_name is required"}), 400

        # Fetch the company information using linkedin-api
        company_info: dict = api.get_company(company_name)
        print(company_info)
        # Return the company information as a JSON response
        return jsonify(company_info), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Create an endpoint to get the profile details
@app.route('/get_profile_details', methods=['POST'])
def get_profile_details() -> tuple:
    """
    Endpoint to get the profile details based on the profile name provided in the request body.
    
    Request body should contain the following JSON:
    {
        "profile_name": str
    }
    
    Returns the profile information as a JSON response.
    
    :return: A tuple containing the JSON response and the HTTP status code.
    """
    try:
        # Get the profile name from the request body
        data: dict = request.get_json()
        profile_name: str = data.get('profile_name')

        # If profile_name is not provided, return an error
        if not profile_name:
            return jsonify({"error": "profile_name is required"}), 400

        # Fetch the profile information using linkedin-api
        profile_info: dict = api.get_profile(profile_name)
        print(profile_info)
        # Return the company information as a JSON response
        return jsonify(profile_info), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Create an endpoint to get ping
@app.route('/ping', methods=['GET'])
def ping(): 
    """Responds with a simple JSON payload to verify that the server is running
    and reachable. The payload includes a single key-value pair, where the key is
    "status" and the value is 1.

    Returns:
        A JSON response with a status of 200 and a payload like {"status": 1}.
    """
    return jsonify({"status":1}), 200

# Create an endpoint to get get_job_by_company_urn
@app.route('/get_job_by_company_urn', methods=['POST'])
def get_job_by_company_urn() -> tuple:
    """
    Endpoint to search for jobs based on the company name provided in the request body.

    Request body should contain the following JSON:
    {
        "company_URN": str,  # Company URN
        "limit": int,  # Number of jobs to return
        "offset": int  # Offset for pagination
    }

    Returns the job search results as a JSON response.

    :return: A tuple containing the JSON response with job search results and the HTTP status code.
    """
    try:
        # Get the request data
        data: dict = request.get_json()

        # Get the company name from the request
        company_name: str = data.get('company_URN').replace('urn:li:fs_normalized_company:', '')

        # If company_name is not provided, return an error
        if not company_name:
            return jsonify({"error": "company_name is required"}), 400

        # Get limit and offset from request, or set default values
        limit: int = data.get('limit', -1)  # Default to -1 if limit is not provided
        offset: int = data.get('offset', 0)  # Default to 0 if offset is not provided

        # Search for jobs using the company name, limit, and offset
        jobs: dict = api.search_jobs(companies=[company_name], limit=limit, offset=offset)

        # Return the filtered job results and job search URL
        return jsonify(jobs), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Create an endpoint to get get_job_details
@app.route('/get_job_details', methods=['POST'])
def get_job_details() -> tuple:
    """
    Endpoint to get the job details based on the job ID provided in the request body.
    
    Request body should contain the following JSON:
    {
        "job_id": str  # Job ID
    }
    
    Returns the job details as a JSON response.
    
    :return: A tuple containing the JSON response with job details and the HTTP status code.
    """
    try:
        # Get the job ID from the request body
        data: dict = request.get_json()
        job_id: str = data.get('job_id').replace('urn:li:fsd_jobPosting:', '')

        # If job_id is not provided, return an error
        if not job_id:
            return jsonify({"error": "job_id is required"}), 400

        # Fetch the job details using linkedin-api
        job_details: dict = api.get_job(job_id)

        # If job details are not found, return a message
        if not job_details:
            return jsonify({"message": "Job not found."}), 404

        # Return the job details as a JSON response
        return jsonify(job_details), 200

    except Exception as e:
        # Handle any exceptions and return an error response
        return jsonify({"error": str(e)}), 500
    
# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
    #app.run(host='31.220.90.49', port=5000, debug=True)
    # serve(app, host='31.220.90.49', port=5000, threads=4)

