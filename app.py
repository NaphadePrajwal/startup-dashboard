import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re
import seaborn as sns

st.set_page_config(layout='wide',page_title='StartUp Analysis')

df = pd.read_csv('startup_cleaned.xls')
df['date'] = pd.to_datetime(df['date'],errors='coerce')
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month

# Clean 'startup' column
df['startup'] = df['startup'].str.lower().str.strip()

# Clean 'investors' column
df['investors'] = df['investors'].str.lower().str.strip()

# Common startup name variations
startup_replacements = {
    'flipkart.com': 'flipkart',
    'flipkart pvt ltd': 'flipkart',
    'ola cabs': 'ola',
    'olacabs': 'ola',
    'oyo rooms': 'oyo',
    'oyo': 'oyo',
    'paytm marketplace': 'paytm',
    'one97': 'paytm',
    'zomato media': 'zomato',
    'zomato.com': 'zomato',
    'snapdeal.com': 'snapdeal',
    'housing.com': 'housing',
    'redbus.in': 'redbus',
    'inmobi': 'inmobi',
    'urbanclap': 'urban company',
    'urban company pvt ltd': 'urban company'
}

# Common investor name variations
investor_replacements = {
    'sequoia capital india': 'sequoia',
    'sequoia capital': 'sequoia',
    'accel partners': 'accel',
    'accel india': 'accel',
    'softbank group': 'softbank',
    'softbank corp': 'softbank',
    'matrix partners india': 'matrix partners',
    'kalari capital': 'kalari',
    'tiger global management': 'tiger global',
    'blume ventures india': 'blume ventures',
    'blume ventures': 'blume ventures',
    'samsung ventures': 'samsung',
    'alibaba group': 'alibaba',
    'google capital': 'google ventures',
    'google ventures': 'google ventures'
}

# Replace using the dictionaries
df['startup'] = df['startup'].replace(startup_replacements)
df['investors'] = df['investors'].replace(investor_replacements)


# Remove unnecessary punctuations or extra spaces
df['startup'] = df['startup'].apply(lambda x: re.sub(r'[^\w\s]', '', x))
df['investors'] = df['investors'].apply(lambda x: re.sub(r'[^\w\s,]', '', x))  # keep commas for splitting



def load_overall_analysis():
    st.title('Overall Analysis')

    # total Invested amount
    total = round(df['amount'].sum())



    # max amount ind=fused in startup
    max_funding = df.groupby('startup')['amount'].max().sort_values(ascending = False).head(1).values[0]

    # avg ticket size
    avg_funding = df.groupby('startup')['amount'].sum().mean()

    #total funded startups
    num_startups = df['startup'].nunique()

    col1,col2,col3,col4 = st.columns(4)
    with col1:
        st.metric('Total Funding', str(total) + ' Cr')
    with col2:
        st.metric('Max Funding', str(max_funding) + ' Cr')
    with col3:
        st.metric('Avg Funding', str(round(avg_funding)) + ' Cr')
    with col4:
        st.metric('Funded Startups',num_startups)

    st.header('MoM graph')
    selected_option = st.selectbox('Select Type',['Total','Count'])
    if selected_option == 'Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()


    temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')

    fig3, ax3 = plt.subplots(figsize=(12, 5))  # wider figure
    ax3.plot(temp_df['x_axis'], temp_df['amount'], marker='o')

    ax3.set_xlabel("Month-Year")
    ax3.set_ylabel("Amount")
    ax3.set_title("Month-on-Month Funding Trend")

    plt.xticks(rotation=45, ha='right')  # Rotate labels
    plt.tight_layout()  # Adjust layout to prevent clipping
    st.pyplot(fig3)


def sector_analysis():
    st.subheader('Sector Analysis')

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🔹 By Investment Count")
        count_series = df['vertical'].value_counts().head(10)
        fig1, ax1 = plt.subplots()
        ax1.pie(count_series, labels=count_series.index, autopct="%0.1f%%")
        st.pyplot(fig1)

    with col2:
        st.markdown("#### 🔹 By Investment Amount")
        sum_series = df.groupby('vertical')['amount'].sum().sort_values(ascending=False).head(10)
        fig2, ax2 = plt.subplots()
        ax2.pie(sum_series, labels=sum_series.index, autopct="%0.1f%%")
        st.pyplot(fig2)

def funding_type_analysis():
    st.subheader("Type of Funding")

    type_series = df['round'].value_counts()
    fig, ax = plt.subplots()
    ax.pie(type_series, labels=type_series.index, autopct='%0.1f%%')
    st.pyplot(fig)

def city_wise_funding():
    st.subheader("City-wise Total Funding (Top 10)")

    city_series = df.groupby('city')['amount'].sum().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots()
    ax.bar(city_series.index, city_series.values, color='teal')
    plt.xticks(rotation=45)
    st.pyplot(fig)

def top_startups():
    st.subheader("Top Funded Startups")

    tab1, tab2 = st.tabs(['Overall', 'Year-wise'])

    with tab1:
        top_df = df.groupby('startup')['amount'].sum().sort_values(ascending=False).head(10)
        st.bar_chart(top_df)

    with tab2:
        years = sorted(df['year'].dropna().unique())
        selected_year = st.selectbox('Select Year', years)
        temp_df = df[df['year'] == selected_year]
        top_year_df = temp_df.groupby('startup')['amount'].sum().sort_values(ascending=False).head(10)
        st.bar_chart(top_year_df)

def top_investors():
    st.subheader("Top Investors (by Total Funding)")

    investor_dict = {}
    for index, row in df.iterrows():
        if pd.notnull(row['investors']):
            investors = str(row['investors']).split(',')
            for inv in investors:
                inv = inv.strip()
                investor_dict[inv] = investor_dict.get(inv, 0) + row['amount']

    investor_df = pd.DataFrame(sorted(investor_dict.items(), key=lambda x: x[1], reverse=True)[:10],
                               columns=['Investor', 'Total Funding'])
    st.dataframe(investor_df)




