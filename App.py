#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
from pycaret.regression import load_model, predict_model
from datetime import datetime


# In[ ]:


# Load the trained model from PyCaret
def load_model_pycaret():
    model = load_model('best_model')  # Replace 'best_model' with your model's name
    return model


# In[ ]:


# Load data.csv
def load_data():
    data = pd.read_csv('data.csv')
    return data


# In[ ]:


# Function to make predictions using PyCaret
def predict(model, input_df):
    prediction = predict_model(model, data=input_df)
    return prediction['Label'][0]  # 'Label' contains the predicted values


# In[ ]:


# Main Streamlit app function
def main():
    st.title("HDB Resale Price Prediction App")
    
    # Sidebar for user input
    st.sidebar.header("Input Parameters")
    
    def user_input_features():
        # Ordinal mapping for flat_type
        flat_type_input = st.sidebar.selectbox('Flat Type', ['1 Room', '2 Room', '3 Room', '4 Room', '5 Room', 'Executive', 'Multi-Generation'])
        flat_type_map = {
            '1 Room': 1,
            '2 Room': 2,
            '3 Room': 3,
            '4 Room': 4,
            '5 Room': 5,
            'Executive': 6,
            'Multi-Generation': 7
        }
        flat_type = flat_type_map[flat_type_input]
        
        # Automatically set tranc_yearmonth to the current year and month (YYYYMM)
        current_datetime = datetime.now()
        tranc_yearmonth = current_datetime.strftime("%Y%m")
        
        floor_area_sqft = st.sidebar.number_input('Floor Area (in sqft)', step=1.0, format="%.1f", value=1000.0)
        hdb_age = st.sidebar.number_input('HDB Age (in years)', step=1.0, format="%.1f", value=20.0)
        total_dwelling_units = st.sidebar.number_input('Total Dwelling Units', step=1.0, format="%.1f", value=150.0)
        remaining_lease = st.sidebar.number_input('Remaining Lease (in years)', step=1.0, format="%.1f", value=60.0)
        
        # Adding the amenities score based on user input
        st.sidebar.subheader("Amenities within 1km")
        mall_nearby = st.sidebar.checkbox('Mall')
        hawker_nearby = st.sidebar.checkbox('Hawker')
        mrt_nearby = st.sidebar.checkbox('MRT Station')
        bus_stop_nearby = st.sidebar.checkbox('Bus Stop')

        # Calculate amenities score
        amenities_score = 0
        if mall_nearby:
            amenities_score += 1
        if hawker_nearby:
            amenities_score += 1
        if mrt_nearby:
            amenities_score += 1
        if bus_stop_nearby:
            amenities_score += 1

        region = st.sidebar.selectbox('Region', ['Central', 'North', 'South', 'East', 'West'])
        flat_model = st.sidebar.selectbox('Flat Model', ['Standard', 'Improved', 'New Generation', 'Model A', 'Premium Apartment', 'Terrace', 'Type S1', 'Type S2'])
        
        # Storey Category (Dummified Variable)
        storey_category_input = st.sidebar.selectbox('Storey Category (in ranges)', ['1-5', '6-10', '11-15', '16-20', '21-25', '26-30', '31-35', '36-40', '41-45', '46-50', '>50'])

        # Mapping to dummified variables
        storey_category_map = {
            '1-5': '1_to_5',
            '6-10': '6_to_10',
            '11-15': '11_to_15',
            '16-20': '16_to_20',
            '21-25': '21_to_25',
            '26-30': '26_to_30',
            '31-35': '31_to_35',
            '36-40': '36_to_40',
            '41-45': '41_to_45',
            '46-50': '46_to_50',
            '>50': '>50'
        }
        storey_category = storey_category_map[storey_category_input]

        # Primary School Distance and Vacancy Interaction Term (pri_dist_vac)
        st.sidebar.subheader("Primary School Proximity and Vacancy")
        primary_school_distance = st.sidebar.number_input('Distance to nearest primary school (in km)', step=0.1, format="%.1f", value=1.0)
        primary_school_vacancy = st.sidebar.number_input('Vacancy in the nearest primary school', step=1, format="%.0f", value=50)
        
        # Calculate pri_dist_vac
        pri_dist_vac = primary_school_distance * primary_school_vacancy

        data = {
            'flat_type': flat_type,
            'Tranc_YearMonth': Tranc_YearMonth,
            'floor_area_sqft': floor_area_sqft,
            'hdb_age': hdb_age,
            'total_dwelling_units': total_dwelling_units,
            'remaining_lease': remaining_lease,
            'amenities_1km': amenities_1km,
            'region': region,
            'flat_model': flat_model,
            'storey_category': storey_category,
            'pri_dist_vac': pri_dist_vac
        }
        
        return pd.DataFrame(data, index=[0])

    # Load the model
    model = load_model_pycaret()
    
    # Capture user input
    input_df = user_input_features()
    
    # Display input features
    st.subheader('User Input Parameters')
    st.write(input_df)

    # Predict when button is pressed
    if st.button('Predict'):
        result = predict(
            model,
            input_df['flat_type'][0],
            input_df['tranc_yearmonth'][0],
            input_df['floor_area_sqft'][0],
            input_df['hdb_age'][0],
            input_df['total_dwelling_units'][0],
            input_df['remaining_lease'][0],
            input_df['amenities_score'][0],
            input_df['region'][0],
            input_df['flat_model'][0],
            input_df['storey_category'][0],
            input_df['pri_dist_vac'][0]
        )
        st.success(f'The predicted resale price of the flat is ${result:.2f}')


# In[ ]:


if __name__ == '__main__':
    main()

