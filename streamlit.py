import streamlit as st
import  time
import pandas as pd
import matplotlib.pyplot as plt

df=pd.read_csv("C:/Users/DELL/OneDrive/Desktop/Indian startup/startup_cleaned.csv")
df['date'] = pd.to_datetime(df['date'],errors='coerce')
df.head()
df.info()
# data cleaning
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
df['year']=df['date'].dt.year
df['month']= df['date'].dt.month

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def load_overall_analysis(df):
    st.title("Overall Analysis")

    # Total invested amount
    total = round(df['amount'].sum())
    
    # Max amount infused in a startup
    max_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    
    # Average ticket size
    avg_funding = df.groupby('startup')['amount'].sum().mean()
    
    # Total number of funded startups
    num_startups = df['startup'].nunique()

    # Create columns for displaying metrics
    col1, col2, col3, col4 = st.columns(4)

    # Displaying metrics in the Streamlit app
    with col1:
        st.metric('Total Investment', str(total) + ' Cr')
    
    with col2:
        st.metric('Max Investment', str(max_funding) + ' Cr')
    
    with col3:
        st.metric('Average Ticket Size', str(round(avg_funding)) + ' Cr')
    
    with col4:
        st.metric('Total Startups Funded', num_startups)

    # MOM Graph
    st.header("MOM Graph")
    selected_options = st.selectbox('Select type', ['Total', 'Count'])

    if selected_options == 'Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()

    temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')

    # Plotting the graph
    fig5, ax5 = plt.subplots(figsize=(10,6))
    ax5.plot(temp_df['x_axis'], temp_df['amount'], marker='o')
    ax5.set_xlabel('Month-Year')
    ax5.set_ylabel('Amount Invested')
    ax5.set_title('Month-over-Month Investment')
    plt.xticks(rotation=45,ha='right')
    ax5.set_xticks(ax5.get_xticks()[::12])
    ax5.grid(True, which='both', linestyle='--', linewidth=0.5)
    st.pyplot(fig5)

    # Sectoral Sum Pie Chart
    sectoral_sum = df.groupby('vertical')['amount'].sum().sort_values(ascending=False).head()
    st.subheader("Sector-Wise Investment Distribution")
    fig6, ax6 = plt.subplots()
    ax6.pie(sectoral_sum, labels=sectoral_sum.index, autopct='%1.1f%%', startangle=90)
    ax6.axis('equal')  # Equal aspect ratio ensures that pie chart is circular
    st.pyplot(fig6)

    # Sectoral Count Pie Chart
    sectoral_count = df.groupby('vertical')['amount'].count().sort_values(ascending=False).head()
    st.subheader("Sector-Wise Investment Count")
    fig7, ax7 = plt.subplots()
    ax7.pie(sectoral_count, labels=sectoral_count.index, autopct='%1.1f%%', startangle=90)
    ax7.axis('equal')
    st.pyplot(fig7)

    # Investment Round Analysis
    round_data = df.groupby('round')['amount'].sum().sort_values(ascending=False).head(10)
    selected_round = st.selectbox('Select Investment Round', round_data.index)

    filtered_df = df[df['round'] == selected_round]
    top_verticals = filtered_df.groupby('vertical')['amount'].sum().nlargest(5).reset_index()

    fig8, ax8 = plt.subplots()
    ax8.bar(top_verticals['vertical'], top_verticals['amount'])
    ax8.set_xlabel('Vertical')
    ax8.set_ylabel('Amount (INR)')
    ax8.set_title(f'Top 5 Verticals in {selected_round} Round')
    st.pyplot(fig8)

    # Top Investors
    st.subheader("Top Investors")
    top_investors = df.groupby('investors')['amount'].sum().sort_values(ascending=False).head()
    fig9, ax9 = plt.subplots()
    ax9.pie(top_investors, labels=top_investors.index, autopct='%0.01f%%')
    ax9.set_title('Top Investors')
    st.pyplot(fig9)

    # City-wise Funding
    df['city'] = df['city'].replace({
        'Bengaluru': 'Bangalore',
        'Gurgaon': 'Gurugram'
    })
    
    city_funding = df.groupby('city')['amount'].sum().sort_values(ascending=False).head(7)
    st.subheader("City-Wise Funding")
    
    fig10, ax10 = plt.subplots()
    bars = ax10.bar(city_funding.index, city_funding.values, color='skyblue', edgecolor='white')
    
    ax10.set_xlabel('City', fontsize=14)
    ax10.set_ylabel('Total Funding Amount (INR)', fontsize=14)
    ax10.set_title('City-wise Funding', fontsize=16)
    ax10.yaxis.grid(True)
    
    # Add data labels on top of the bars
    for bar in bars:
        yval = bar.get_height()
        ax10.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom')

    st.pyplot(fig10)

