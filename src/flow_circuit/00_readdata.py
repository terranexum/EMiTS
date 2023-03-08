import pandas as pd

incr = 1e-8

# Read in the sources file
sources_orig_df = pd.read_csv('sources.csv', header=1)

# Select the columns for plant name, latitude, longitude, MWh generated, and CO2e emitted
sources_df = sources_orig_df[['PNAME', 'LAT', 'LON', 'PLNGENAN', 'PLC2ERTA']]
sources_df = sources_df.rename(columns={'PNAME': 'Name', 'LAT': 'Latitude', 'LON': 'Longitude', 'PLNGENAN': 'Energy Generated (MWh)', 'PLC2ERTA': 'CO2e Emitted (metric tons)'})
sources_df['Energy Generated (MWh)'].fillna('1', inplace=True)
sources_df['Energy Generated (MWh)'] = sources_df['Energy Generated (MWh)'].str.replace(',', '')
sources_df['CO2e Emitted (metric tons)'].fillna('1', inplace=True)
sources_df['CO2e Emitted (metric tons)'] = sources_df['CO2e Emitted (metric tons)'].str.replace(',', '')
sources_df['Type'] = 'Energy Generator'
del sources_orig_df

# Read in the sinks file
sinks_orig_df = pd.read_csv('sinks.csv', header=0)

# Select the columns for the location ID, MWh generated, and CO2e emitted
sinks_df = sinks_orig_df[['Property Name', 'Building Id', 'Site Energy Use (Kbtu)', 'Total Ghg Emissions (Metric Tons Co2E)']]
sinks_df = sinks_df.rename(columns={'Property Name': 'Name', 'Building Id': 'Building ID', 'Site Energy Use (Kbtu)': 'Energy Consumed (KBtu)', 'Total Ghg Emissions (Metric Tons Co2E)': 'CO2e Emitted (metric tons)'})
sinks_df['Energy Consumed (KBtu)'].fillna(1, inplace=True)
sinks_df['CO2e Emitted (metric tons)'].fillna(1, inplace=True)
sinks_df['Type'] = 'Energy Consumer'
del sinks_orig_df

# Convert kBtu to MWh, insert as new column, delete old column
sinks_df['Energy Consumed (MWh)'] = sinks_df['Energy Consumed (KBtu)'].astype(float) * 0.000293071 # 1 kBtu = 0.000293071 MWh
del sinks_df['Energy Consumed (KBtu)']


# Add new calculated columns to the sources dataframe to get M (kg), S (m), E (J), and T (s) 
sources_df['M'] = sources_df['Energy Generated (MWh)'].astype(float) / 1000000 * 3600 # divided by 1000000 to get Wh, and multiplied by 3600 to get J
sources_df['S'] = incr
sources_df['E'] = sources_df['CO2e Emitted (metric tons)'].astype(float) * 2200000 * 3600 # 2200 kWh per metric ton for DAC, 3600 J in 1 Wh
sources_df['T'] = incr
del sources_df['Energy Generated (MWh)']
del sources_df['CO2e Emitted (metric tons)']


# Add new calculated columns to the sinks dataframe to get M (kg), S (m), E (J), and T (s) 
sinks_df['M'] = sinks_df['Energy Consumed (MWh)'].astype(float) / 1000000 * 3600 * -1 # divided by 1000000 to get Wh, and multiplied by 3600 to get J; negative 1 since it's a sink
sinks_df['S'] = incr
sinks_df['E'] = sinks_df['CO2e Emitted (metric tons)'].astype(float) * 2200000 * 3600 # 2200 kWh per metric ton for DAC, 3600 J in 1 Wh
sinks_df['T'] = incr
del sinks_df['Energy Consumed (MWh)']
del sinks_df['CO2e Emitted (metric tons)']


# Combine sources and sinks dataframes
combined_df = pd.concat([sources_df, sinks_df], ignore_index=True)

df_length = len(combined_df)
file_name = '../static/EMiTS_' + str(df_length) + '.csv'

# Save to a new CSV file
combined_df.to_csv(file_name, index=False)

'''
M (kg),S (km),E (kWh),T (h),EMiTS
20,10,0.5,1,200
15,5,0.3,2,30
10,15,0.7,3,70
25,20,1.0,4,400
5,7,0.4,1,14
30,10,0.6,2,180
20,5,0.5,3,50
15,15,0.8,4,120
10,7,0.3,1,21
25,20,1.2,2,600

'''