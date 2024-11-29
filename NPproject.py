import requests
import time
import random
from flask import Flask, render_template, request

# Importing partner microservice
# Uncomment and update to your own configuration to use the application's  trail recommendations feature
# from partnerMicro import sending, receiving 

# Initialize flask application
app = Flask(__name__)

# Global variables for making calls to the National Park Service API
API_KEY = "YOUR_API_KEY"  # Replace with your actual NPS API key
API_BASE_URL = "https://developer.nps.gov/api/v1"

# Global array to store favorited parks
favorites = []


# Function to fetch all national parks using NPS API
def get_all_parks():
    parks = []  # Initialize empty list to store parks
    limit = 400  # Set limit for pagnation
    start = 0  # Starting index for pagination
    while True:
        # Make API call to fetch parks
        response = requests.get(f"{API_BASE_URL}/parks?api_key={API_KEY}&designation=National Park"
                                f"&limit={limit}&start={start}")
        if response.status_code != 200:
            print("Error fetching parks:", response.text) # Error handling if the API call fails
            break

        parks_data = response.json()["data"] # Parse response JSON to get park data
        # Filter to ensure we only have National Parks in the list
        national_parks = [park for park in parks_data if park["designation"] == "National Park"]
        parks.extend(national_parks) # Add filtered parks to the list
        if len(parks_data) < limit:
            break  # Exit loop once all results have been fetched
        start += limit # Move to the next set of results

    return parks # Return the list of national parks


# Function to search parks by name or state
def search_parks(search_term):
    try:
        # Make API call to search for parks using the search term
        response = requests.get(f"{API_BASE_URL}/parks?api_key={API_KEY}&q={search_term}"
                                f"&designation=National Park&sort=-relevanceScore")
        if response.status_code == 200:
            parks_data = response.json()["data"] # Parse response to get parks
            national_parks = [park for park in parks_data if park["designation"] == "National Park"]
            return national_parks
        else:
            print("Error fetching parks:", response.text)
            return [] # Return empty list if no parks found
    except requests.RequestException as e:
        print("Error:", e) # Handle request exceptions
        return []


# Function to get extended parks details using NPS API parks endpoint
def fetch_park_details(park_name):
    try:
        # Make API call to fetch detailed information about a specific park
        response = requests.get(f"{API_BASE_URL}/parks?api_key={API_KEY}&q={park_name}&designation=National Park"
                                f"&sort=-relevanceScore&fields=activities,entranceFees,entrancePasses,operatingHours,"
                                f"weatherInfo,images")  # Additional fields added to request
        if response.status_code == 200:
            parks_data = response.json()["data"]
            national_parks = [park for park in parks_data if park["designation"] == "National Park"]
            return national_parks
        else:
            print("Error fetching parks:", response.text)
            return [] # Return empty list if no parks found
    except requests.RequestException as e:
        print("Error:", e) # Handle request exceptions
        return []


# Function to get park amenities using the NPS API amenities endpoint
def fetch_park_amenities(park_name):
    try:
        # Make API call to fetch park amenities
        response = requests.get(f"{API_BASE_URL}/amenities?api_key={API_KEY}&q={park_name}")
        if response.status_code == 200:
            amenities_data = response.json()["data"] # Parse response for amenities dat
            return amenities_data
        else:
            print("Error fetching amenities:", response.text)
            return [] # Return empty list if no amenities found
    except requests.RequestException as e:
        print("Error:", e) # Handle request exceptions
        return []


# Pick a random image from the set of images for a park
def get_random_image(park_details_info):
    if 'images' in park_details_info[0]: # Check if images are available
        images = park_details_info[0]['images']
        random_image = random.choice(images) # Choose a random image from the list
    else:
        random_image = None # Return None if no images found
    return random_image


# Pick a random park to then pick a random image from to use on the home page
def get_random_image_for_home(park_data):
    if 'data' in park_data: # Ensure the data field exists
        parks = park_data['data']
        random_park = random.choice(parks) # Select a random park from the list
        if 'images' in random_park: # Ensure images exist for the park
            images = random_park['images']
            random_image = random.choice(images) # Choose a random image
            return random_park, random_image # Return park and selected imag
    return None, None # Return None if no valid park or image


# Call partner's microservice to get trail information for a park
# Uncomment and update to your own configuration to use the application's  trail recommendations feature
#def get_trails(park_name):
#    # Send request to microservice
#    sending.get_park(park_name)
#    # Wait for microservice to execute
#    time.sleep(3)
#    # Receive the microservice response
#    trails_data = receiving.get_trails_data(park_name)
#    return trails_data


# Function to get park boundary locations using the NPS API mapdata/parkboundaries endpoint
def fetch_park_boundaries(site_code):
    try:
        # Make API call to fetch park boundary data
        response = requests.get(f"{API_BASE_URL}/mapdata/parkboundaries/{site_code}?api_key={API_KEY}")
        if response.status_code == 200:
            return response.json() # Return boundary data as JSON
        else:
            return None # Return None if no data found
    except requests.RequestException as e:
        print("Error:", e) # Handle request exceptions
        return []


# Function to get current park alerts using the NPS API alerts endpoint
def fetch_park_alerts(park_name):
    try:
        # Make API call to fetch alerts for a park
        response = requests.get(f"{API_BASE_URL}/alerts?api_key={API_KEY}&q={park_name}")
        if response.status_code == 200:
            alerts_data = response.json()["data"] # Parse the alerts data
            return alerts_data
        else:
            print("Error fetching alerts:", response.text)
            return [] # Return empty list if no alerts found
    except requests.RequestException as e:
        print("Error:", e) # Handle request exceptions
        return []


