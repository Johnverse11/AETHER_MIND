from flask import Flask, render_template, request, jsonify, session
import requests
from gen_ai import gemini_response

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Replace with a secure key for session management

# Adzuna API credentials
ADZUNA_API_ID = "87267910"  # Application ID
ADZUNA_API_KEY = "467e6bf6cdf7d353ed9a79f9ec63fd6a"  # Application Key
ADZUNA_API_URL = "https://api.adzuna.com/v1/api/jobs"

# edX API credentials (assumed structure, replace with actual API details)
EDX_API_URL = "https://api.edx.org/catalog/v1/courses"

# Function to call Adzuna API
def fetch_job_listings(job_title, location="India"):
    endpoint = f"{ADZUNA_API_URL}/in/search/1"  # Endpoint for India
    params = {
        "app_id": ADZUNA_API_ID,
        "app_key": ADZUNA_API_KEY,
        "what": job_title,
        "where": location,
    }
    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        return response.json()  # Return the JSON response
    else:
        return {"error": f"Failed to fetch jobs: {response.text}"}

# Function to call edX API for course listings
def fetch_course_listings(course_title):
    params = {
        "search": course_title,
        "page_size": 5  # Adjust the number of results as needed
    }
    response = requests.get(EDX_API_URL, params=params)
    
    # Debugging: Print the response for inspection
    print("edX API Response:", response.json())  # Log the entire response
    
    if response.status_code == 200:
        return response.json()  # Return the JSON response
    else:
        return {"error": f"Failed to fetch courses: {response.text}"}

@app.route('/', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        user_input = request.form.get('user_input')
        conversation_type = request.form.get('conversation_type')

        # Retrieve chat history from session, or initialize it if empty
        chat_history = session.get('chat_history', [])

        # Append the current user input to the chat history
        chat_history.append(f"User: {user_input}")

        # Send chat history as part of the input to the Gemini API
        gemini_data = gemini_response("\n".join(chat_history))

        # Prepare a default response and link list
        response = gemini_data.get('response', "Sorry, I couldn't process your request.")
        chat_history.append(f"AI: {response}")
        links = []

        if conversation_type == 'job':
            # Fetch job listings from Adzuna API
            job_data = fetch_job_listings(user_input)
            if "results" in job_data:
                links = [{"url": job['redirect_url'], "text": job['title']} for job in job_data['results']]
            else:
                response += " Unfortunately, I couldn't find any relevant job listings."
        elif conversation_type == 'course':
            course_data = fetch_course_listings(user_input)
            print("Course Data:", course_data)  # Debugging
            if "results" in course_data:
                links = [{"url": course['url'], "text": course['title']} for course in course_data['results']]
            else:
                response += " Unfortunately, I couldn't find any relevant courses."
        elif conversation_type == 'internship':
            # Fetch internship listings from Adzuna API (assuming similar to jobs)
            internship_data = fetch_job_listings(f"{user_input} internship")  # Adjust query as needed
            if "results" in internship_data:
                links = [{"url": job['redirect_url'], "text": job['title']} for job in internship_data['results']]
            else:
                response += " Unfortunately, I couldn't find any relevant internships."

        # Store the updated chat history back in the session
        session['chat_history'] = chat_history

        return jsonify({
            "response": response,
            "links": links,
            "chat_history": chat_history  # Optionally return history for debugging or UI display
        })

    # Clear chat history when rendering the page (optional, or provide a button to clear)
    session['chat_history'] = []

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
