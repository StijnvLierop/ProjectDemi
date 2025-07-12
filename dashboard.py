import numpy as np
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

    # Calculate log concentration
    df['log10 concentration ng/ml'] = df['Concentration ng/ml'].apply(
        lambda x: np.log10(x))

    # Create failed LR column
    df['LR calculation'] = 'successful'
    df.loc[df['Log10 LR DNAxs'] == -1, 'LR calculation'] = 'failed'

    # Variables to filter / select
    VARIABLES = ['Weight (g)', 'Material', 'Position/role', 'Volume (ul)',
                 'Movement (rpm)', 'Duration of contact (min)',
                 'Concentration ng/ml', 'log10 concentration ng/ml',
                 'Log10 LR DNAxs']

    # Set filters
    dynamic_filters = DynamicFilters(df=df, filters=VARIABLES)

    # Display filters and show dataframe
    dynamic_filters.display_filters(location='sidebar')
    dynamic_filters.display_df()

    # Plot boxplot using filtered df
    filtered_df = dynamic_filters.filter_df()

    # Set plot variable selectors
    variable = st.selectbox(label='var 1', options=VARIABLES)
    second_var = st.selectbox(label='var 2', options=VARIABLES)
    y_var = st.selectbox(label='y var', options=VARIABLES)

    # Filter out unsuccessful LRs
    filter_failed_LRs = st.checkbox(label='filter failed LRs')
    if filter_failed_LRs:
        filtered_df = filtered_df[filtered_df['LR calculation'] != 'failed']

    # Show swarmplot
    fig = px.strip(filtered_df, y=y_var, x=variable, color=second_var, hover_data =['Sample number'])
    st.write(fig)

    # Show boxplot
    fig = px.box(filtered_df, y=y_var, x=variable, color=second_var, hover_data =['Sample number'])
    st.write(fig)

    # Show correlation matrix
    fig = px.imshow(filtered_df.corr(numeric_only=True), text_auto=True)
    st.write(fig)