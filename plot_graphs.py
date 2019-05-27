import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
import matplotlib.axes as axes
import matplotlib.ticker as ticker
import matplotlib
import seaborn as sns
from datetime import datetime

DEADLINE='2019-07-31-235959'
PLOT_DEADLINE=False
WORDS_COLOR='purple'
PAGES_COLOR='blue'
MPL_BACKEND='agg'
COLOR_SET= ['red', 'goldenrod', 'gold', '#FFFF79', 'aquamarine', 'green']

def get_times_as_date_time(times):
    # Convert times to DateTime
    timesdf = []
    for time in times:    
        timesdf.append(datetime.strptime(time, '%Y-%m-%d-%H%M%S'))
    return timesdf

def plot_simple_line(input_file, output_file):

    # Import the data
    df = pd.read_csv(input_file)
    
    # Rename columns and get as Series
    df.columns = ['Time', 'Pages', 'Words']
    times = df['Time']
    pages = df['Pages']
    words = df['Words']
    
    # Convert times to DateTime
    timesdf = get_times_as_date_time(times)
    
    # Get references to the figure and axes
    fig = plt.figure()
    ax = plt.gca()
    ax2 = ax.twinx()
    
    # Make a large graph
    fig.set_size_inches(20, 10)
    
    # Plot the times and counts
    ax.plot(timesdf, pages, color=PAGES_COLOR)
    ax.set_ylabel('pages', color=PAGES_COLOR)
    ax.tick_params('y', colors=PAGES_COLOR)
    ax.set_xlabel('date')
    
    # Y axis between 0 and 300 (limit for PhD thesis)
    ax.set_ylim([0,350])
    
    # Plot ave length
    ax.axhline(y=140, linestyle=':', color='green')
    ax.axhline(y=300, linestyle='--', color='red')
    
    ax2.plot(timesdf, words, color=WORDS_COLOR)
    ax2.set_ylabel('words', color=WORDS_COLOR)
    ax2.tick_params('y', colors=WORDS_COLOR)
    
    # Second Y axis between 0 and 80,000 (limit for PhD thesis)
    ax2.set_ylim([0,80000])
    
    # Rotate x labels
    fig.autofmt_xdate()
    
    # Format the DateTime labels
    myFmt = mdates.DateFormatter('%Y-%m-%d')
    ax.xaxis.set_major_formatter(myFmt)
    ax.xaxis_date()
    
    if PLOT_DEADLINE:
        ax.axvline(x=datetime.strptime(DEADLINE, '%Y-%m-%d-%H%M%S'), linestyle='--', color='red')
    
    # Save the plot out
    plt.savefig(output_file)
    
    # Comment out for command line
    # plt.show()
    
    # Close the plot
    plt.close()
    
    
def plot_stacked_regions(input_file, output_image):
    
    # Import the data
    df = pd.read_csv(input_file)

    # Get series    
    times = df['TIME']
    categories = [ df['TODO'], df['STARTED'], df['FIRST_DRAFT'], df['SECOND_DRAFT'], df['REVISIONS_DONE'], df['COMPLETE'] ]
    timesdf = get_times_as_date_time(times)
    
    # Normalize each observation to total to 100%
    categories = normalize_categories(categories)
        
    # Make a large graph
    fig = plt.figure()
    fig.set_size_inches(20, 10)

    # Plot graph
    plt.stackplot(timesdf, categories, labels=['TODO', 'STARTED', 'FIRST_DRAFT', 'SECOND_DRAFT', 'REVISIONS_DONE', 'COMPLETE'], 
                  colors=COLOR_SET)
    
    # Rotate x labels
    fig.autofmt_xdate()
    
    # Format the DateTime labels
    ax = plt.gca()
    myFmt = mdates.DateFormatter('%Y-%m-%d')
    ax.xaxis.set_major_formatter(myFmt)
    ax.xaxis_date()
    ax.set_xlabel('date')

    # Set Y axis as percentages
    ax.set_ylabel('% of categories')
    ax.yaxis.set_major_formatter(ticker.PercentFormatter())
    ax.legend(loc=3)
    
    
    if PLOT_DEADLINE:
        ax.axvline(x=datetime.strptime(DEADLINE, '%Y-%m-%d-%H%M%S'), linestyle='--', color='red')
    
    # Save the plot out
    plt.savefig(output_image)
    
    # Show the plot (comment out for command line)
    # plt.show()

    plt.close()
    
