import streamlit as st
import requests
import datetime
import pandas as pd

'''
# TaxiFareModel front
'''

with st.form(key='params_form'):
    col1, col2 = st.columns(2)

    with col1:
        pickup_date = st.date_input("Pickup Date", value=datetime.datetime.now())
        pickup_time = st.time_input("Pickup Time", value=datetime.datetime.now())
        passenger_count = st.number_input("Passenger Count", min_value=1, max_value=8, value=1)

    with col2:
        pickup_longitude = st.number_input("Pickup Longitude", value=-73.985428)
        pickup_latitude = st.number_input("Pickup Latitude", value=40.748817)
        dropoff_longitude = st.number_input("Dropoff Longitude", value=-73.985428)
        dropoff_latitude = st.number_input("Dropoff Latitude", value=40.748817)

    submit_button = st.form_submit_button(label='Predict Fare')


url = 'https://taxifare.lewagon.ai/predict'

if url == 'https://taxifare.lewagon.ai/predict':

    if submit_button:
    # 2. Let's build a dictionary containing the parameters for our API...
    params = {
        "pickup_datetime": f"{pickup_date} {pickup_time}",
        "pickup_longitude": pickup_longitude,
        "pickup_latitude": pickup_latitude,
        "dropoff_longitude": dropoff_longitude,
        "dropoff_latitude": dropoff_latitude,
        "passenger_count": passenger_count
    }

    # 3. Let's call our API using the `requests` package...
    response = requests.get(url, params=params)

    # 4. Let's retrieve the prediction from the **JSON** returned by the API...
    if response.status_code == 200:
        prediction = response.json().get('fare', 0)

        
        st.metric(label="Predicted Fare", value=f"${round(prediction, 2)}")

        # Bonus: Map
        st.markdown("### Route Map 🗺")
        map_data = pd.DataFrame({
            'lat': [pickup_latitude, dropoff_latitude],
            'lon': [pickup_longitude, dropoff_longitude]
        })
        st.map(map_data)
    else:
        st.error("Error: Could not retrieve prediction from API.")
