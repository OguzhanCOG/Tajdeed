import psycopg2
from flask import Flask, jsonify
from flask_cors import CORS  # Import CORS

app = Flask(__name__)

CORS(app)

def fetch_all_poems():
    try:
        # Reconnect to the database
        conn = psycopg2.connect(
            dbname="taj_deed_2024", 
            user="postgres", 
            password="Tajdeed2024!",
            host="tajdeed-db.cdocq8c0qfhe.us-east-1.rds.amazonaws.com", 
            port="5432", 
            sslmode="require", 
            sslrootcert="path_to_downloaded/rds-combined-ca-bundle.pem"  # Update this path
        )
        
        # Set client encoding to UTF-8 to ensure correct handling of non-ASCII characters
        conn.set_client_encoding('UTF8')

        cur = conn.cursor()

        # SQL query to select all poems
        select_query = "SELECT * FROM poems;"

        # Execute the query
        cur.execute(select_query)

        # Fetch all results
        poems = cur.fetchall()

        # Fetch column names
        columns = [desc[0] for desc in cur.description]

        # Convert the result to a list of dictionaries
        poems_list = []
        for poem in poems:
            poem_dict = dict(zip(columns, poem))  # Create a dictionary using column names as keys
            # print(poem_dict)
            poems_list.append(poem_dict)

        # Close the cursor and connection
        cur.close()
        conn.close()

        return poems_list

    except Exception as e:
        print(f"Error: {e}")
        return []

# Define an endpoint to fetch poems
@app.route('/api/poems', methods=['GET'])
def get_poems():
    poems = fetch_all_poems()
    if poems:
        return jsonify({"message": "Poems fetched successfully", "poems": poems}), 200
    else:
        return jsonify({"message": "Error fetching poems"}), 500

# Run the application on a different port
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Changed the port to 5001
CORS(app)
