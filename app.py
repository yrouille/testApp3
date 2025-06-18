import json
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
with open('data/competitor_news.json') as f:
    news_data = json.load(f)
with open('data/marketing_counts.json') as f:
    marketing_data = json.load(f)

competitors = list(news_data.keys())

st.title('Competitive Intelligence Dashboard')

st.header('Latest News Across Competitors')
for name, items in news_data.items():
    st.subheader(name)
    for item in items:
        st.write(f"{item['date']} - {item['title']}")
        st.write(item['summary'])

st.header('Latest News for a Specific Competitor')
selected = st.selectbox('Choose a competitor', competitors)

if selected:
    st.subheader(f'News for {selected}')
    entries = news_data.get(selected, [])
    summaries = []
    for item in entries:
        st.write(f"{item['date']} - {item['title']}")
        st.write(item['summary'])
        summaries.append(item['summary'])
    if summaries:
        st.markdown('**Summary of highlighted features:**')
        for s in summaries:
            st.write('-', s)

st.header('Marketing Communication Activity')
fig, ax = plt.subplots()
keys = list(marketing_data.keys())
values = [marketing_data[k] for k in keys]
ax.bar(keys, values, color='skyblue')
ax.set_xlabel('Solution')
ax.set_ylabel('Number of marketing communications')
ax.set_title('Marketing Activity')
st.pyplot(fig)