def funding_heatmap():
    st.subheader("Funding Heatmap (Year vs Month)")

    heatmap_data = df.pivot_table(index='month', columns='year', values='amount', aggfunc='sum', fill_value=0)

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.heatmap(heatmap_data, annot=True, fmt='.0f', cmap='YlGnBu', linewidths=.5, ax=ax)
    st.pyplot(fig)

def load_startup_details(startup_name):
    st.title(startup_name.title())

    # Filter the selected startup
    startup_df = df[df['startup'] == startup_name]

    if startup_df.empty:
        st.warning("No data found for the selected startup.")
        return

    # Get most recent record for metadata
    latest = startup_df.sort_values(by='date', ascending=False).iloc[0]

    # Show basic info
    st.subheader("📄 Basic Details")
    st.write(f"**Name**: {latest['startup'].title()}")
    st.write(f"**Location**: {latest['city'].title() if pd.notnull(latest['city']) else 'N/A'}")
    st.write(f"**Industry**: {latest['vertical'].title() if pd.notnull(latest['vertical']) else 'N/A'}")
    st.write(f"**Subindustry**: {latest['subvertical'].title() if pd.notnull(latest['subvertical']) else 'N/A'}")


    st.subheader("💰 Funding Summary")

    total_funding = int(startup_df['amount'].sum())
    st.write(f"**Total Funding**: ₹ {total_funding:,} Cr")

    funding_rounds = startup_df['round'].unique()
    st.write(f"**Funding Rounds**: {', '.join(funding_rounds)}")

    st.write(f"**Latest Funding Date**: {latest['date'].date()}")

    st.write(f"**Investors**: {', '.join(startup_df['investors'].dropna().unique())}")

    st.subheader("📌 Recent Funding Entries")
    st.dataframe(startup_df[['date', 'round', 'amount', 'investors']].sort_values(by='date', ascending=False).head(5))

    # --- SIMILAR STARTUPS ---
    st.subheader("🧠 Similar Startups (by Industry/Subindustry)")
    industry = latest['vertical']
    subindustry = latest['subvertical']

    sim_startups = df[
        ((df['vertical'] == industry) | (df['subvertical'] == subindustry)) &
        (df['startup'] != startup_name)
    ]['startup'].value_counts().head(5).index.tolist()

    if sim_startups:
        st.write(", ".join([s.title() for s in sim_startups]))
    else:
        st.write("No similar companies found.")


def load_investor_details(investor):
    st.title(investor)
    # load the recent 5 investment of the investor
    last5_df = df[df['investors'].str.contains(investor)].head()[['date', 'startup', 'vertical', 'city', 'round', 'amount']]
    st.subheader('Most Recent Investments')
    st.dataframe(last5_df)

    col1, col2 = st.columns(2)
    with col1:
        # biggest investments
        big_series = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest Investments')
        fig, ax = plt.subplots()
        ax.bar(big_series.index, big_series.values)

        st.pyplot(fig)

    with col2:
        vertical_series = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
        st.subheader('Sectors Invested In')
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series,labels = vertical_series.index,autopct="%0.01f%%")

        st.pyplot(fig1)

    col3, col4 = st.columns(2)
    with col3:
        round_series = df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum()
        st.subheader('Round Invested')
        fig2, ax2 = plt.subplots()
        ax2.pie(round_series, labels=round_series.index, autopct="%0.01f%%")

        st.pyplot(fig2)

    with col4:
        city_series = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum()
        st.subheader('Most Invested City')
        fig3, ax3 = plt.subplots()
        ax3.pie(city_series, labels=city_series.index, autopct="%0.01f%%")

        st.pyplot(fig3)


    year_series = df[df['investors'].str.contains(investor )].groupby('year')['amount'].sum()

    st.subheader('YoY Investment')
    fig4, ax4 = plt.subplots()
    ax4.plot(year_series.index, year_series.values)

    st.pyplot(fig4)


    # --- SIMILAR INVESTORS SECTION ---
    st.subheader('Similar Investors (based on common startups)')

    # Get startups invested by selected investor
    startups_invested = df[df['investors'].str.contains(investor, na=False)]['startup'].unique()

    # Dictionary to count shared startups
    similarity_dict = {}

    for index, row in df.iterrows():
        current_investors = str(row['investors']).split(',')
        current_startup = row['startup']

        # Skip if not a common startup
        if current_startup not in startups_invested:
            continue

        for inv in current_investors:
            inv = inv.strip()
            if inv != investor:
                similarity_dict[inv] = similarity_dict.get(inv, 0) + 1

    # Convert to DataFrame
    sim_df = pd.DataFrame(similarity_dict.items(), columns=['Investor', 'Common Startups'])
    sim_df = sim_df.sort_values(by='Common Startups', ascending=False).head(5)

    st.dataframe(sim_df)


st.sidebar.title('Startup Funding Analysis')

option = st.sidebar.selectbox('Select One',['Overall Analysis','StartUp','Investor'])

if option == 'Overall Analysis':
    load_overall_analysis()
    sector_analysis()
    funding_type_analysis()
    city_wise_funding()
    top_startups()
    top_investors()
    funding_heatmap()

elif option == 'StartUp':
    selected_startup = st.sidebar.selectbox('Select StartUp', sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find StartUp Details')

    if btn1:
        load_startup_details(selected_startup)

else:
    selected_investor = st.sidebar.selectbox('Select StartUp',sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor Details')

    if btn2:
        load_investor_details(selected_investor)
