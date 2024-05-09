# -*- coding: utf-8 -*-
"""final.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1-c3rA6vMncx0Ixb89smsFBwG7tHhVXya
"""

import streamlit as st
import sqlite3

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

# Country acronyms dictionary
country_acronyms = {
    'Belgium': 'BE', 'Bulgaria': 'BG', 'Czechia': 'CZ', 'Denmark': 'DK', 'Germany': 'DE',
    'Estonia': 'EE', 'Ireland': 'IE', 'Greece': 'EL', 'Spain': 'ES', 'France': 'FR', 'Croatia': 'HR',
    'Italy': 'IT', 'Cyprus': 'CY', 'Latvia': 'LV', 'Lithuania': 'LT', 'Luxembourg': 'LU',
    'Hungary': 'HU', 'Malta': 'MT', 'Netherlands': 'NL', 'Austria': 'AT', 'Poland': 'PL',
    'Portugal': 'PT', 'Romania': 'RO', 'Slovenia': 'SI', 'Slovakia': 'SK', 'Finland': 'FI', 'Sweden': 'SE'
}

def load_data():
    conn = sqlite3.connect('ecsel_database.db')
    query_countries = "SELECT DISTINCT country FROM Participants;"
    df_countries = pd.read_sql(query_countries, conn)
    return df_countries

def get_participants(country_acronym):
    conn = sqlite3.connect('ecsel_database.db')
    query = f"""SELECT shortName, name, activityType, organizationURL, SUM(ecContribution) as totalGrants
                FROM Participants WHERE country='{country_acronym}'
                GROUP BY organisationID
                ORDER BY totalGrants DESC;"""
    df_participants = pd.read_sql(query, conn)
    return df_participants

def get_coordinators(country_acronym):
    conn = sqlite3.connect('ecsel_database.db')
    query = f"""SELECT shortName, name, activityType, projectAcronym
                FROM Participants WHERE country='{country_acronym}' AND role='Coordinator'
                ORDER BY shortName ASC;"""
    df_coordinators = pd.read_sql(query, conn)
    return df_coordinators

def get_grants_evolution(country_acronym):
    conn = sqlite3.connect('ecsel_database.db')
    query = f"""SELECT activityType, SUM(ecContribution) as totalGrants
                FROM Participants WHERE country='{country_acronym}'
                GROUP BY activityType;"""
    df_grants_evolution = pd.read_sql(query, conn)
    return df_grants_evolution

st.title('Ecsel Project Management System')

# Layout and color enhancements using columns and Streamlit methods
col1, col2 = st.columns(2)

with col1:
    # Load countries with enhanced dropdown
    df_countries = load_data()
    country = st.selectbox('Select a country', df_countries['country'], key='countrySelect', help='Select a country to display data for.')

country_acronym = country_acronyms.get(country)

if country_acronym:
    with col2:
        st.markdown("<p class='big-font'>Data Overview</p>", unsafe_allow_html=True)
        # Display Participants Data
        df_participants = get_participants(country_acronym)
        st.write('Participants Data:', df_participants.style.set_properties(**{'background-color': '#f0f0f0', 'color': '#3466f6'}))

    # Display Coordinators Data
    df_coordinators = get_coordinators(country_acronym)
    st.markdown("<p class='big-font'>Coordinator Overview</p>", unsafe_allow_html=True)
    st.write('Coordinators Data:', df_coordinators)

    # Graph of evolution of grants
    df_grants_evolution = get_grants_evolution(country_acronym)
    fig = px.bar(df_grants_evolution, x='activityType', y='totalGrants', title='Evolution of Received Grants by Activity Type', color='activityType')
    st.plotly_chart(fig, use_container_width=True)

    # Export buttons
if st.button('Download Participants Data'):
        df_participants.to_csv('participants_data.csv')
        st.success('Participants data downloaded successfully!')

if st.button('Download Coordinators Data'):
        df_coordinators.to_csv('coordinators_data.csv')
        st.success('Coordinators data downloaded successfully!')


