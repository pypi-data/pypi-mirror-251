"""Streamlit component to display a sample of a dataframe and its schema."""

import pandas as pd
import streamlit as st


def display_sample_df_container(sample_df: pd.DataFrame) -> pd.DataFrame:
    """Display a sample of the selected dataframe."""
    st.write("---")
    st.header("Sample data")
    col1, col2 = st.columns(spec=[4, 1])
    with col1:
        st.warning(f":warning: Sample DataFrame - {len(sample_df)} rows")
        # Streamlit does not support displaying timedelta types at the moment.
        if (sample_df.dtypes == "timedelta64[ns]").any():
            td_cols = sample_df.dtypes.index[sample_df.dtypes == "timedelta64[ns]"]
            for col in td_cols:
                sample_df[col] = sample_df[col].dt.total_seconds()

        st.write(sample_df)
    with col2:
        st.subheader("Schema")
        schema_df = pd.DataFrame(sample_df.dtypes).rename(columns={0: "types"})
        st.write(schema_df)
