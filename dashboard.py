import streamlit as st
from streamlit_dynamic_filters import DynamicFilters
import pandas as pd
import plotly.express as px

# Upload data
file = st.file_uploader('Upload .xlsx hier')

if file:
    # Read data
    df = pd.read_excel(file).drop('Location', axis=1)

    # Drop rows without LR
    df.dropna(inplace=True, subset=['Log10 LR DNAxs'])

    # Print
    st.write(f"{len(df)} samples met Log10LRs gevonden")

    # Variables to filter / select
    VARIABLES = ['Weight (g)', 'Material', 'Position/ role', 'Volume (ul)', 'Movement (rpm) ', 'Duraction of contact (min)', 'Concentration ng/ml']

    # Set filters
    dynamic_filters = DynamicFilters(df=df, filters=VARIABLES)

    # Display filters and show dataframe
    dynamic_filters.display_filters(location='sidebar')
    dynamic_filters.display_df()

    # Plot boxplot using filtered df
    filtered_df = dynamic_filters.filter_df()

    # Set plot variable selectors
    variable = st.selectbox(label='boxplot_var', options=VARIABLES)
    second_var = st.selectbox(label='second_boxplot_var', options=VARIABLES)

    # Show swarmplot
    fig = px.strip(filtered_df, y='Log10 LR DNAxs', x=variable, color=second_var, hover_data =['Sample number'])
    st.write(fig)