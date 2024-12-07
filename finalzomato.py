import pandas as pd 
import numpy as np
import plotly.express as px
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image 

df = pd.read_csv('merged_data.csv')

#-------------------------------------------------------streamlit part--------------------------------------------------------------------------------
#menu bar 
st.set_page_config(layout="wide")
img = Image.open("download.png")
st.image(img, use_column_width=True)                
selected = option_menu(
    menu_title = None,
    options = ["OVERVIEW", "PROJECT", "ABOUT"],
    icons = ["book", "database-fill-check", "blockquote-right"],
    default_index = 0,
    orientation=  "horizontal")


if selected == 'OVERVIEW':
    st.write('''# Zomato Data Analysis and Visualization

## Table of Contents

- [Overview](#overview)
- [Project Objectives](#project-objectives)
- [Dataset](#dataset)
- [Key Features](#key-features)
- [Installation](#installation)
- [Usage](#usage)
- [Results](#results)
- [Project Evaluation Metrics](#project-evaluation-metrics)
- [Contributing](#contributing)
- [License](#license)

## Overview

This project focuses on analyzing and visualizing data from Zomato, a popular restaurant discovery and food delivery service. Through data exploration and visualization techniques, this project aims to provide insights into customer preferences, popular cuisines, and trends in the restaurant industry. The findings will be beneficial for stakeholders, including restaurants, food industry players, and investors.

## Project Objectives

- Perform data exploration and cleaning to prepare the dataset for analysis.
- Visualize various aspects of Zomato's data to identify trends and patterns.
- Create an interactive dashboard using Streamlit for data analysis and visualization.

## Dataset

- Zomato Dataset: [Zomato Data CSV](https://raw.githubusercontent.com/nethajinirmal13/Training-datasets/main/zomato/zomato.csv)
- Country Codes: [Country Code Excel](https://github.com/nethajinirmal13/Training-datasets/blob/main/zomato/Country-Code.xlsx)

## Key Features

1. **Data Engineering**:
   - Added a column for prices in Indian Rupees (INR).
   - Compared Indian currency with other currencies.

2. **Dashboard Development**:
   - Dropdown filter to choose country-specific data.
   - Two charts visualizing metrics such as total sales and popular cuisines.
   - Insights on costliest cuisines in India.
   - City filtering for analyzing:
     - Most popular and expensive cuisines.
     - Rating count based on ratings.
     - Online delivery vs. dine-in options in pie chart format.
   - Comparison between cities in India regarding online delivery, dine-in spending, and living costs.

3. **Dashboard Deployment**:
   - Hosted and deployed the dashboard on a web application server for public access.


''')
    