# Function to get list of activities and places at a park using NPS API thingstodo endpoint
def fetch_things_to_do(park_code):
    # Make API call to fetch activities for a park
    response = requests.get(f'{API_BASE_URL}/thingstodo?api_key={API_KEY}&parkCode={park_code}')
    if response.status_code == 200:
        return response.json() # Return the activities data
    else:
        return None # Return None if no activities found


# Extract and parse together needed data into array from thingstodo API response
def parse_activities_data(activities_data):
    activities = [] # Initialize an empty list for activities
    for activity in activities_data['data']:
        # Parse relevant fields and add to the activities list
        activities.append({
            'title': activity['title'],
            'shortDescription': activity['shortDescription'],
            'url': activity['url'],
            'durationDescription': activity['durationDescription'],
            'locationDescription': activity['locationDescription'],
            'activityDescription': activity['activityDescription'],
            'petsDescription': activity['petsDescription']
        })
    return activities # Return the list of parsed activities


# Application home page
@app.route('/')
def index():
    # Make a request to the parks endpoint with the images field
    response = requests.get(f'{API_BASE_URL}/parks?api_key={API_KEY}&designation=National Park&fields=images')
    if response.status_code == 200:
        parks_data = response.json() # Parse response to get park data
        # Get a random image from a random park
        random_park, random_image = get_random_image_for_home(parks_data)
        if random_park is not None and random_image is not None:
            return render_template('index.html', random_park=random_park, random_image=random_image)
        else:
            return 'Error: No parks or images found'
    else:
        return 'Error fetching park data'


# List of parks application page
@app.route('/list_parks')
def list_parks():
    parks = get_all_parks() # Fetch all parks
    return render_template('list_parks.html', parks=parks) # Render the list of parks


# Search parks application page
@app.route('/search_parks', methods=['GET', 'POST'])
def search_parks_route():
    if request.method == 'POST':
        search_term = request.form['search_term'] # Get the search term from the form
        parks = search_parks(search_term) # Search for parks using the term
        if parks:
            return render_template('search_parks.html', parks=parks) # Display the search results
        else:
            return render_template('search_parks.html', message="No parks found matching the search criteria.")
    else:
        return render_template('search_parks.html')


# Park details application page
@app.route('/park_details', methods=['GET', 'POST'])
# Handle case with park name parameter passed in
@app.route('/park_details/<park_name>', methods=['GET', 'POST'])
def park_details(park_name=None):
    parks_data = get_all_parks()
    park_names = [park['fullName'] for park in parks_data]
    fetched_park_details = None
    random_image = None
    amenities_data = None
    alerts_data = None

    # Get park name input from user selection
    if request.method == 'POST':
        park_name = request.form['park_name']

    if park_name:
        fetched_park_details = fetch_park_details(park_name) # Fetch detailed information
        random_image = get_random_image(fetched_park_details) # Pick random park image to display
        amenities_data = fetch_park_amenities(park_name)
        alerts_data = fetch_park_alerts(park_name)

    return render_template('park_details.html', park_names=park_names, park_details=fetched_park_details,
                           park_name=park_name, random_image=random_image, amenities=amenities_data, alerts=alerts_data)


# Trail recommendations application page
# Doesn't work if microservice is not implemented
@app.route('/trail_recommendations', methods=['GET', 'POST'])
def trail_recommendations():
    parks_data = get_all_parks()
    park_names = [park['fullName'] for park in parks_data]
    if request.method == 'POST':
        park_name = request.form['park_name']
        # Uncomment if you implement the microservice
        # trails_data = get_trails(park_name)
        return render_template('trail_recommendations.html', park_names=park_names, trails=trails_data,
                               park_name=park_name)
    else:
        return render_template('trail_recommendations.html', park_names=park_names)


# Park added to favorites application page
@app.route('/add_favorite', methods=['POST'])
def add_favorite():
    park_name = request.form['park_name']
    favorites.append(park_name) # Add park to favorites array
    return render_template('add_favorite.html', park_name=park_name) # Display favorites list


# Favorite parks application page
@app.route('/favorites')
def favorites_page():
    return render_template('favorites.html', favorites=favorites) # Display favorites list


# Park map application page
@app.route('/view_map', methods=['POST'])
def view_map():
    park_name = request.form['park_name']
    site_code = request.form['site_code']
    park_boundaries_data = fetch_park_boundaries(site_code) # Get boundary coordinates for map
    if park_boundaries_data:
        # Display interactive map
        return render_template('view_map.html', park_name=park_name, park_boundaries=park_boundaries_data)
    else:
        return 'Error fetching park boundaries data'


# Things to do application page
@app.route('/itinerary', methods=['GET', 'POST'])
def itinerary():
    parks_data = get_all_parks()
    # Extract park names with corresponding park codes
    park_names = [(park['fullName'], park['parkCode']) for park in parks_data]

    if request.method == 'POST':
        park_code = request.form['park_code']
        park_name = request.form['park_name']
        activities_data = fetch_things_to_do(park_code) # Get activities data using selected park code
        if activities_data:
            activities = parse_activities_data(activities_data)
            # Display activities
            return render_template('itinerary.html', park_names=park_names, activities=activities, park_name=park_name)
        else:
            return 'Error fetching activities data'
    else:
        return render_template('itinerary.html', park_names=park_names)


# Main entry point for the application
if __name__ == '__main__':
    app.run(debug=True)
