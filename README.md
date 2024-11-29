# National Park Explorer Web Application

The National Parks Explorer Application is a web-based platform designed to help users explore various national parks across the United States. It provides information about different parks, including their locations, activities, amenities, alerts, and more. Users can search for parks by name or state, view park details, discover trails, add parks to favorites, explore park maps, and plan their itineraries based on available activities.

## Features
- **List of Parks:** Browse through a comprehensive list of national parks in the United States.
- **Search Functionality:** Search for parks by name or state to quickly find specific parks of interest.
- **Park Details:** Access detailed information about each park, including activities, entrance fees, operating hours, weather information, and images.
- **Trail Recommendations:** Discover recommended trails within specific parks for hiking and exploration.
- **Favorites:** Add parks to favorites for easy access to frequently visited or preferred destinations.
- **Interactive Maps:** View park boundaries and explore the geographical layout of parks.
- **Itinerary Planning:** Plan your park visits by exploring available activities and attractions within each park.

## National Park Service API Integration
The National Parks Explorer Application utilizes the National Park Service (NPS) API to fetch information about various national parks across the United States. By leveraging the NPS API, the application provides users with up-to-date details about park locations, activities, amenities, alerts, and more.

To use this application, you need an API key from the National Park Service. Visit [NPS Developer Get Started](https://www.nps.gov/subjects/developer/get-started.htm) to obtain your API key and include it in the application configuration.

## Microservice Integration
The application seamlessly integrates with a microservice developed by a project partner for fetching trail information and recommendations. This microservice, although not included in this repository, complements the functionality of the National Parks Explorer Application by providing additional trail-related data for enhanced user experience.

## Recreating the Microservice
To recreate the microservice:

1. **Set Up a Message Queue:** Use RabbitMQ to facilitate communication between the components. Create a queue to handle messages with park address data.
2. **Develop the Sender:** Build a sender program to format and send park addresses as JSON messages to the message queue.
3. Develop the Receiver: Implement a receiver program to:
    - Retrieve park addresses from the queue.
    - Use a geocoding API to obtain the latitude and longitude of the park.
    - Query a trails API to fetch trails near the park's location.
    - Process and display the fetched trail data.
4. Run the Microservice: Start the sender and receiver components to handle park addresses and fetch relevant trail information.

This microservice uses APIs such as TrueWay Geocoding and TrailAPI. API keys are required to access these services.

## Local Development Environment
The National Parks Explorer Application is designed to run locally on your computer, allowing for easy setup and testing.

### How to Start the Application
1. Clone the repository to your local machine.
2. Obtain an API key from the National Park Service and update the application configuration file with your key.
3. Install the necessary dependencies using your preferred package manager.
4. Run the application locally with the command:  ```python3 NPproject.py```