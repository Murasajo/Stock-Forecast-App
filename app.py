import streamlit as st
from datetime import date
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly
from plotly import graph_objs as go


START = "2016-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

st.title('Stock Forecast App')

stocks_dict = {'GOOG': 'Google Alphabet Inc', 
          'KO': 'The Coca-Cola Company', 
          'AAPL': 'Apple Inc', 
          'AAL': 'American Airline Group Inc', 
          'MSFT': 'Microsoft Corporation', 
          'GME': 'GameStop Corp', 
          'TSLA': 'Tesla Inc', 
          'PEP': 'PepsiCo, Inc', 
          'ORCL': 'Oracle Corporation', 
          'AMZN': 'Amazon.com, Inc', 
          'BABA': 'Alibaba Group Holding Limited', 
          'BCS': 'Barclays PLC', 
          'HBIO': 'Harvard Bioscience, Inc',
          'QAT': 'iShares MSCI Qatar ETF'
          }

stocks = list(stocks_dict.values())
selected_company = st.selectbox('Select company for prediction', stocks)
# Get the ticker corresponding to the selected company
selected_ticker = [ticker for ticker, name in stocks_dict.items() if name == selected_company]

duration_years = st.slider('Years of prediction:', 1, 4)
period = duration_years * 365


def load_data():
    data = yf.download(selected_ticker, START, TODAY)
    data.reset_index(inplace=True)
    
    return data

data_load_mssg = st.text('Loading data...')
data = load_data()
data_load_mssg.text('Successfully loaded data!')

# Extracting the 'Raw data' by diplaying the first five
st.subheader('Raw data')
st.write(data.head())

# Visualize the raw data to see the trend
def plot_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="Stock_open"))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='Stock_close'))
    fig.layout.update(title_text='Time Series data with Rangeslider', xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)

plot_raw_data()

# Predict forecast for the stocks in the companies
df_train = data[['Date', 'Close']]
df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

model = Prophet()
model.fit(df_train)
future = model.make_future_dataframe(periods=period)
forecast = model.predict(future)

# Display and plot forecast
st.subheader('Forecasted Data')
st.write(forecast.head())

# Specifying the number of years to forecast
st.write(f'Forecast Chart for {duration_years} years')
fig1 = plot_plotly(model, forecast)
st.plotly_chart(fig1)

st.write("Forecast components")
fig2 = model.plot_components(forecast)
st.write(fig2)