if selected == 'PROJECT':
    selected = option_menu(
        menu_title = None,
        options = ["OVERALL", "COUNTRY-VIA", 'CITIES_VIA', 'INDIA'],
        icons = None,
        default_index = 0,
        orientation=  "horizontal")

    if selected ==  "OVERALL":
        col1, col2 = st.columns(2)
        with col1:
            # Average Price Comparison in INR by Currency
            average_prices = df.groupby('Currency')['Price_in_INR'].mean().reset_index()
            fig = px.bar(average_prices, x='Currency', y='Price_in_INR', title='Average Price Comparison in INR by Currency')
            st.plotly_chart(fig)

            # Total Number of Restaurants by Country
            restaurant_count = df['Country'].value_counts().reset_index()
            restaurant_count.columns = ['Country', 'Total Restaurants']
            # Chart: Total Number of Restaurants by Country
            fig1 = px.bar(restaurant_count, x='Country', y='Total Restaurants', title='Total Number of Restaurants by Country')
            # Display the first chart
            st.plotly_chart(fig1)

            # Group by cuisine and calculate average price
            average_price_by_cuisine = df.groupby('Cuisines')['Average Cost for two'].mean().reset_index()
            # Chart: Average Price for Two People by Cuisine
            fig2 = px.bar(average_price_by_cuisine, x='Cuisines', y='Average Cost for two', title='Average Price for Two by Cuisine')
            # Display the second chart
            st.plotly_chart(fig2)


        with col2:
            st.table(average_prices)
            st.table(restaurant_count)
            st.write(average_price_by_cuisine)



    if selected == "COUNTRY-VIA":
        # Create a dropdown to select a country
        countries = df['Country'].unique()  # Get unique country names
        selected_country = st.selectbox("Select a Country:", countries)

        # Filter the DataFrame based on the selected country
        filtered_data = df[df['Country'] == selected_country]

        col1, col2 = st.columns(2)
        with col1:
            restaurant_count = filtered_data['Country'].value_counts().reset_index()
            restaurant_count.columns = ['Country', 'Total Restaurants']
            # Chart: Total Number of Restaurants by Country
            fig1 = px.bar(restaurant_count, x='Country', y='Total Restaurants', title='Total Number of Restaurants by Country')
            # Display the first chart
            st.plotly_chart(fig1)

            # Group by cuisine and calculate average price
            average_price_by_cuisine = filtered_data.groupby('Cuisines')['Average Cost for two'].mean().reset_index()
            # Chart: Average Price for Two People by Cuisine
            fig2 = px.bar(average_price_by_cuisine, x='Cuisines', y='Average Cost for two', title='Average Price for Two by Cuisine')
            # Display the second chart
            st.plotly_chart(fig2)           
            

        with col2:
            st.write(restaurant_count)
            st.write(average_price_by_cuisine)


    if selected == 'CITIES_VIA':
        countries = df['Country'].unique()
        selected_country = st.selectbox("Select a Country:", countries)

        # Filter the dataset based on the selected country
        country_data = df[df['Country'] == selected_country]

        # Create a dropdown for selecting a city based on the selected country
        cities = country_data['City'].unique()
        selected_city = st.selectbox("Select a City:", cities)

        # Filter data for the selected city
        city_data = country_data[country_data['City'] == selected_city]

        # Most popular cuisine in the city
        popular_cuisine = city_data['Cuisines'].mode()[0]

        # Most expensive cuisine in the city
        average_price_by_cuisine = city_data.groupby('Cuisines')['Average Cost for two'].mean().reset_index()
        most_expensive_cuisine = average_price_by_cuisine.sort_values(by='Average Cost for two', ascending=False).head(1)

        # Rating count in the city
        rating_counts = city_data['Rating text'].value_counts()

        # Pie chart data for online delivery vs. dine-in
        delivery_counts = city_data['Has Online delivery'].value_counts()
        delivery_labels = ['Dine-in', 'Online Delivery']
        delivery_data = [delivery_counts.get(True, 0), delivery_counts.get(False, 0)]

        # Display results
        st.write(f"## Most Popular Cuisine in {selected_city}, {selected_country}:** {popular_cuisine}")
        st.write(f"## Most Expensive Cuisine in {selected_city}, {selected_country}:** {most_expensive_cuisine['Cuisines'].values[0]} with an average cost of {most_expensive_cuisine['Average Cost for two'].values[0]} INR")

        # Display rating counts in the city
        st.write("**Rating Counts in the City:**")
        st.bar_chart(rating_counts)

        delivery_labels = ['Dine-in', 'Online Delivery']
        delivery_data = [delivery_counts.get(True, 0), delivery_counts.get(False, 0)]

        # Check if Dine-in is available or not
        if delivery_data[0] == 0:  # No dine-in available
            st.write(f"## No, Dine-in is available in {selected_city}, {selected_country}")
        else:    
            # Create a pie chart only if dine-in is available
            fig = px.pie(names=delivery_labels, values=delivery_data, title=f"Online Delivery vs Dine-in Options in {selected_city}, {selected_country}")
            st.plotly_chart(fig)

    if selected == 'INDIA':
        # Filter Indian data (assuming 'Country' column has country names and 'India' is one of them)
        india_data = df[df['Country'] == 'India']
        col1, col2 = st.columns(2)
        with col1:
            average_price_by_cuisine = india_data.groupby('Cuisines')['Average Cost for two'].mean().reset_index()
            # Sort the cuisines by average price in descending order
            average_price_by_cuisine = average_price_by_cuisine.sort_values(by='Average Cost for two', ascending=False)
            fig = px.bar(average_price_by_cuisine.head(10), 
                x='Cuisines', 
                y='Average Cost for two', 
                title='Top 10 Most Expensive Cuisines in India',
                labels={'Average Cost for two': 'Average Cost for Two (INR)', 'Cuisines': 'Cuisines'})
            # Display the chart
            st.plotly_chart(fig)
        with col2:
            st.write(average_price_by_cuisine.head(10))    

        # Online Delivery vs. Dine-in Comparison by City
        online_delivery_by_city = india_data.groupby('City')['Has Online delivery'].value_counts(normalize=True).unstack().fillna(0)

        # Rename columns for clarity
        online_delivery_by_city.columns = ['Dine-in', 'Online Delivery']

        # Plot the online delivery vs dine-in comparison by city
        st.write("## Comparison of Online Delivery vs. Dine-in in Different Cities of India")
        fig = px.bar(online_delivery_by_city, barmode='group', title="Online Delivery vs. Dine-in by City in India")
        st.plotly_chart(fig)

        # Calculate Average Living Cost (Average Cost for two) by City
        living_cost_by_city = india_data.groupby('City')['Average Cost for two'].mean().reset_index()

        # Plot Living Costs by City
        st.write("## Comparison of Living Costs Across Cities in India")
        fig = px.bar(living_cost_by_city, x='City', y='Average Cost for two', title="Average Cost for Two in Different Cities of India (Living Costs)")
        st.plotly_chart(fig)

        # Identify top cities for online delivery and dine-in
        st.write("## Top Cities in India for Online Delivery and Dine-in")

        # Top cities for online delivery
        top_online_delivery_cities = online_delivery_by_city.sort_values(by='Online Delivery', ascending=False).head(5)
        st.write("Top Cities for Online Delivery:")
        st.table(top_online_delivery_cities[['Online Delivery']])

        # Top cities for dine-in
        top_dine_in_cities = online_delivery_by_city.sort_values(by='Dine-in', ascending=False).head(5)
        st.write("Top Cities for Dine-in:")
        st.table(top_dine_in_cities[['Dine-in']])    

if selected == 'ABOUT':
        col1, col2 = st.columns(2)  
        col2.image(Image.open(r'C:\Users\JANANI BHAARATHI\OneDrive\Desktop\ZOMATO\JANANI BHAARATHI K M.jpeg'), width=600)
        with col1:
            st.markdown("## Done by : JANANI BHAARATHI K M ") 
            st.markdown(" An Aspiring DATA-SCIENTIST..!")
            st.markdown("Gmail: jananibharathi2001@gmail.com")
            st.markdown("[Githublink](https://github.com/Janani2001Bhaarathi/)")
            st.markdown("[LinkedIn](https://www.linkedin.com/in/janani-bhaarathi-k-m-25988a22a/)") 
        st.write("---") 
