# -*- coding: utf8 -*-
import sys 
import matplotlib.pyplot as plt 
from matplotlib.dates import DateFormatter, DayLocator, HourLocator
import matplotlib.dates  as mdates 
from   datetime import datetime  
from collections import OrderedDict
import pytz 


class RatioPlotter:
      def __init__(self, paths=None , 
                         dates=None ,
                         lplot=None , 
                         lverb=None ,
                         rso_dict=None, 
                         rsb_dict=None ):

          self.path =  paths
          self.dates=  dates
          self.rsb  =  rso_dict      # Dict
          self.rso  =  rsb_dict      # Dict 
          self.lplot=  lplot 
          self.lverb=  lverb  
          return None

      def InitPlot (self):
          fig, ax = plt.subplots( figsize=(10,8) )
          tz = pytz.timezone('Europe/Paris')
          return ax 

      def PlotByDay(self):
          # TOD O FORMAT DT TICKS !!!!

          dt=[]
          sorted_rso = OrderedDict(sorted(self.rso.items()))
          for k in sorted_rso.keys():
              dtk=datetime.strptime(k, "%Y%m%d%H")
              dt.append( dtk )
          rso=[ self.rso[xd] for xd in  self.dates ]
          rsb=[ self.rsb[xd] for xd in  self.dates ]

          ax=self.InitPlot()

          ax.plot_date(  dt , rso  , label="r_o" , xdate=True, ls="-")
          ax.plot_date(  dt , rsb  , label="r_b" , xdate=True, ls="-")
          locator = mdates.AutoDateLocator()
          formatter = mdates.ConciseDateFormatter(locator)
          ax.xaxis.set_major_locator(locator)
          ax.xaxis.set_major_formatter(formatter)
          plt.show()
          

      def PlotByHour(self,   hlist ):
          self.hh= sorted(hlist )
          print( self.hh )
          rro=[ro00:=[],ro06:=[],ro12:=[],ro18:=[]]
          rrb=[rb00:=[],rb06:=[],rb12:=[],rb18:=[]]
          rdt=[dt00:=[],dt06:=[],dt12:=[],dt18:=[]]

          for i  in range(len( list( self.rso.keys()))):
             xt=list(self.rso.keys())[i]
             dtk=datetime.strptime(xt , "%Y%m%d%H")
             if   dtk.hour == 0:
                  dt00.append(xt) 
                  ro00.append(self.rso[xt] )
                  rb00.append(self.rsb[xt] )
             elif dtk.hour == 6:
                  dt06.append(xt) ;
                  ro06.append(self.rso[xt] )
                  rb06.append(self.rsb[xt] )
             elif dtk.hour == 12:
                  dt12.append(xt) 
                  ro12.append(self.rso[xt] )
                  rb12.append(self.rsb[xt] )
             elif dtk.hour == 18:
                  dt18.append(xt) ;
                  ro18.append(self.rso[xt] )
                  rb18.append(self.rsb[xt] )
             else:
                  print("Hour not in list of cycles " )
                  pass 
          ax, ttz =self.InitPlot()
          # TOD O : 
          # INTO A LOOP !
          plt.plot(rdt[0] ,  rro[0] )
          plt.plot(rdt[0] ,  rrb[0] )
          #plt.show()




