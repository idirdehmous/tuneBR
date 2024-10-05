# -*- coding: utf8 -*-
import sys 
import matplotlib.pyplot as plt 
from matplotlib.dates import DateFormatter, DayLocator, HourLocator
import matplotlib.dates  as mdates 
from   datetime import datetime  , timedelta 
from collections import OrderedDict
import pytz 


class RatioPlotter:
      def __init__(self, paths=None , 
                         dates=None ,
                         rso_dict=None,
                         rsb_dict=None,
                         lverb=None , 
                         lplot     =None ,
                         dates_range=None,
                         hours      =None ):

          self.path =  paths
          self.dates=  dates
#          self.inc  =  cycle_inc 
          self.rsb  =  rso_dict      # Dict
          self.rso  =  rsb_dict      # Dict 
          self.lplot=  lplot 
          self.lverb=  lverb  
          return None

      def InitPlot (self):
          fig, ax = plt.subplots( figsize=(10,8), dpi=250 )
          
          return ax 


      """def DateList (self, dt_range , cycle_inc):
             Create DATE LIST FOR DATE RANGEP  PLOT
          self.inc=cycle_inc  
          self.dt1=dt_range[0]
          self.dt2=dt_range[1]
          bdate=self.dt1
          edate=self.dt2
        
          dtlist=[]
          bdt =datetime.strptime( str(bdate) , "%Y%m%d%H")
          edt =datetime.strptime( str(edate) , "%Y%m%d%H")
          
          delta =timedelta(hours=int(cycle_inc))
          print( bdt , edt )
          if bdt != edt:
             print( "True")  

          while bdt <= edt :
                print( "heree" )
                strdate=bdate.strftime("%Y%m%d%H")
                print( strdate)
                dtlist.append( strdate )
                bdate += delta
          return dtlist"""
 


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


          ax.plot_date(  dt , rso  , label="r_o" , xdate=True, ls="-", lw=1.5 ,color="green", markersize=5)
          ax.plot_date(  dt , rsb  , label="r_b" , xdate=True, ls="-", lw=1.5 ,color="red"  , markersize=5)
          plt.title( "Tuning ratios for "+str(len(dt))+" days period" )
          locator = mdates.AutoDateLocator()
          formatter = mdates.ConciseDateFormatter(locator)
          ax.xaxis.set_major_locator(locator)
          ax.xaxis.set_major_formatter(formatter)
          plt.xlabel("Dates")
          plt.ylabel("Ratio")
#          plt.xlim(0,2.5)
          plt.legend()

          plt.show()
          

      def PlotByHour(self, dt_range  ,   hlist=[0,6,12,18]):
          dt=dt_range
          if hlist !=None and isinstance ( hlist, list ):
             self.hh= sorted(hlist )
          else:
             print( "List of hours to plot must be a list of integers [0,12,...]" )
             sys.exit()
          rro=[ro00:=[],ro06:=[],ro12:=[],ro18:=[]]
          rrb=[rb00:=[],rb06:=[],rb12:=[],rb18:=[]]
          rdt=[dt00:=[],dt06:=[],dt12:=[],dt18:=[]]

          """
          Todo : Add  DATE RANGE  LIST
          if not None and  isinstance (dt_range, tuple ):    
             if not isinstance (dt_range[0], int )  or not isinstance(dt_range[1], int):
                print( "Dates range must be a tuple of integers ")
                sys.exit()
             else:
                #selected_dates= self.DateList( dt_range , 3  )
                #print( selected_dates )
                print ( "Selected date range to plot " , selected_dates )

          else:
             print( dt_range , "variable must be a tuple " )
             sys.exit()
          if not isinstance (dt_range, tuple ) or dt_range==None:
             selected_dates=list( self.rso.keys())

          print( selected_dates)"""


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
                  # IT WILL CORRESPOND TO MISSING DATE OT INTERMEDIATE CYCLES 
                  # PLOT MAIN CYCLES ONLY !
                  pass 
          ax=self.InitPlot()
          for i in range(len(rdt)):            
              plt.plot(rdt[i] ,  rro[i], "-o" , color="green" ,label="ratio_o" , lw=1.5 )
              plt.plot(rdt[i] ,  rrb[i], "-o" , color="blue"  ,label="ratio_b" , lw=1.5 )
              plt.xlabel("cycle dates/time")
              plt.ylabel("Ratio")


              plt.legend()
              plt.show()




