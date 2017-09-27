import pandas as pd
import time


class Cleaning:

    dir_location = '/home/atin/programs/muse/test2/time_vs_barcode/'
    file_location = None
    file_name = None
    destination_file_location = None
    destination_file_name = None
    log_file_name = '_log_cleaning.txt'
    log_file = None

    data_frame = None
    no_capture_window = None
    barcode_size_rectified = None
    barcode_format = '^[0-9]*$'
    barcode_format_rectified = None

    def __init__(self, filename, destinationfilename):
        self.file_name = filename
        self.destination_file_name = destinationfilename
        self.file_location = self.dir_location + self.file_name
        self.destination_file_location = self.dir_location + self.destination_file_name

        self.log_file = open(self.dir_location + self.file_name + self.log_file_name, mode='a')
        self.log('NEW INITIALIZATION')
        self.read_csv_data()
        self.remove_capture_window()
        self.rectify_barcode_size()
        self.rectify_barcode_values()
        self.write_to_csv()

    def read_csv_data(self):
        self.data_frame = pd.read_csv(self.file_location, sep='|', names=['POS_Application_Name', 'STOREID', 'MACID', 'BILLNO', 'BARCODE', 'GUID', 'CREATED_STAMP', 'CAPTURED_WINDOW', 'UPDATE_STAMP'])
        self.log('CSV file:' + self.file_name + ' is read')
        return

    def remove_capture_window(self):
        self.no_capture_window = self.data_frame[['POS_Application_Name', 'STOREID', 'BARCODE', 'GUID', 'CREATED_STAMP']]
        self.log('Capture window removed')
        return

    def rectify_barcode_size(self):
        self.barcode_size_rectified = self.no_capture_window[(self.no_capture_window == 12) | (self.no_capture_window == 13) | (self.no_capture_window == 8)]
        self.log('Barcode size rectified')
        return

    def rectify_barcode_values(self):
        self.barcode_size_rectified = self.barcode_size_rectified.dropna(subset=['BARCODE'])
        self.barcode_format_rectified = self.barcode_size_rectified[self.barcode_size_rectified['BARCODE'].str.contains(self.barcode_format)]
        self.log('Barcode format rectified')
        return

    def get_barcodes(self):
        self.barcode_format_rectified.BARCODE = self.barcode_format_rectified.BARCODE.astype(str).astype(int)
        barcodes = pd.DataFrame.as_matrix(self.barcode_format_rectified['BARCODE'])
        self.log('Barcodes extracted.')
        return barcodes

    def get_created_stamp(self):
        self.barcode_format_rectified['CREATED_STAMP'] = pd.to_datetime(self.barcode_format_rectified['CREATED_STAMP'], format='%Y-%m-%d %H:%M:%S')
        self.barcode_format_rectified['CREATED_STAMP'] = self.barcode_format_rectified['CREATED_STAMP'].dt.strftime('%Y%m%d')
        created_stamps = pd.DataFrame.as_matrix(self.barcode_format_rectified['CREATED_STAMP'])
        self.log('Created Stamps extracted.')
        return created_stamps


    def write_to_csv(self):
        self.barcode_format_rectified.to_csv(self.destination_file_location, sep='|')
        return

    def get_current_time_stamp(self):
        return time.asctime(time.localtime(time.time()))

    def log(self, log_string):
        self.log_file.write(self.get_current_time_stamp() + '\t' + log_string + '\n')
        self.log_file.flush()
        return

def main():
    busy_cleaning = Cleaning('BUSY7246fb6.csv', 'BUSYvnew.csv')
    easy_cleaning = Cleaning('EASYSOL326dc49.csv', 'EASYSOLvnew.csv')
    marg_cleaning = Cleaning('MARGfc72cd7_pipe.csv', "MARGvnew.csv")
    retail_cleaning = Cleaning('RETAIL_EXPERe490dde.csv', 'RETAIL_EXPERvnew.csv')
    soft_cleaning = Cleaning('SOFT_GENd6661f5.csv', 'SOFT_GENvnew.csv')


if __name__ == '__main__':
    main()
