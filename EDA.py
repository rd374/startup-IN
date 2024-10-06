import  time
import pandas as pd

df=pd.read_csv("C:/Users/DELL/OneDrive/Desktop/SQL/archive/startup_funding.csv")
# data 
df.head()
df.info()
df.drop(columns=['Remarks'],inplace=True)
df.head()
df.set_index('Sr No',inplace=True)
df.rename(columns={
    'Date dd/mm/yyyy':'date',
    'Startup Name':'startup',
    'Industry Vertical':'vertical',
    'SubVertical':'subvertical',
    'City  Location':'city',
    'Investors Name':'investors',
    'InvestmentnType':'round',
    'Amount in USD':'amount'    
    
},inplace=True)
df.head()
df['amount'] = df['amount'].fillna('0')
df['amount'] = df['amount'].str.replace(',','')
df['amount'] = df['amount'].str.replace('undisclosed','0')
df['amount'] = df['amount'].str.replace('unknown','0')
df['amount'] = df['amount'].str.replace('Undisclosed','0')
df = df[df['amount'].str.isdigit()]
df['amount'] = df['amount'].astype('float')
df.info()
def to_inr(dollar):
    inr = dollar * 82.5
    return inr/10000000
df['amount'] = df['amount'].apply(to_inr)

df.head()
df['date'] = df['date'].str.replace('05/072018','05/07/2018')
df['date'] = pd.to_datetime(df['date'],errors='coerce')
df.head()
df.info()
df = df.dropna(subset=['date','startup','vertical','city','investors','round','amount'])
df.info()

df.head()
# 
df['investors']
# comma saperated
# Split the 'investors' column values by commas, creating lists of individual investors
# Then flatten these lists into one long list using sum()
# Finally, set() removes duplicates, leaving unique investors
sorted(set(df['investors'].str.split(',').sum()))
pd.set_option('display.max_columns', None)

# investors 
# users #ML #small letterrr---> distinct 
# Filter rows where the 'investors' column contains 'Mumbai Angels Network'
# Filter and select columns in one step, and store in a single variable
df[df['investors'].str.contains('Mumbai Angels Network', na=False)][['date', 'startup', 'vertical', 'city', 'round', 'amount']].head()

# Display the result

df[df['investors'].str.contains('IDG Ventures')].groupby('startup')['amount'].sum().sort_values(ascending=False)

df[df['investors'].str.contains('IDG Ventures')].groupby('vertical')['amount'].sum().plot(kind='pie')

df[df['investors'].str.contains('IDG Ventures')].groupby('round')['amount'].sum().plot(kind='pie')

df[df['investors'].str.contains('IDG Ventures')].groupby('city')['amount'].sum().plot(kind='pie')
df
df['year']=df['date'].dt.year
df.info()

df[df['investors'].str.contains('IDG Ventures')].groupby('year')['amount'].sum().plot()


df.to_csv(r'C:/Users/DELL/OneDrive/Desktop/SQL/startup_cleaned.csv', index=False)

df.groupby('startup')['amount'].max().sort_values(ascending=False)
round(df.groupby('startup')['amount'].sum().mean(),2)

df['month']= df['date'].dt.month
temp_df=df.groupby(['year','month'])['amount'].sum().reset_index()
temp_df['x_axis']=temp_df['month'].astype('str')+ '-'+ temp_df['year'].astype('str')
temp_df[['amount','x_axis']]


sectoral_sum =df.groupby('vertical')['amount'].sum().sort_values(ascending=False).head()
sectoral_sum

sectoral_count = df.groupby('vertical')['amount'].count().sort_values(ascending=False).head()
sectoral_count
df['round'].unique()

sorted(set(df['round'].str.split(',').sum()))
df.groupby('round')['amount'].sum().sort_values(ascending=False)
# top investors
df.groupby('investors')['amount'].sum().sort_values(ascending=False).head()

df.info()
city_top= df.groupby('city')['amount'].sum().sort_values(ascending=False).head(10)
df['city'].unique()
sorted(set(df['city'].str.split(',').sum()))
df['city'] = df['city'].replace({
    'Bengaluru': 'Bangalore'  # Replace 'Bengaluru' with 'Bangalore'
})
df['city'] = df['city'].replace({
    'Gurgaon': 'Gurugram'  # Replace 'Bengaluru' with 'Bangalore'
})
pd.set_option('display.max_rows', 10) 



sorted(set(df['startup'].str.split(',').sum()))


df.info()
df.groupby('startup')['vertical'].unique()

# Grouping by 'startup' and 'round' and summing the 'amount'
grouped_data = df.groupby(['startup', 'round'])['amount'].sum().reset_index()

# To filter only the head of the result
grouped_data

# Displaying the result

df[df['startup'].str.contains('paytm',na=False)[['vertical','subvertical']]]


round_series = df[df['startup'].str.contains('Paytm', na=False)].groupby(['round','startup'])['amount'].sum().sort_values(ascending=False)

round_series

vertical_series = df[df['startup'].str.contains('paytm', na=False, case=False)]['vertical']
vertical_series
total_amt = df[df('startup').str.contains('paytm',na=False).groupby('startup')['amount'].sum()]

