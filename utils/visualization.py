# utils/visualization.py
import matplotlib.pyplot as plt
import seaborn as sns


def plot_sentiment_by_rating(df):
    fig, axs = plt.subplots(1, 3, figsize=(15, 3))
    sns.barplot(data=df, x='rating', y='pos', ax=axs[0])
    sns.barplot(data=df, x='rating', y='neu', ax=axs[1])
    sns.barplot(data=df, x='rating', y='neg', ax=axs[2])
    axs[0].set_title('Positive')
    axs[1].set_title('Neutral')
    axs[2].set_title('Negative')
    return fig
