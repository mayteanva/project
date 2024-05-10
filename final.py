# -*- coding: utf-8 -*-
"""final.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1-c3rA6vMncx0Ixb89smsFBwG7tHhVXya
"""



import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from PIL import Image

# Custom CSS to improve the look and feel
st.markdown("""
<style>
.primaryFont {
    font-size:16px;
    font-family: 'Helvetica';
    color: #4a4a4a;
}
.big-font {
    font-size:20px !important;
    font-weight: bold;
    color: #3466f6;
}
</style>
""", unsafe_allow_html=True)

# Function to be used to download the files as csv files
def to_csv(data_frame):
    return data_frame.to_csv().encode('utf-8')

class Button:
    def __init__(self, data, file_name):
        self.data = data
        self.file_name = file_name

    def display_button(self):
        st.download_button(label = f'Download participants data from {countries_dictionary[country]}',
                   file_name = f'{self.file_name}_{countries_dictionary[country]}.csv',
                   data = self.data,
                   mime = 'text/csv')

  # 1. Adding the logo of the application
logo = Image.open('logo.png')

# In order to center the logo, the following process will be applied:
container = st.beta_container()

with container:
    col1, col2, col3 = st.beta_columns(3)
    col2.image(logo, width=250)
    col1.empty()
    col3.empty()

  # 2. Adding the title of the app
st.markdown(f"<h1 style = 'color:#307be8;'>PARTNER SEARCH APP</h1>", unsafe_allow_html = True)


# Country acronyms dictionary
country_acronyms = {
    'Belgium': 'BE', 'Bulgaria': 'BG', 'Czechia': 'CZ', 'Denmark': 'DK', 'Germany': 'DE',
    'Estonia': 'EE', 'Ireland': 'IE', 'Greece': 'EL', 'Spain': 'ES', 'France': 'FR', 'Croatia': 'HR',
    'Italy': 'IT', 'Cyprus': 'CY', 'Latvia': 'LV', 'Lithuania': 'LT', 'Luxembourg': 'LU',
    'Hungary': 'HU', 'Malta': 'MT', 'Netherlands': 'NL', 'Austria': 'AT', 'Poland': 'PL',
    'Portugal': 'PT', 'Romania': 'RO', 'Slovenia': 'SI', 'Slovakia': 'SK', 'Finland': 'FI', 'Sweden': 'SE'
}

 country = st.selectbox('Choose a country', sorted(country_acronyms.keys()))
 st.write(f'You have chosen {country}')

  conn = sqlite3.connect('ecsel_database.db')
    df_participants = pd.read_sql(f"""SELECT p.shortName, p.name, p.activityType, p.organizationURL, SUM(p.ecContribution) AS ReceivedGrants, COUNT(p.name) AS TotalParticipations
                                        FROM participants AS p
                                        JOIN countries AS c
                                        ON c.Acronym = p.country
                                        WHERE c.Country = '{country}'
                                        GROUP BY p.shortName, p.name, p.activityType, p.organizationURL
                                        ORDER BY ReceivedGrants DESC""", conn)

    conn.close()

   # Display it:
    st.subheader(f'Participants in {country}')
    # Style the dataframe beforehand
    df_participants_stylized = df_participants.style.set_properties(**{'background-color': '#f2f9ff', 'color': '#000000'})
    st.dataframe(df_participants_stylized)

    csv_df_participants = to_csv(df_participants)

    first_button = Button(data = csv_df_participants, file_name = f'participants_from')
    first_button.display_button()

 conn = sqlite3.connect('ecsel_database.db')
    # Duda: El count era totalpartners?
    df_participants_coordinators = pd.read_sql(f"""SELECT p.shortName, p.name, p.activityType, p.projectAcronym
                                                    FROM participants AS p
                                                    JOIN countries AS c
                                                    ON c.Acronym = p.country
                                                    WHERE c.Country = '{country}' AND p.role = 'coordinator'
                                                    ORDER BY p.shortName ASC""", conn)
    conn.close()

     st.subheader(f'Coordinators in {country}')
    # Style the dataframe beforehand
    df_participants_coordinators_stylized = df_participants_coordinators.style.set_properties(**{'background-color': '#f2f9ff', 'color': '#000000'})
    st.dataframe(df_participants_coordinators_stylized)

    csv_df_participants_coordinators = to_csv(df_participants_coordinators)

    second_button = Button(data = csv_df_participants_coordinators, file_name = f'coordinators_from')
    second_button.display_button()
