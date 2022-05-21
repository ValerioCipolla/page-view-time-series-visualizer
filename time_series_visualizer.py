import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv",
                 parse_dates=["date"], index_col="date")

# Clean data
df = df[(df["value"] <= df["value"].quantile(0.975)) &
        (df["value"] >= df["value"].quantile(0.025))]


def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df.index, df["value"], "r", linewidth=1)
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar["year"] = df.index.year
    df_bar["month"] = df.index.month
    df_bar = df_bar.groupby(["year", "month"])["value"].mean()
    df_bar = df_bar.unstack()

    # Draw bar plot
    fig = df_bar.plot.bar(legend=True, figsize=(
        10, 5), xlabel="Years", ylabel="Average Page Views").figure
    plt.legend(["January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", "December"])
    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig


def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    df_box["month-num"] = df_box["date"].dt.month
    df_box = df_box.sort_values("month-num")
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(15, 10))
    axes[0] = sns.boxplot(x="year", y="value", data=df_box, ax=axes[0]).set(
        xlabel="Year", ylabel="Page Views", title="Year-wise Box Plot (Trend)")
    axes[1] = sns.boxplot(x="month", y="value", data=df_box, ax=axes[1]).set(
        xlabel="Month", ylabel="Page Views", title="Month-wise Box Plot (Seasonality)")
    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