# Usage: call the function with your DataFrame
# load_overall_analysis(df)





# Sample DataFrame (replace this with your actual DataFrame)

# Function to load investor details
def load_investor_details(investor):
    st.title(investor)

    # Load the most recent 5 investments of the investor
    last5_df = df[df['investors'].str.contains(investor, na=False)][['date', 'startup', 'vertical', 'city', 'round', 'amount']].head()
    st.subheader('Most Recent Investments')
    st.dataframe(last5_df)

    # Display the biggest investments in a bar chart
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        # Get the biggest investments grouped by startup
        big_series = df[df['investors'].str.contains(investor, na=False)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        
        st.subheader('Biggest Investments')
        
        # Plotting a bar graph
        fig, ax = plt.subplots()
        ax.bar(big_series.index, big_series.values, color='skyblue', edgecolor='white')
        ax.set_ylabel('Investment Amount (INR)')
        ax.set_title(f"Top 5 Investments by {investor}")

        # Display the plot in Streamlit
        st.pyplot(fig)

    with col2:
        vertical_series = df[df['investors'].str.contains(investor, na=False)].groupby('vertical')['amount'].sum()
        st.subheader('Sectors Invested In')

        # Plotting a pie chart
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series, labels=vertical_series.index, autopct="%0.1f%%", startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie chart is circular.
        st.pyplot(fig1)

    with col3:
        stage_investments = df[df['investors'].str.contains(investor, na=False)].groupby('round')['amount'].sum()
        st.subheader("Stage of Investment")

        # Plotting a pie chart for stages
        fig2, ax2 = plt.subplots()
        ax2.pie(stage_investments, labels=stage_investments.index, autopct='%0.1f%%', startangle=90)
        ax2.axis('equal')
        st.pyplot(fig2)

    with col4:
        invest_places = df[df['investors'].str.contains(investor, na=False)].groupby('city')['amount'].sum()
        st.subheader('Cities for Investment')

        # Plotting a pie chart for cities
        fig3, ax3 = plt.subplots()
        ax3.pie(invest_places, labels=invest_places.index, autopct="%0.1f%%", startangle=90)
        ax3.axis('equal')
        st.pyplot(fig3)

    with col5:
        yearly_investments = df[df['investors'].str.contains(investor, na=False)].groupby('year')['amount'].sum()
        st.subheader('YOY Investment')

        # Plotting a line chart for yearly investments
        fig4, ax4 = plt.subplots()
        ax4.plot(yearly_investments.index, yearly_investments.values, marker='o', color='green')
        ax4.set_xlabel('Year')
        ax4.set_ylabel('Investment Amount (INR)')
        ax4.set_title('Year-over-Year Investments')
        st.pyplot(fig4)

# Usage: call the function with the investor's name
# load_investor_details("Investor Name")
       
df.info()
def load_startup_details(startup):
    st.title(startup)
    round_series = df[df['startup'].str.contains(startup, na=False)].groupby(['round','startup'])['amount'].sum()
    st.subheader("Round-wise Investment Summary")

# Define  colors for the pie chart
    colors = ['#FF9999', '#66B3FF', '#99FF99', '#FFCC99', '#FFD700']

    # Plot the pie chart with shadow and custom colors
    fig11, ax11 = plt.subplots()
    wedges, texts, autotexts = ax11.pie(
        round_series,
        labels=round_series.index,
        autopct='%1.1f%%',
        startangle=90,
        colors=colors,
        shadow=True,
        explode=[0.05] * len(round_series)  # Slightly explode all wedges
    )

    # Customize label styles
    for text in texts:
        text.set_fontsize(12)
        text.set_color('#4B0082')  # Indigo color for labels

    for autotext in autotexts:
        autotext.set_color('white')  # White color for percentage labels
        autotext.set_fontsize(10)

    # Ensure the pie chart is a circle
    ax11.axis('equal')

    # Display the pie chart in Streamlit
    st.pyplot(fig11)
 

# title
st.sidebar.title("Startup Funding Analysis")
# we are giving 3 options to the users 
options= st.sidebar.selectbox('Select one',['Overall Analysis','Startups','Investor'])

if options == 'Overall Analysis':
        load_overall_analysis(df)
        
elif options == 'Startups':
    # Selecting a startup
    startup = st.sidebar.selectbox('Select Startup', sorted(df["startup"].unique().tolist()))
    load_startup_details(startup)

   
else:
    selected_investor=st.sidebar.selectbox('Select Investors',sorted(set(df['investors'].str.split(',').sum())))
    btn2= st.sidebar.button("Find Investor details")
    load_investor_details(selected_investor)
  

# investor: multiple names so we need to concate the group of investors

# General analysis
round(df['amount'].sum())
