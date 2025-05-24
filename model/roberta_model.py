import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import nltk
from nltk.tokenize import word_tokenize
from nltk.sentiment import SentimentIntensityAnalyzer
from tqdm import tqdm

# nltk.download('vader_lexicon')
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('maxent_ne_chunker')
# nltk.download('words')

plt.style.use('ggplot')


# Read in data

df = pd.read_csv(r"dataset\amazon_reviews_500.csv")

# NLTK
example = df['review_text'][50]
tokens = word_tokenize(example)
tagged = nltk.pos_tag(tokens)
entities = nltk.chunk.ne_chunk(tagged)

# Vader model
sia = SentimentIntensityAnalyzer()

# Run the polarity score on the entire dataset
res = {}
for i, row in tqdm(df.iterrows(), total=len(df)):
    text = row["review_text"]
    myid = row['review_id']
    res[myid] = sia.polarity_scores(text)


vaders = pd.DataFrame(res).T
vaders = vaders.reset_index().rename(columns={'index': 'review_id'})
vaders = vaders.merge(df, how='left')

print(vaders.head())

ax = sns.barplot(data=vaders, x='rating', y='compound')
ax.set_title('compund Score by amazon star review')
# plt.show()

fig, axs = plt.subplots(1, 3, figsize=(15, 3))
sns.barplot(data=vaders, x='rating', y='pos', ax=axs[0])
sns.barplot(data=vaders, x='rating', y='neu', ax=axs[1])
sns.barplot(data=vaders, x='rating', y='neg', ax=axs[2])
axs[0].set_title('Positive')
axs[1].set_title('neutral')
axs[2].set_title('negetive')
plt.show()
