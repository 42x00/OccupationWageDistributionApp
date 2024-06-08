import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("data/onet_monthly_average_wage_2023.csv"), pd.read_csv("data/onet_name.csv").set_index("onet_cd")['name'].to_dict()

df, onet2name = load_data()

with st.sidebar:
    st.title("Occupation Wage Distribution App")
    onets = st.multiselect("Select Occupations", onet2name.keys(), format_func=lambda x: onet2name[x])
    nbins = st.text_input("Number of Bins", "Auto")
    nbins = None if nbins.lower() == "auto" else int(nbins)
    if not onets:
        st.stop()


data = df[df['onet_cd'].isin(onets)]
data['onet_cd'] = data['onet_cd'].map(onet2name)

fig = px.histogram(data, x="wage", nbins=nbins, color="onet_cd", histnorm='probability', marginal="violin",
                   barmode='overlay', labels={"wage": "Monthly Average Wage", "onet_cd": "Occupation"}, template="ggplot2")

fig.update_layout(xaxis_tickprefix="$", yaxis_tickformat='.1%', height=800)

tabs = st.tabs(["Histogram", "Description"])

with tabs[0]:
    st.plotly_chart(fig, use_container_width=True, theme=None)

with tabs[1]:
    st.dataframe(data.groupby("onet_cd")['wage'].describe().T)