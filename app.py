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

st.header('Latest News')
selected = st.selectbox('Filter by competitor', ['All'] + competitors)

def show_news(name, items):
    st.subheader(name)
    for item in items:
        st.write(f"{item['date']} - {item['title']}")
        st.write(item['summary'])

if selected == 'All':
    for name, items in news_data.items():
        show_news(name, items)
else:
    entries = news_data.get(selected, [])
    show_news(selected, entries)
    summaries = [item['summary'] for item in entries]
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

