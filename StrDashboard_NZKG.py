import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

#import plotly.express as px
#import plotly.graph_objects as go
#import yfinance as yf 

# Import document
df = pd.read_excel('BAL_DEF_updated.xlsx')
theme_counts = pd.read_excel('gemiddelden .xlsx')

st.write("""
        # Milieubelastende activiteiten 
        ## *Aantal BAL thema's per MBA*
         """)

# Get unique 'Paragraaf' values for the multi-select widget
paragraph_options = df['Paragraaf'].unique().tolist()

# Create the multi-select sidebar widget without any default values selected
selected_paragraphs = st.sidebar.multiselect(
    'Selecteer de gewenste Paragraaf',
    options=paragraph_options
    # Note: No default is set, so all options are unselected initially
)

# Filter the DataFrame based on the selected paragraphs
if selected_paragraphs:
    # Filter the data for selected paragraphs
    filtered_data = df[df['Paragraaf'].isin(selected_paragraphs)]
else:
    # If nothing is selected, consider all options as selected
    filtered_data = df

# Count the occurrences of each 'Thema' in the filtered data
theme_counts = filtered_data['Thema'].value_counts().reset_index()
theme_counts.columns = ['Thema', 'Totaal van Paragraaf']

# Sort the counts in descending order for the plot
theme_counts.sort_values(by='Totaal van Paragraaf', ascending=False, inplace=True)

# Set up the layout with columns
col1, col2 = st.columns((3, 1))  # Adjust the ratio as needed

# First column for the bar plot
with col1:
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.barplot(
        x='Totaal van Paragraaf',
        y='Thema',
        data=theme_counts,
        ax=ax,
        palette='coolwarm'
    )
    ax.set_title('Aantal thema\'s per paragraaf')
    ax.grid(True, linestyle='--', linewidth=0.5, color='grey')
    st.pyplot(fig)

# Second column for the metric tiles
with col2:
    st.write("""
             #### *Aantal thema's per paragraaf*
             """)  # You can add a title for the metrics section
    for thema, totaal in theme_counts.itertuples(index=False):
        st.metric(label=thema, value=totaal)

# Manually creating a DataFrame for the averages from the screenshot
average_counts = pd.DataFrame({
    'Thema': ['lucht', 'water', 'bodem', 'externe veiligheid', 'module', 
              'afval', 'energie', 'geluid', 'lucht en geluid', 'lucht en geur', 
              'gezondheid', 'veiligheid', 'geur', 'lichtschittering', 'water en gezondheid'],
    'Gemiddeld aantal mba\'s': [8.5, 3.5, 2.5, 2.7, 1, 2.3, 2.2, 2.3, 1, 1, 
                                1.5, 3, 1, 2, 2]
})

# Merge the average counts with the theme_counts to calculate the difference
theme_analysis = theme_counts.merge(average_counts, on='Thema', how='left').round(1)

# Calculate the difference
theme_analysis['Verschil met gemiddelde'] = theme_analysis['Totaal van Paragraaf'] - theme_analysis['Gemiddeld aantal mba\'s']

# Round the 'Gemiddeld aantal mba\'s' column to one decimal place and format as string
theme_analysis['Gemiddeld aantal mba\'s'] = theme_analysis['Gemiddeld aantal mba\'s'].round(1).map('{:.1f}'.format)

# Calculate the difference and round the 'Verschil met gemiddelde' column to one decimal place, then format as string
theme_analysis['Verschil met gemiddelde'] = (theme_analysis['Totaal van Paragraaf'] - theme_analysis['Gemiddeld aantal mba\'s'].astype(float)).round(1)
theme_analysis['Verschil met gemiddelde'] = theme_analysis['Verschil met gemiddelde'].map('{:.1f}'.format)

# Create a new DataFrame with only the necessary columns for display
theme_display = theme_analysis[['Thema', 'Gemiddeld aantal mba\'s', 'Verschil met gemiddelde']]

# Display the updated DataFrame in Streamlit without the index
st.write("""
         #### *Analyse van ieder thema: het gemiddeld aantal mba's per paragraaf en het verschil in aantal van dit gemiddelde per geselecteerde paragraaf*
         """)
st.table(theme_display)

# Pivot the data with 'Paragraaf' as the index and 'Thema' as columns
# Counting the number of occurrences of each 'Thema' per 'Paragraaf'
pivot_df = pd.pivot_table(df, values='lidnr', index='Paragraaf', columns='Thema', aggfunc='count', fill_value=0)

# List of new column names provided by the user
new_column_names = [
    "lucht", "water", "bodem", "externe veiligheid", "module",
    "afval", "energie", "geluid", "lucht en geluid", "lucht en geur",
    "gezondheid", "veiligheid", "geur", "lichtschittering", "water en gezondheid"
]

# Map the original 'Thema' values to the new names if they don't match
# This is a placeholder for the correct mapping based on the user's data
# The actual mapping should be defined according to the specific values in the 'Thema' column of the data
thema_mapping = {thema: new_name for thema, new_name in zip(pivot_df.columns, new_column_names)}

# Rename the columns using the mapping
pivot_df_renamed = pivot_df.rename(columns=thema_mapping)

# Use the created pivot table for display in Streamlit
st.write("""
         #### *Interactieve Tabel: Aantal thema's per paragraaf*
         """)
st.dataframe(pivot_df_renamed)

