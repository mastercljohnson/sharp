# This is a script which takes in csv files of radiation dosage from specific
# examination and outputs basic statistics about these tests specific to each
# machine and each hospital

# Import libraries for manipulating data tables
import pandas as pd
import numpy as np
import matplotlib as mpl
import scipy
from scipy import stats
import xlsxwriter


class pediatric_general:

    # Initialize tables for different types of radiation values
    def __init__(self, file_path):
        self.maniparraydlp = np.array([])
        self.maniparrayctdi = np.array([])
        self.descriptarray = np.array([])
        self.medianarraydlp = np.array([])
        self.medianarrayctdi = np.array([])
        self.maxarraydlp = np.array([])
        self.maxarrayctdi = np.array([])
        self.minarraydlp = np.array([])
        self.minarrayctdi = np.array([])
        self.file_path = file_path

    # Load csv files data chosen from path into pandas table
    def sort(self):
        data = pd.read_csv(self.file_path, names =["MRN","A#","date","time",
                                          "proced","prot_name","prot"
                                          ,"Institution","equip","device",
                                          "CTDI_vol","dlp","103_ICRP"
                                          ])

        # Parse the values which contain 0 and are repeated
        inst = np.unique(data["Institution"].values)
        inst = np.delete(inst, 0)
        equip = np.unique(data["equip"].values)

        # Create a loop through the datatable which matches
        # institutions with their equipment
        # and outputs basic statistics for those equipment

        # Checks for each Institution
        for n in inst:
            nn = str(n)
            data_inst = data[data["Institution"].str.contains(nn)]
            # Match equipment inside institutions
            for p in equip:
                pp = str(p)
                data_equip = data_inst[data_inst["equip"].str.contains(pp)]

                DLP_ar = data_equip["dlp"]
                CTDI_ar = data_equip["CTDI_vol"]

                # Checks if the institution runs the specified test
                # Creates an empty file if nothing was found
                if data_equip.empty is False:
                    self.minarraydlp = np.append( self.minarraydlp
                                            , np.nanmin(DLP_ar.dropna().values))
                    self.minarrayctdi = np.append( self.minarrayctdi
                                        , np.nanmin(CTDI_ar.dropna().values))
                    self.maxarraydlp = np.append( self.maxarraydlp
                                        , np.nanmax(DLP_ar.dropna().values))
                    self.maxarrayctdi = np.append( self.maxarrayctdi
                                        , np.nanmax(CTDI_ar.dropna().values))
                    dlpp=pd.to_numeric(DLP_ar, errors='coerce')
                    ctdii=pd.to_numeric(CTDI_ar, errors='coerce')
                    self.medianarraydlp = np.append(self.medianarraydlp
                                                        , np.nanmedian(dlpp))
                    self.medianarrayctdi = np.append(self.medianarrayctdi
                                                        , np.nanmedian(ctdii))
                    o = nn+" "+pp
                    self.descriptarray = np.append( self.descriptarray, o)

        # If equipment was found for specific tests create a files
        # and compute statistics such as the mean, median , and standard deviation
        # etc. for each instituion and machine and output in an excel file
        strin= data["date"][1]
        strin = str(strin)
        print(strin)
        strin = strin.replace("/", "-")
        string = strin.split("-")[0]+'.xlsx'



        workbook = xlsxwriter.Workbook(string)
        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': True})
        worksheet.write('A1', 'device', bold)
        worksheet.write('B1', 'DLP Min', bold)
        worksheet.write('C1', 'DLP Median', bold)
        worksheet.write('D1', 'DLP Max', bold)
        worksheet.write('E1', 'CTDI Min', bold)
        worksheet.write('F1', 'CTDI Median', bold)
        worksheet.write('G1', 'CTDI Max', bold)
        row = 1
        worksheet.write_column(row, 0 , self.descriptarray)
        worksheet.write_column(row, 1 , self.minarraydlp)
        worksheet.write_column(row, 2 , self.medianarraydlp)
        worksheet.write_column(row, 3 , self.maxarraydlp)
        worksheet.write_column(row, 4 , self.minarrayctdi)
        worksheet.write_column(row, 5 , self.medianarrayctdi)
        worksheet.write_column(row, 6 , self.maxarrayctdi)
        workbook.close()
