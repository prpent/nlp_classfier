# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 14:36:17 2022

@author: velua

Editors:Pravallika
"""
# !pip install textblob
#!pip install wordcloud

import streamlit as st 
import joblib,os
import spacy
import pandas as pd
nlp = spacy.load('en_core_web_sm')
import matplotlib.pyplot as plt 
import matplotlib
matplotlib.use("Agg")
from PIL import Image
import seaborn as sns
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import emoji
from textblob import TextBlob
import re

 # wordcloud function
def show_wordcloud(data, title = None):
    from wordcloud import WordCloud,STOPWORDS
    plt.figure(figsize=(12,12))
    wc = WordCloud(max_words=1000, 
               min_font_size=10,
               height=600,
               width=1600,
               background_color='black',
               contour_color='black',
               colormap='plasma',
               repeat=False,
               stopwords=STOPWORDS).generate(' '.join(data))

    plt.title("Word Cloud with Headlines", size=15, weight='bold')
    plt.imshow(wc, interpolation= "bilinear")
    plt.axis('off')
    st.pyplot(plt)
    
def plot_by_category(data):
    plt.figure(figsize=(12,8))
    count = data.value_counts()
    sns.barplot(x=count.index, y=count)
    plt.xlabel('Category')
    plt.ylabel('Count')
    plt.xticks(rotation=90)
    st.pyplot(plt)
    
def plot_Top10_category(data):
    cat_df = pd.DataFrame(data.value_counts()).reset_index()
    cat_df.rename(columns={'index':'news_classes','category':'numcat'}, inplace=True)

    # Visualize top 10 categories and proportion of each categories in dataset
    plt.figure(figsize=(10,6))
    ax = sns.barplot(np.array(cat_df.news_classes)[:10], np.array(cat_df.numcat)[:10])
    for p in ax.patches:
        ax.annotate(p.get_height(), (p.get_x()+0.01, p.get_height() + 50))
    plt.title("TOP 10 Categories of News articles", size=15)
    plt.xlabel("Categories of articles", size=14)
    plt.xticks(rotation=45)
    plt.ylabel("Number of articles", size=14)
    st.pyplot(plt)  
    
def Visualization():
    st.info("Dataset Information:")
    News = pd.read_json("News_Category_Dataset_v2.json",lines=True)
    st.write(News.head())
    st.write(News.shape)
    News['Headline_Combined']= News["headline"] +"" +News["short_description"]
    plotChoice = st.sidebar.selectbox("Select the plot you want to see",["Number of headlines for each category","Top 10 News Categories","Display Word Cloud With Headlines"])
    if plotChoice=="Number of headlines for each category":
        st.info("Number of headlines for each category")
        plot_by_category(News['category'])
    elif plotChoice=="Display Word Cloud With Headlines":
        st.info("Word Cloud with Headlines")
        show_wordcloud(News['Headline_Combined'])
        #show_wordcloud(News['category'])
    else:
        st.info("Display Top 10 News Categories")
        plot_Top10_category(News['category'])
    
   
def clean_news(text):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())    


def home_page_module():
    st.title("News Headlines Classification")
    image = Image.open("Projectimage.jpeg")
    st.image( image , caption='** Classify a News** ' )
    st.subheader("About Application:")
    st.write("The objective of this project is to create a web application that can consume news headline sentences and provide a classification label to understand what the topic of the news article is and suggest an overall article sentiment.")
    
    st.write("Usefullness: News is all around us through the internet or Television keeping us up to date on the daily events as they happen. There are over 5000 news articles published just in the United States every day [1]. The amount of News articles available to consumers can be overwhelming and requires a process to classify them, this helps the reader to focus on the articles that are of interest to them. This process filters the news articles to an extent but in addition to news topic classification, we would like to provide a suggested sentiment on a news article such that the consumer has an additional piece of information before reading the article and potentially decide on whether to read the article.")
   
    st.write("Build By Fall 2022 NLP Team: Agalya Velusamy, Pravallika Pentapati and Srikanth Bolishetty")

     
     #return doc
def nlp_task():
    st.title("Natural Language Processing Tasks")
    raw_text = st.text_area("Enter News Here","Type Here")
    nlp_task = ["Select NLP Task","Tokenization","Lemmatization","Named Entity Recognition","Parts Of Speech Tags","Sentiment Analysis"]
    task_choice = st.selectbox("Choose NLP Task",nlp_task)
    if st.button("Analyze"):
         st.info("Original Text::\n{}".format(raw_text))

         docx = nlp(raw_text)
         if task_choice == 'Tokenization':
             st.caption("Result:")
             result = [token.text for token in docx ]
             st.text(result)
         elif task_choice == 'Lemmatization':
             result = ["'Token':{},'Lemma':{}".format(token.text,token.lemma_) for token in docx]
             st.text(result)
         elif task_choice == 'Named Entity Recognition':
             for entity in docx.ents:
                 result=[f"{entity.text:-<{20}}{entity.label_:-<{20}}{str(spacy.explain(entity.label_))}"] 
                 st.text(result)
         elif task_choice == 'Parts Of Speech Tags':
               result = ["'Token':{},'POS':{},'Dependency':{}".format(word.text,word.tag_,word.dep_) for word in docx]
               st.json(result)  
         elif task_choice=='Sentiment Analysis':
             analysis = TextBlob(clean_news(raw_text))
             result = analysis.sentiment.polarity
             if result > 0.0:
                 custom_emoji = ':smile:'
                 st.write("smile",emoji.emojize(custom_emoji))
             elif result < 0.0:
                 custom_emoji = ':disappointed:'
                 st.write("sad",emoji.emojize(custom_emoji))
             else:
                 st.write("neutral",emoji.emojize(':expressionless:'))
             st.info("Polarity Score is:: {}".format(result))
                
                
            
     
         


    
  
def  prediction_task():
     st.info("News Category Prediction")
     user_headline=st.text_area('Enter your news headline to predict news category')
     if(st.button('Predict')):
         st.success("In Process")      
def main():
    if 'loggedIn' not in st.session_state:
        st.session_state.loggedIn = False
    
    menu = ["Home","NLP Task" ,"Prediction Task","Statistical Plots"]
    choice = st.sidebar.selectbox("Menu",menu )

    ## HOME PAGE
    if choice == "Home":
        home_page_module()
    elif choice =="NLP Task":
        nlp_task()
    elif choice=="Prediction Task": 
        prediction_task()
    elif choice=="Statistical Plots":
        Visualization()
    else:
        st.write("Under Development")
if __name__ == '__main__':
    main()        