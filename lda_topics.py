#Working from example code at: 
#http://scikit-learn.org/stable/auto_examples/applications/plot_topics_extraction_with_nmf_lda.html#sphx-glr-auto-examples-applications-plot-topics-extraction-with-nmf-lda-py

from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer


#LDA tuning parameters
doc_name = "ast_example.txt"      #Name of the .txt file to extract topics from
n_topics = 3                #Number of topics to extract from the document(s)
min_word_freq = 1#0.05      #Ignore words that appear less frequently than this
max_word_freq = 1#0.95      #Ignore words that appear more frequently than this
n_top_words = 10            #The number of words to display for each topic


#Prints the topics and words associated with each topic for the given model
def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        message = "Topic #%d: " % topic_idx
        message += " ".join([feature_names[i]
                             for i in topic.argsort()[:-n_top_words - 1:-1]])
        print(message)
    print()


data = open(doc_name, "r")
tf_vectorizer = CountVectorizer(max_df=max_word_freq, min_df=min_word_freq,
                                stop_words='english')
tf = tf_vectorizer.fit_transform(data)
lda = LatentDirichletAllocation(n_components=n_topics)
lda.fit(tf)


tf_feature_names = tf_vectorizer.get_feature_names()
print_top_words(lda, tf_feature_names, n_top_words)
