import pandas as pd
import numpy as np
import sys

file_location = "BUSYv1.csv"

# reading the csv file '|' separated
df = pd.read_csv(file_location, sep='|', names=['POS_Application_Name','STOREID','MACID','BILLNO','BARCODE','GUID','CREATED_STAMP','CAPTURED_WINDOW','UPDATE_STAMP'])
#df = pd.read_csv(file_location, sep='|')

# correcting the barcode size
barcode_size_corrected_df = df[(df['BARCODE'].str.len() == 12) | (df['BARCODE'].str.len() == 13) | (df['BARCODE'].str.len() == 8)]

# removing columns that are not required
no_capture_window = barcode_size_corrected_df[['POS_Application_Name','STOREID','MACID','BILLNO','BARCODE','GUID','CREATED_STAMP']]

# extracting barcodes using regular expressions
barcode_pattern = '^[0-9]*$'
barcode_rectified = no_capture_window[no_capture_window['BARCODE'].str.contains(barcode_pattern)]

# converting barcodes to float
# barcode_rectified.BARCODE = barcode_rectified.BARCODE.astype(str).astype(float)

# numpy array of barcodes
# barcodes = pd.DataFrame.as_matrix(barcode_rectified['BARCODE'])

# converting created_stamp to datetime object
barcode_rectified['CREATED_STAMP'] = pd.to_datetime(barcode_rectified['CREATED_STAMP'], format='%Y-%m-%d %H:%M:%S')

# changing the date time format
#barcode_rectified['CREATED_STAMP'] = barcode_rectified['CREATED_STAMP'].dt.strftime('%Y%m%d')

# converting date to float
#barcode_rectified.CREATED_STAMP = barcode_rectified.CREATED_STAMP.astype(str).astype(float)

# numpy array of created dates
# created_stamps = pd.DataFrame.as_matrix(barcode_rectified['CREATED_STAMP'])

# making a COPY for joins and other operations (just to change tha name)
busy_df = barcode_rectified.copy(deep=True)

# Loading the product master DataFrame
pm_df = pd.read_excel('ProductMaster404b8b3.xlsx', header = 0)

# Making the BARCODE as object (String)
busy_df.BARCODE = busy_df.BARCODE.astype('int')
# busy_df

# Joining the two DataFrames based on the barcodes and extracting only category_desc, subcategory_desc, brand_desc and basepack_desc
joined_df = busy_df.join(pm_df.set_index('BARCODE'), on='BARCODE', how='inner', sort=False)

# print(joined_df.BARCODE.dtype)
# print(busy_df.BARCODE.dtype)
# print(pm_df.BARCODE.dtype)

# Extracting only required columns
joined_df = joined_df[['BARCODE', 'CATEGORY_DESC', 'SUBCATEGORY_DESC', 'BRAND_DESC', 'BASEPACK', 'CREATED_STAMP']]

joined_df['CREATED_STAMP'] = joined_df['CREATED_STAMP'].apply(pd.datetools.normalize_date)

# Adding a column for week number
joined_df['WEEK_NUM'] = joined_df['CREATED_STAMP'].dt.week
# Use joined_df

no_of_weeks = 53;
joined_df_copy = joined_df.copy(deep=True)

with open('weekly_data.csv', 'w') as weekly_file:
    weekly_csv = csv.writer(weekly_file)
    for x in range(1,no_of_weeks):
        weekly_df = joined_df_copy.where(joined_df_copy.WEEK_NUM == x)
        weekly_data = weekly_df['CATEGORY_DESC'].tolist()
        weekly_data = [x for x in weekly_data if not((str(x)=='nan' or str(x)=='OTHERS'))]
        weekly_csv.writerow(weekly_data)

