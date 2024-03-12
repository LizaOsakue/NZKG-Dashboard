from pathlib import Path

import appdirs as ad

CACHE_DIR = ".cache"

# Force appdirs to say that the cache dir is .cache
ad.user_cache_dir = lambda *args: CACHE_DIR

# Create the cache dir if it doesn't exist
Path(CACHE_DIR).mkdir(exist_ok=True)


from collections import UserString
import streamlit as st
import yfinance as yf 
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Import document
df = pd.read_excel('/Users/lizaosakue/Desktop/Streamlit/BAL_DEF_updated.xlsx')
theme_counts = pd.read_excel('/Users/lizaosakue/Desktop/Streamlit/gemiddelden .xlsx')

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
