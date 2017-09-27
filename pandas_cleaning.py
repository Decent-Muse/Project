import pandas as pd
import datetime

file_location = 'new.csv'

df = pd.read_csv(file_location, sep='|', names=['BARCODE','CREATED_STAMP'])
barcode_size_corrected_df = df[(df['BARCODE'].str.len() == 12) | (df['BARCODE'].str.len() == 13) | (df['BARCODE'].str.len() == 8)]
no_capture_window = barcode_size_corrected_df[['BARCODE','CREATED_STAMP']]
barcode_pattern = '^[0-9]*$'
barcode_rectified = no_capture_window[no_capture_window['BARCODE'].str.contains(barcode_pattern)]
print(len(barcode_rectified.index))
print(barcode_rectified[:10])
barcode_rectified.to_csv('new2.csv', sep='|', index=False)
