import pandas as pd
import sys

file_location = sys.argv[1]

# reading the csv file '|' separated
df = pd.read_csv(file_location, sep='|', names=['POS_Application_Name','STOREID','MACID','BILLNO','BARCODE','GUID','CREATED_STAMP'])
#df = pd.read_csv(file_location, sep='|')

# correcting the barcode size
barcode_size_corrected_df = df[(df['BARCODE'].str.len() == 12) | (df['BARCODE'].str.len() == 13) | (df['BARCODE'].str.len() == 8)]

# removing columns that are not required
no_capture_window = barcode_size_corrected_df[['BARCODE','CREATED_STAMP']]

# extracting barcodes using regular expressions
barcode_pattern = '^[0-9]*$'
barcode_rectified = no_capture_window[no_capture_window['BARCODE'].str.contains(barcode_pattern)]

# converting barcodes to float
barcode_rectified.BARCODE = barcode_rectified.BARCODE.astype(str).astype(float)

#numpy array of barcodes
barcodes = pd.DataFrame.as_matrix(barcode_rectified['BARCODE'])

# converting created_stamp to datetime object
barcode_rectified['CREATED_STAMP'] = pd.to_datetime(barcode_rectified['CREATED_STAMP'], format='%Y-%m-%d %H:%M:%S')

# changing the date time format
barcode_rectified['CREATED_STAMP'] = barcode_rectified['CREATED_STAMP'].dt.strftime('%Y%m%d')

# converting date to float
barcode_rectified.CREATED_STAMP = barcode_rectified.CREATED_STAMP.astype(str).astype(float)

# numpy array of created dates
created_stamps = pd.DataFrame.as_matrix(barcode_rectified['CREATED_STAMP'])

print(len(barcode_rectified.index))
print(barcode_rectified[:10])
#barcode_rectified.to_csv('SOFT_GENv2.csv', sep='|', index=False)
