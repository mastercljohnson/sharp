import pandas as pd
import numpy as np
import matplotlib as mpl

    #import tkinter as tk
    #from tkinter import filedialog
import scipy
from scipy import stats

import xlsxwriter


class pediatric_general:

   

#root = tk.Tk()
#root.withdraw()
#file_path = filedialog.askopenfilename()


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

    

        


    
    def sort(self):
        



        data = pd.read_csv(self.file_path, names =["MRN","A#","date","time",
                                          "proced","prot_name","prot","Institution","equip","device",
                                          "CTDI_vol","dlp","103_ICRP"
                                          ])
#print(data["Institution"])
        #inst = data["Institution"]
        #["SGH","SMH","SCVMC","SRS","SCO","SCVIC", "SGH GMT", "SMH OPP"]
        
        inst = np.unique(data["Institution"].values)
        inst = np.delete(inst, 0)
        print(inst)
#dev = ["Aquilion","BrightSpeed","LightSpeed Ultra","LightSpeed VCT", "LightSpeed16"]
        equip = np.unique(data["equip"].values)

        


        a=0


        for n in inst:
            nn = str(n)
            data_inst = data[data["Institution"].str.contains(nn)]
            for p in equip:
                pp = str(p)
                data_equip = data_inst[data_inst["equip"].str.contains(pp)]

                DLP_ar = data_equip["dlp"]
                CTDI_ar = data_equip["CTDI_vol"]
        


        

        
    #r=pd.DataFrame(data_inst,columns = ["MRN", "DOB", "Gender", "Weight", "Height", "A#","Description", "Date_Performed", "Time_Performed",
                                      #"Institution","equipment","device","Scan_Region","Images",
                                      #"does_sheet","eye_ct","eye_total","103_ICRP",
                                      #"ov_ct","ov_nm","ov_tot","remainderircp","test_tot", "ut_ct",
                                      #"ut_tot"])
                if data_equip.empty is False:
                #print('m')
                #print(descriptarray)
                #print(DLP_ar.values)
                    self.minarraydlp = np.append( self.minarraydlp , np.nanmin(DLP_ar.dropna().values))
                    self.minarrayctdi = np.append( self.minarrayctdi , np.nanmin(CTDI_ar.dropna().values))
                    self.maxarraydlp = np.append( self.maxarraydlp , np.nanmax(DLP_ar.dropna().values))
                    self.maxarrayctdi = np.append( self.maxarrayctdi , np.nanmax(CTDI_ar.dropna().values))
                    dlpp=pd.to_numeric(DLP_ar, errors='coerce')
                    ctdii=pd.to_numeric(CTDI_ar, errors='coerce')
                    self.medianarraydlp = np.append(self.medianarraydlp , np.nanmedian(dlpp))
                    self.medianarrayctdi = np.append(self.medianarrayctdi , np.nanmedian(ctdii))
                    o = nn+" "+pp
                    self.descriptarray = np.append( self.descriptarray, o)

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
    
    
    

        
            

            #print(data_dev)
            #print(data_dev["dlp"])
        #try:
           # print(nn+pp+"dlp")
           # print(mini(data_dev["dlp"]))
           # print( median(data_dev,"dlp"))
           # print( maxi(data_dev["dlp"]))
           # print(nn+pp+"icrp103")
           # print(mini(data_dev["103_ICRP"]))
           # print( median(data_dev,"103_ICRP"))
           # print( maxi(data_dev["103_ICRP"]))
        #except ValueError:
          #  print('skip '+nn+pp)
    #r.to_csv(o)
    #print(r)