def plot_combined(states_file, counts_file, output_image):
    
    # Import the data
    df_count = pd.read_csv(counts_file)
    df_states = pd.read_csv(states_file)
    
    # Rename columns and get as Series
    df_count.columns = ['Time', 'Pages', 'Words']
    times_count = df_count['Time']
    pages = df_count['Pages'] 
    times_states = df_states['TIME']
    categories = [ df_states['TODO'], df_states['STARTED'], df_states['FIRST_DRAFT'], 
                  df_states['SECOND_DRAFT'], df_states['REVISIONS_DONE'], df_states['COMPLETE'] ]
    
    # Convert times to DateTime
    timesdf_count = get_times_as_date_time(times_count)
    timesdf_states = get_times_as_date_time(times_states)
    
    # Normalize each observation to total to 100%
    categories = normalize_categories(categories)
    
    # Get references to the figure and axes
    fig = plt.figure()
    ax = plt.gca()
    ax2 = ax.twinx()
    
    # Make a large graph
    fig.set_size_inches(20, 10)

    
    # Plot graph
    ax.stackplot(timesdf_states, categories, labels=['TODO', 'STARTED', 'FIRST_DRAFT', 'SECOND_DRAFT', 'REVISIONS_DONE', 'COMPLETE'], 
                  colors=COLOR_SET)
    ax.set_ylabel('% of categories')
    ax.yaxis.set_major_formatter(ticker.PercentFormatter())
    
    # Plot the times and counts
    ax2.plot(timesdf_count, pages, color=PAGES_COLOR)
    ax2.set_ylabel('pages', color=PAGES_COLOR)
    ax2.tick_params('y', colors=PAGES_COLOR)
    ax2.set_xlabel('date')
    
    # Y axis between 0 and 300 (limit for PhD thesis)
    ax2.set_ylim([0,250])
    
    ax.legend(loc=1, facecolor='white')
    
    
    if PLOT_DEADLINE:
        ax.axvline(x=datetime.strptime(DEADLINE, '%Y-%m-%d-%H%M%S'), linestyle='--', color='red')
    
    # Rotate x labels
    fig.autofmt_xdate()
    
    # Format the DateTime labels
    myFmt = mdates.DateFormatter('%Y-%m-%d')
    ax.xaxis.set_major_formatter(myFmt)
    ax.xaxis_date()
    
    plt.tight_layout()
    
    # Save the plot out
    plt.savefig(output_image)

    plt.close()
    
def normalize_categories(categories):
    # Count categories
    number_of_observations = len(categories[0])
    # for each observation
    
    # Convert categories to floats
    for index in range(0, len(categories)):
        categories[index] = categories[index].apply(float)
        
    totals_by_index = {}
    
    for index in range(0, number_of_observations):
        total = 0
        
        # for each category add the relevant observation to total
        for category in categories:
            total += category[index]
            
        totals_by_index[index] = total
        
    for cat_index, category in enumerate(categories):
        values = []
        for index, value in category.items():
            values.append(value * 100.0 / totals_by_index[index])
        categories[cat_index] = values
    
    return categories

def plot_simple_line_with_default_args():
    # Set seaborn style
    sns.set()
    matplotlib.use(MPL_BACKEND, warn=True)
    print('Matplotlib Backend ' + matplotlib.get_backend())
    
    plot_simple_line('page_count.csv','count.png')
    
def plot_combined_with_default_args():
    
    matplotlib.use(MPL_BACKEND, warn=True)
    print('Matplotlib Backend ' + matplotlib.get_backend())
    plot_combined('state.csv', 'page_count.csv', 'combined.png')
    
def plot_stacked_regions_with_default_args():
    # Set seaborn style
    sns.set()
    matplotlib.use(MPL_BACKEND, warn=True)
    print('Matplotlib Backend ' + matplotlib.get_backend())

    plot_stacked_regions('state.csv','state.png')    
    
if __name__ == '__main__':

    # once both are done, render both to a single plot too
    plot_combined_with_default_args()
    plot_simple_line_with_default_args()
    plot_stacked_regions_with_default_args()

    
