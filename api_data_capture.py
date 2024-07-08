from flask import Flask, jsonify, request
import datetime

# Create a Flask application
app = Flask(__name__)

# Arbitrary list of names
names = ["Alice", "Bob", "Charlie", "David", "Eve"]

# Function to log metadata to a file
def log_metadata():
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ip_address = request.remote_addr
    user_agent = request.user_agent.string
    endpoint = request.path
    http_method = request.method
    query_parameters = dict(request.args)
    headers = dict(request.headers)
    
    log_entry = f'{timestamp} - IP: {ip_address}, User-Agent: {user_agent}, Endpoint: {endpoint}, Method: {http_method}, Query Params: {query_parameters}, Headers: {headers}\n'
    
    with open('request_logs.txt', 'a') as file:
        file.write(log_entry)

# Define a route to return the list of names
@app.route('/names', methods=['GET'])
def get_names():
    # Log metadata
    log_metadata()
    return jsonify(names)

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
