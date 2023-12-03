
import seaborn as sns
from matplotlib import colors
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go 
from wordcloud import WordCloud, STOPWORDS
from nltk.util import bigrams, trigrams
import seaborn as sns
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Load the generated Jumia reviews dataset
data = pd.read_csv('ReviewsDataset.csv', encoding='ISO-8859-1')
df = pd.DataFrame(data)
df['reviews'] = df['reviews.title'].astype(str) + " " + df['reviews.text']
df = df.drop(['reviews.title', 'reviews.text'], axis=1)

st.sidebar.title("Sentiment Analysis of Reviews")
st.markdown("This is a dashboard used to analyze sentiments of reviews ")
st.sidebar.markdown("This is a dashboard used to analyze sentiments of reviews ")

@st.cache_data(persist=True)
def load_data():
    data = pd.read_csv('ReviewsDataset.csv', encoding='ISO-8859-1')
    df = pd.DataFrame(data)
    df['reviews'] = df['reviews.title'].astype(str) + " " + df['reviews.text']
    df = df.drop(['reviews.title', 'reviews.text'], axis=1)
    df['reviews.date'] = pd.to_datetime(df['reviews.date'], format='%d-%m-%y')
    return df  # Return df instead of data

data = load_data()

st.sidebar.subheader("Show random review")
random_review = st.sidebar.radio('sentiment', ('positive', 'neutral', 'negative'))
selected_review = data.query("sentiment == @random_review").sample(n=1)['reviews'].iat[0]
st.sidebar.markdown(selected_review)

st.sidebar.markdown("### Number of reviews by sentiment")
select = st.sidebar.selectbox('Visualization type', ['Bar plot', 'Pie chart'], key='1')
sentiment_count = data['sentiment'].value_counts()
sentiment_count = pd.DataFrame({'sentiment':sentiment_count.index, 'reviews':sentiment_count.values})
if not st.sidebar.checkbox("Hide", True):
    st.markdown("### Number of reviews by sentiment")
    if select == 'Bar plot':
        fig = px.bar(sentiment_count, x='sentiment', y='reviews', color='reviews', height=500)
        st.plotly_chart(fig)
    else:
        fig = px.pie(sentiment_count, values='reviews', names='sentiment')
        st.plotly_chart(fig)
st.sidebar.subheader("Total number of reviews for categories")
each_category = st.sidebar.selectbox('Visualization type', ['Bar plot', 'Pie chart'], key='category_selection')

sentiment_count = data.groupby('categories')['sentiment'].count().sort_values(ascending=False)
sentiment_count = pd.DataFrame({'categories': sentiment_count.index, 'reviews': sentiment_count.values.flatten()})

if not st.sidebar.checkbox("Close", True, key='close_checkbox'):
    if each_category == 'Bar plot':
        st.subheader("Total number of reviews for each category")
        fig_1 = px.bar(sentiment_count, x='categories', y='reviews', color='reviews', height=500)
        st.plotly_chart(fig_1)
    elif each_category == 'Pie chart':
        st.subheader("Total number of reviews for each category")
        fig_2 = px.pie(sentiment_count, values='reviews', names='categories')
        st.plotly_chart(fig_2)
        
st.sidebar.header("Word Cloud")
word_sentiment = st.sidebar.radio('Display word cloud for what sentiment?', ('positive', 'neutral', 'negative'))
if not st.sidebar.checkbox("Close", True, key='3'):
    st.subheader('Word cloud for %s sentiment' % (word_sentiment))
    df = data[data['sentiment']==word_sentiment]
    words = ' '.join(df['reviews'])
    processed_words = ' '.join([word for word in words.split() if 'http' not in word and not word.startswith('@') and word != 'RT'])
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white', width=800, height=640).generate(processed_words)
    fig, ax = plt.subplots()
    ax.imshow(wordcloud)
    ax.set_xticks([])
    ax.set_yticks([])

    # Pass the Matplotlib figure to st.pyplot()
    st.pyplot(fig)
