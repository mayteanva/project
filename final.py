
import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

# Defining the buttons to download the data later on
def to_csv(data_frame):
    return data_frame.to_csv().encode('utf-8')

class Button:
    def __init__(self, data, file_name):
        self.data = data
        self.file_name = file_name

    def display_button(self):
        st.download_button(label = f'Download participants data from {country_acronyms[country]}',
                   file_name = f'{self.file_name}_{country_acronyms[country]}.csv',
                   data = self.data,
                   mime = 'text/csv')

# Starting the app with the project logo, making it wither to see it better
logo = Image.open('logo.png')
st.image(logo, use_column_width=False, width=500)

# After the logo we put the tittle of the project in a steel blue to match the logo
st.markdown(f"<h1 style = 'color:steelblue;'>PARTNER SEARCH APP</h1>", unsafe_allow_html = True)

# Specyfing the country acronyms dictionary to be used
conn = sqlite3.connect('ecsel_database.db')
countries = pd.read_sql(f"SELECT * FROM countries", conn)
conn.close()

# Adding the menu to select the wanted country with the name to make it more user friendly
country = st.selectbox('Choose a country', sorted(countries.keys()))
st.write(f'You have chosen {country}')

# Dividing the document into two columns to change the layout
col1, col2 = st.columns(2)

# Dataframe of yearly contribution 
# Containing the total EC contribution per year in the selected country in ascending order of years
conn = sqlite3.connect('ecsel_database.db')
df_yearly_contributions = pd.read_sql(f"""
        SELECT strftime('%Y', p.startDate) AS Year, SUM(pt.ecContribution) AS ECContribution
        FROM Projects p
        JOIN Participants pt ON p.projectID = pt.projectID
        JOIN Countries c ON pt.country = c.Acronym
        WHERE c.Country = '{country}'
        GROUP BY Year
        ORDER BY Year ASC
        """, conn)
# Visualization of the yearly contribution graph in frst column and with stly that matches the theme of the app
with col1:
    st.markdown(f'<h2 style="color: lightsteelblue;">Yearly EC Contribution in {country}</h2>', unsafe_allow_html=True)
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df_yearly_contributions, x='Year', y='ECContribution', palette='Blues')
    plt.xticks(rotation=45)
    plt.xlabel('Year')
    plt.ylabel('EC Contribution (€)')
    plt.title(f'Yearly EC Contribution in {country}', color='steelblue')
    st.pyplot(plt.gcf())
conn.close()

# Dataframe of projects per year
# Containing the total number of projects in a year per selected country in ascending order of years
conn = sqlite3.connect('ecsel_database.db')
df_projects_per_year = pd.read_sql(f"""
        SELECT strftime('%Y', p.startDate) AS Year, COUNT(p.projectID) AS NumberOfProjects
        FROM Projects p
        JOIN Participants pt ON p.projectID = pt.projectID
        JOIN Countries c ON pt.country = c.Acronym
        WHERE c.Country = '{country}'
        GROUP BY Year
        ORDER BY Year ASC
        """, conn)
# Matching the style of the projects per year graph to the theme 
plt.figure(figsize=(10, 6))
sns.lineplot(data=df_projects_per_year, x='Year', y='NumberOfProjects', linewidth=2.5, marker='o')

plt.xticks(rotation=45)
plt.xlabel('Year')
plt.ylabel('Number of Projects')
plt.title('Yearly Projects Initiated in {country}', color='steelblue')

# Visualization of the yearly contribution graph in second column
with col2:
    st.markdown(f'<h2 style="color: lightsteelblue;">Yearly Projects Initiated in {country}</h2>', unsafe_allow_html=True)
    st.pyplot(plt.gcf())
conn.close()

# Continuing the theme of the two columns the df will also be shown this way 
col1, col2 = st.columns(2)


# Creation of participants data frame 
# Containing the total amount of received grants per partner in the selected country in descending order by received grants
conn = sqlite3.connect('ecsel_database.db')
df_participants = pd.read_sql(f"""SELECT p.shortName, p.name, p.activityType, p.organizationURL, SUM(p.ecContribution) AS ReceivedGrants, COUNT(p.name) AS TotalParticipations
                                        FROM participants AS p
                                        JOIN countries AS c
                                        ON c.Acronym = p.country
                                        WHERE c.Country = '{country}'
                                        GROUP BY p.shortName, p.name, p.activityType, p.organizationURL
                                        ORDER BY ReceivedGrants DESC""", conn)

conn.close()

# Visualization of data frame in the first column
# Matching the theme with a light steel blue title, a black backgorund and steel blue color for the data

with col1:
    st.markdown(f'<h2 style="color: lightsteelblue;">Participants in {country}</h2>', unsafe_allow_html=True)
    df_participants_stylized = df_participants.style.set_properties(**{'background-color': 'black', 'color': 'steelblue'})
    st.dataframe(df_participants_stylized)

csv_df_participants = to_csv(df_participants)

# Adding the first button configured at the beginning of the project to download the participants dataframe as csv
# In the first column as well so its under the dataframe 
with col1:
    first_button = Button(data = csv_df_participants, file_name = f'participants_from')
    first_button.display_button()

# Creation of coordinators data frame 
# Filtering only project coordinators

conn = sqlite3.connect('ecsel_database.db')
    # Duda: El count era totalpartners?
df_participants_coordinators = pd.read_sql(f"""SELECT p.shortName, p.name, p.activityType, p.projectAcronym
                                                    FROM participants AS p
                                                    JOIN countries AS c
                                                    ON c.Acronym = p.country
                                                    WHERE c.Country = '{country}' AND p.role = 'coordinator'
                                                    ORDER BY p.shortName ASC""", conn)
conn.close()

# Visualization of data frame in the second column
# Matching the theme with a light steel blue title, a black backgorund and steel blue color for the data

with col2:
    st.markdown(f'<h2 style="color: lightsteelblue;">Coordinators in {country}</h2>', unsafe_allow_html=True)
    df_participants_coordinators_stylized = df_participants_coordinators.style.set_properties(**{'background-color': 'black', 'color': 'steelblue'})
    st.dataframe(df_participants_coordinators_stylized)


csv_df_participants_coordinators = to_csv(df_participants_coordinators)

# Adding the second button configured at the beginning of the project to download the coordinators dataframe as csv
# In the second column as well so its under the dataframe 

with col2:
    second_button = Button(data = csv_df_participants_coordinators, file_name = f'coordinators_from')
    second_button.display_button()
