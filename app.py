from flask import Flask, request, jsonify
from linkedin_api import Linkedin

# Initialize Flask app
app = Flask(__name__)

# Initialize LinkedIn API with your credentials
api = Linkedin('ratheepranjal449@gmail.com', 'Welcome@2?')

# Create an endpoint to get the company details
@app.route('/get_company', methods=['POST'])
def get_company():
    try:
        # Get the company name from the request body
        data = request.get_json()
        company_name = data.get('company_name')

        # If company_name is not provided, return an error
        if not company_name:
            return jsonify({"error": "company_name is required"}), 400

        # Fetch the company information using linkedin-api
        company_info = api.get_company(company_name)

        # Return the company information as a JSON response
        return jsonify(company_info), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
