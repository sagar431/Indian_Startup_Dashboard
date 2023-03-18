import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout='wide',page_title='StartUp Analysis')

df=pd.read_csv('startup_cleaned.csv')
df['date'] = pd.to_datetime(df['date'],errors='coerce')
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

def load_overall_analysis():
    st.title('Overall Analysis')

    #total  invested amount
    total=round(df['amount'].sum())
    #max amount infused in a startup
    max_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    avg_funding = df.groupby('startup')['amount'].sum().mean()
    # total funded startups
    num_startups = df['startup'].nunique()

    col1,col2,col3,col4=st.columns(4)

    with col1:
        st.metric('Total',str(total)+' Cr')
    with col2:
        st.metric('Max', str(max_funding) + ' Cr')
    with col3:
        st.metric('Avg',str(round(avg_funding))+' cr')
    with col4:
        st.metric('Funded startup',num_startups)

    st.header('MoM graph')
    selected_option = st.selectbox('Select Type',['Total','Count'])
    if selected_option == 'Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()

    temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')

    fig3, ax3 = plt.subplots()
    ax3.plot(temp_df['x_axis'], temp_df['amount'])

    st.pyplot(fig3)

def load_investors_details(investors):
    st.title(investors)
    #load the recent 5 investment of the investor
    last5_df = df[df['investors'].str.contains(investors)].head()[
        ['date', 'startup', 'vertical', 'city', 'round', 'amount']]
    st.subheader('Most recent Inverstments ')
    st.dataframe(last5_df)

    col1,col2=st.columns(2)
    with col1:

        #biggest invesments
        # biggest investments
        big_series= df[df['investors'].str.contains(investors)].groupby('startup')['amount'].sum().sort_values(
            ascending=False).head()
        st.subheader('Biggest Investments')
        fig, ax = plt.subplots()
        ax.bar(big_series.index, big_series.values)

        st.pyplot(fig)

    with col2:
        verical_series = df[df['investors'].str.contains(investors)].groupby('vertical')['amount'].sum()

        st.subheader('Sectors invested in')
        fig1, ax1 = plt.subplots()
        ax1.pie(verical_series, labels=verical_series.index, autopct="%0.01f%%")

        st.pyplot(fig1)
    df['year'] = df['date'].dt.year
    year_series = df[df['investors'].str.contains(investors)].groupby('year')['amount'].sum()

    st.subheader('YoY Investment')
    fig2, ax2 = plt.subplots()
    ax2.plot(year_series.index, year_series.values)

    st.pyplot(fig2)


st.sidebar.title('Startup Funding Analysis')

option=st.sidebar.selectbox('Select one', ['Overall Analysis','Startup','Investor'])

if option=='Overall Analysis':
        load_overall_analysis()
elif option == 'Startup':
    st.sidebar.selectbox('Select Startup',sorted(df['startup'].unique().tolist()))
    st.title('Start up Analysis')
else:
    selected_investors=st.sidebar.selectbox('Select= Startup',sorted(set(df['investors'].str.split(',').sum())))
    btn2=st.sidebar.button('Find investors Details')
    if btn2:
        load_investors_details(selected_investors)


