import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('medical_examination.csv')

# Add overweight column
df['overweight'] = (df['weight'] / np.square(df['height']/100) > 25).astype('int') 
#df.head(5)

# Normalize the data by making 0 always good and 1 always bad
df['gluc'] = (df['gluc'] != 1).astype('uint8')
df['cholesterol'] = (df['cholesterol'] != 1).astype('uint8')


# Use Seaborn's `catplot()` to display the value counts of categorical features in long format, segmented by the 'Cardio' column 
def draw_cardio_plot():
    columns = ['active','alco','cholesterol','gluc','overweight','smoke']
    df_cardio = pd.melt(df, id_vars=['cardio'], value_vars=columns)

    df_cardio = df_cardio.reset_index().groupby(['variable', 'cardio', 'value']).agg('count').rename(columns = {'index':'total'}).reset_index()

    fig = sns.catplot(x='variable', y='total', col='cardio', hue='value', data=df_cardio, kind='bar').fig
    
    fig.savefig('cardioplot.png')
    return fig

 
draw_cardio_plot()


# Clean data and create a correlation matrix with heatmap()
def draw_heat_map():
    df_heat = df [
         (df['ap_lo'] <= df['ap_hi'])
        &(df['height']>= df['height'].quantile(0.025))
        &(df['height']<= df['height'].quantile(0.975))
        &(df['weight']>=df['weight'].quantile(0.025))
        &(df['weight']<=df['weight'].quantile(0.975))]

    # Create the correlation matrix
    corr = df_heat.corr()

    # Create a mask for the upper triangle
    mask = np.triu(np.ones_like(corr))

    # Set up the matplotlib figure
    fig = plt.figure(figsize=(12,8))

    # Draw the heatmap with sns.heatmap
    sns.heatmap(corr, mask=mask, annot=True,
                fmt='.1f', center=0, vmin=-0.5, vmax=0.5)
    
    #Do not modify the next two lines 
    fig.savefig('heatmap.png')
    return fig

 
draw_heat_map()