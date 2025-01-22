# -*- coding: utf-8 -*-
import sys  
import os  
from math import sqrt
from statistics    import stdev , mean 
from  .odb         import Odb 
from  .setting_env import TuneEnv  

# BASED ON THE PROGRAM ratio.F90  IN THE ORIGINAL VERSION  B. Strajnar 2010/10/26

class AverageRatios(object):
      def __init__(self,paths  =None ,
                      Nobs   =None ,
                      rednmc =None ,
                      so_pred=None ,
                      so_diag=None ,
                      sb_pred=None ,
                      sb_diag=None ,
                      lwrite =None
                      ):
          if paths != None: self.basedir= paths["BASEDIR"]
          if Nobs     != None:
             self.ptot    =  sum(Nobs)
             self.pt      =  Nobs[0]
             self.pbt     =  Nobs[1]
             self.pq      =  Nobs[2]
             self.pke     =  Nobs[3]
          if so_pred  != None:
             self.so_tp =so_pred[0]  
             self.so_btp=so_pred[1] 
             self.so_qp =so_pred[2] 
             self.so_kep=so_pred[3]  

          if so_diag  != None:
             self.so_td =so_diag[0]
             self.so_btd=so_diag[1]
             self.so_qd =so_diag[2]
             self.so_ked=so_diag[3]

          if sb_pred != None and sb_diag != None:
             self.sb_tp  =sb_pred[0]  ; self.sb_td =sb_diag[0]
             self.sb_qp  =sb_pred[1]  ; self.sb_qd =sb_diag[2]
             self.sb_kep =sb_pred[2]  ; self.sb_ked=sb_diag[3]
 
          self.rednmc=rednmc  
            
          self.rabso =9.9E-310
          self.lwrite=lwrite 
           
      def Write2File (self , varname , pname , value ):
          # OUT PATH ( BASEDIR/out)
          os.system( "mkdir -p "+ self.basedir+"/out" )
          file_=self.basedir+"/out/"+varname+"_"+pname
          
          outfile=open(file_  , "w" )
          if isinstance ( value , list):
             for i,j in enumerate (value):
                 outfile.write(  str(i+1)+"    "+str(j)+"\n")
             outfile.close()
          else:
             outfile.write(str(value) )

      def NotNone (self,item):
          if item != None:
             return True
          else:
             return False



      def ComputeRatios(self, pred , diag , rednmc,  target  ):
          #print( pred , diag , rednmc,  target  ) 
          if pred != self.rabso  and diag != self.rabso :
             if target   == "sigmao":
                ratio =diag/pred
                return ratio
             elif target == "sigmab":
                ratio =diag/(pred * float(rednmc))
                return ratio 
          else: 
             ratio =None 
             return ratio

      def RatioSo(self):
          """
          The averaged ratio is computed by weighted sum of 
          the ratio of each observation subset 
          roav=sqrt(roq**2*float(pq)/float(ptot)+rot**2*float(pt)/float(ptot)
                   robt**2*float(pbt)/float(ptot)+roke**2*float(pke)/float(ptot))

          """
          target="sigmao"
          rot = self.ComputeRatios( self.so_tp  , self.so_td   ,self.rednmc , target )          
          robt= self.ComputeRatios( self.so_btp , self.so_btd  ,self.rednmc , target )
          roq = self.ComputeRatios( self.so_qp  , self.so_qd   ,self.rednmc , target )
          roke= self.ComputeRatios( self.so_kep , self.so_ked  ,self.rednmc , target )

          rot , robt,roke, roq = 0,0,0,0
          #if robt == None:  robt=0.    # NO OBS FOR BRIGHTNESS T 
          #rrobt=0.0
          
          if self.NotNone(rot) :  
             rrot = rot**2* float(self.pt) /float(self.ptot)
          else:
             rot = self.rabso
             rrot= self.rabso

          if self.NotNone(robt):  
             rrobt = robt**2*float(self.pbt)/float(self.ptot)
          else:
             robt = self.rabso
             rrobt= self.rabso

          if self.NotNone(rot) :  
             rroq = roq**2* float(self.pq) /float(self.ptot)
          else:
             roq = self.rabso
             rroq= self.rabso

          if self.NotNone(rot) :  
             rroke= roke**2*float(self.pke)/float(self.ptot)
          else:
             roke  = self.rabso
             rroke = self.rabso

          roav = sqrt(  rroq +rrobt + rrot + rroke )     
          if self.lwrite==True:             
              lines= "ro_t   : "+str("%.4f" % rrot)  +"  |   Nobs_t   : "+str(int(self.pt))   +"\n" \
                     "ro_bt  : "+str("%.4f" % rrobt) +"  |   Nobs_bt  : "+str(int(self.pbt))  +"\n" \
                     "ro_q   : "+str("%.4f" % rroq)  +"  |   Nobs_q   : "+str(int(self.pq) )  +"\n" \
                     "ro_ke  : "+str("%.4f" % rroke) +"  |   Nobs_ke  : "+str(int(self.pke))  +"\n" \
                     "\n" \
                     "ro_avg : "+str("%.4f" % roav) +"  |   Nobs_tot : "+str(int(self.ptot)) +"\n"
              self.Write2File( "ratios" ,"so" , lines )
          return rot , robt , roq , roke ,roav 
 


      def RatioSb(self):
          """
               sb_*d: diagnosed  sigmab
               sb_*p: predefined sigmab
               rb*  : tuning ratio for sigmab  for each parameter 
               rbav : Average weighted ratio for sigmab  
               rb=sbd/(sbp*rednmc)
               rbav=sqrt(rbq**2*pq/ptot+rbt**2*pt/ptot+rbke**2*pke/ptot)
          """
          target="sigmab"
          rrbt, rrbq , rrbke =  0. ,0. ,0. 
          rbt  = self.ComputeRatios( self.sb_tp  , self.sb_td    ,self.rednmc , target )
          rbq  = self.ComputeRatios( self.sb_qp  , self.sb_qd    ,self.rednmc , target )
          rbke = self.ComputeRatios( self.sb_kep , self.sb_ked   ,self.rednmc , target )
          
          # AVERAGE 
          if self.NotNone(rbt)   :  
             rrbt =rbt**2 *(self.pt /self.ptot )
          else:
             rbt = self.rabso 
             rrbt= self.rabso 
             

          if self.NotNone(rbq)   :  
             rrbq =rbq**2 *(self.pq /self.ptot )
          else:
             rbq =self.rabso 
             rrbq=self.rabso 

          if self.NotNone(rbke)  :  
             rrbke=rbke**2*(self.pke/self.ptot )
          else:
             rbke =self.rabso 
             rrbke=self.rabso 

          rbav = sqrt( rrbt  + rrbq  + rrbke )
          if self.lwrite == True:
              lines= "rb_t   : "+str("%.4f" % rbt)  +"  |   Nobs_t   : "+str(int(self.pt))   +"\n" \
                     "rb_q   : "+str("%.4f" % rbq)  +"  |   Nobs_q   : "+str(int(self.pq) )  +"\n" \
                     "rb_ke  : "+str("%.4f" % rbke) +"  |   Nobs_ke  : "+str(int(self.pke))  +"\n" \
                     "\n" \
                     "rb_avg : "+str("%.4f" % rbav) +"  |   Nobs_tot : "+str(int(self.ptot)) +"\n"
              self.Write2File( "ratios" ,"sb" , lines )

          return  rbt , rbq , rbke , rbav
          
      def __class_getitem__(cls, item):
          return cls._get_child_dict()[item]
      @classmethod
      def _get_child_dict(cls):
          return {k: v for k, v in cls.__dict__.items() if not k.startswith('_')}

class Predef:
      """
      Class : 
            RETURN PREDEFINED SIGMAO for t,bt,q and ke 
            OVER THE CHOSEN PERIOD  
      """
      def __init__(self , paths , dates , lverb , lwrite):
          self.basedir=paths['BASEDIR']
          self.lverb  =lverb 
          self.lwrite =lwrite
          # INIT LISTS 
          self.psigma=[]     ;
          self.dates =dates  ;
          self.rabso =9.9E-310  ; # MISSING DATA           
          return None

     
      def NotNone (self,item):
          if item != None:
             return True
          else:
             return False

      def Write2File (self , varname , pname , value ):
          # OUT PATH ( BASEDIR/out)
          os.system( "mkdir -p "+ self.basedir+"/out" )
          file_=self.basedir+"/out/"+varname+"_"+pname

          outfile=open(file_  , "w")
          if isinstance ( value , list):
             for i,j in enumerate (value):
                 outfile.write(  str(i+1)+"    "+str(j)+"\n")
             outfile.close()
          else:
             outfile.write(str(value) )




      # RETURNED PARAM FROM ReadMandalay Method 
      def GetSigmaP(self , param):
          so_pred_dict={}
          means=[]         
          if   param=="t" :  idx=0
          elif param=="bt":  idx=1
          elif param=="q" :  idx=2
          elif param=="ke":  idx=3
          else:
               print("UNKOWN PARAMATER -->",param , " POSSIBLE PARAM SHORT NAME : t , bt , q and ke" )
               sys.exit ()
          for  dt in self.dates:
              if  self.NotNone(Odb.ReadMandalay (self.basedir, dt, "predef") ):
                  self.psigma=self.psigma + Odb.ReadMandalay (self.basedir, dt, "predef")[idx]
                  # GET MEAN FOR EACH DATE/TIME 
                  if len( self.psigma) != 0:
                     if   param == "t": 
                         so_pred_dict[dt]  = mean(self.psigma)
                     elif param == "bt": 
                         so_pred_dict[dt]  = mean(self.psigma)
                     elif param == "q" :
                         so_pred_dict[dt]  = mean(self.psigma)
                     elif param == "ke":
                         so_pred_dict[dt]  = mean(self.psigma)

                     means.append( dt+"    "+str( mean(self.psigma)) )
                  else:
                     if   param == "t":
                         so_pred_dict[dt]  = self.rabso
                     elif param == "bt":
                         so_pred_dict[dt]  = self.rabso
                     elif param == "q" :
                         so_pred_dict[dt]  = self.rabso
                     elif param == "ke":
                         so_pred_dict[dt]  = self.rabso

                     means.append( dt+"    "+"None")

          if self.lwrite == True:
             self.Write2File ("so_pred_means_vs_date" ,param , means  )
          if len(self.psigma) != 0:
             so_pred=sum( self.psigma)/len(self.psigma)
             if self.lwrite == True: self.Write2File ("so_pred_mean" ,param ,so_pred  )
          else:
             so_pred=self.rabso 
             if self.lwrite == True: self.Write2File ("so_pred_mean" ,param ,so_pred  )
          return so_pred , so_pred_dict




class Diag:
      """
      Class : 
            # RETURN SIGMAO AND SIGMAB DIAGNOSTICS OVER THE CHOSEN PERIOD 
            # ACCORDING TO THE METHOD : "obs differences"
            # METHOD : 
            #    HBH^T = d(b,a) * d(b,o)^T 
            #    R     = d(o,a) * d(b,o)^T

      """
      def __init__(self ,paths =None , 
                         dates =None , 
                         lverb =None , 
                         lwrite=None):
          if paths != None:  self.basedir=paths["BASEDIR"]
          if dates != None:  self.dates  =dates
          if lverb != None:  self.lverb  =lverb 
          if lwrite!= None:  self.lwrite =lwrite 

          # INIT LISTS 
          self.sigb  =[]    ;
          self.sigo  =[]    ;
          self.sigb_out=[]  ;
          self.sigo_out=[]  ;
          self.rabso =9.9E-310 ;  # MISSING DATA 
          return None  


      def Write2File (self , varname , pname , value ):
          # OUT PATH ( BASEDIR/out)
          os.system( "mkdir -p "+ self.basedir+"/out" )
          file_=self.basedir+"/out/"+varname+"_"+pname

          outfile=open(file_  , "w")
          if isinstance ( value , list):
             for i,j in enumerate (value):
                 outfile.write(  str(i+1)+"    "+str(j)+"\n")
             outfile.close()
          else:
             outfile.write(str(value) )


      def NotNone (self,item):
          if item != None:
             return True
          else:
             return False


      def ComputeSigmab(self,fg_dep , an_dep):
          s=0
          if self.NotNone(fg_dep) and len(fg_dep )!=0 and self.NotNone(an_dep) and len(an_dep) !=0:
             for i in range(len(fg_dep )): 
                  diff=fg_dep[i]-an_dep[i] 
                  s   =s+ diff  *fg_dep[i]
             sigmab=sqrt(s/len(fg_dep)) 
          else:
             sigmab=None 
          return sigmab 


      def ComputeSigmao(self,fg_dep , an_dep):
          s=0
          if self.NotNone(fg_dep) and len(fg_dep )!=0 and self.NotNone(an_dep) and len(an_dep) !=0:
             for i in range(len(fg_dep)): 
                 s=s + (fg_dep[i]*an_dep[i] )
             sigmao = sqrt( s/len(fg_dep))
             return sigmao
          else:
             sigmao=None  
             return sigmao 

      # 0 = t, 1=bt, 2=q, 3=ke  
      def GetSigmaD(self, param): 
          if param=="t" :  idx=0 ;
          if param=="bt":  idx=1 ;
          if param=="q" :  idx=2 ;
          if param=="ke":  idx=3 ;
          diag_so_dict={}
          diag_sb_dict={}  
          nobs =0
          ncase=[]
          fg=[]
          an=[]
          for  dt in self.dates:
               if self.NotNone(Odb.ReadMandalay (self.basedir ,dt, "fg_diag")):
                  fg = Odb.ReadMandalay (self.basedir ,dt, "fg_diag")[idx] 
                  ncase.append(len(fg ))
                  nobs=len(fg)   # THER IS THE SAME N OBS FOR FG AND AN
               if self.NotNone(Odb.ReadMandalay (self.basedir ,dt, "fg_diag")):
                  an = Odb.ReadMandalay (self.basedir ,dt, "an_diag")[idx]

               if len(fg) !=0 and len(an)!= 0: 
                  #print( fg , an  )
                  self.sigo.append(self.ComputeSigmao( fg, an ))   # OBSERVATIONS  
                  self.sigb.append(self.ComputeSigmab( fg, an ))   # FIRST GUESS 
                  if  param  =="t" : 
                     diag_so_dict[dt] = [fg,an]
                     diag_sb_dict[dt] = [fg,an]
                  elif param =="bt":
                     diag_so_dict[dt] = [fg,an]
                     diag_sb_dict[dt] = [fg,an]
                  elif param =="q" :
                     diag_so_dict[dt] = [fg,an]
                     diag_sb_dict[dt] = [fg,an]
                  elif param == "ke":
                     diag_so_dict[dt] = [fg,an]
                     diag_sb_dict[dt] = [fg,an]
                  else:
                     diag_so_dict[dt] = self.rabso
                     diag_sb_dict[dt] = self.rabso

#
                  if self.lwrite==True:
                     self.sigo_out.append(dt+"    "+str(self.ComputeSigmao( fg, an )) )
                     self.sigb_out.append(dt+"    "+str(self.ComputeSigmab( fg, an )) )

                    
               elif len(fg) ==0 and len(an)== 0:
                  self.sigo.append(self.rabso)
                  self.sigb.append(self.rabso)
                  
                  if self.lwrite ==True:
                     self.sigo_out.append(dt+"    "+"  None" )
                     self.sigb_out.append(dt+"    "+"  None" )
          if self.lwrite==True:
             self.Write2File("so_diag_vs_date", param , self.sigo_out)
             self.Write2File("sb_diag_vs_date", param , self.sigb_out)

          if len( self.sigo) !=0 and len(self.sigb ) !=0:             
             if self.lwrite==True:
                self.Write2File("so_diag_mean", param , mean(self.sigo))
                self.Write2File("sb_diag_mean", param , mean(self.sigb))
             return  mean(self.sigb) , mean(self.sigo),diag_sb_dict, diag_so_dict ,  sum(ncase)
          else:
             if self.lwrite==True:
                self.Write2File("so_diag_mean", param , self.rabso)
                self.Write2File("sb_diag_mean", param , self.rabso) 
             return self.rabso , self.rabso ,  self.rabso , self.rabso  , sum( ncase)



dict_rso={}
dict_rsb={}
                                
class RatiosByCycle:

    d=Diag(None,None ,None ,None)
    def __init__(self, PathDict,  cdtg, 
                       rednmc  ,  so_pred_d ,
                       so_diag_d, sb_pred_d , 
                       sb_diag_d  , Nobs, lverb, lwrite ):


#        Ratios.__init__(self )
        self.basedir = PathDict["BASEDIR"]
        self.cdtg    = cdtg
        self.ptot    =  sum(Nobs)
        self.pt      =  Nobs[0]
        self.pbt     =  Nobs[1]
        self.pq      =  Nobs[2]
        self.pke     =  Nobs[3]

        # SIGMA O/B PREDEF 
        self.so_tp   = so_pred_d[0]   # p=predefined 
        self.so_btp  = so_pred_d[1]
        self.so_qp   = so_pred_d[2]
        self.so_kep  = so_pred_d[3]
    
        self.sb_tp   = sb_pred_d[0]
        self.sb_qp   = sb_pred_d[1]
        self.sb_kep  = sb_pred_d[2]


        # SIGMA O/B DIAG
        self.so_td   = so_diag_d[0]   # d=diagnosed 
        self.so_btd  = so_diag_d[1]
        self.so_qd   = so_diag_d[2]
        self.so_ked  = so_diag_d[3]

        self.sb_td   = sb_diag_d[0]
        self.sb_btd  = sb_diag_d[1]
        self.sb_qd   = sb_diag_d[2]
        self.sb_ked  = sb_diag_d[3]

        
        self.rednmc  = rednmc     
        self.rabso =9.9E-310  ; # MISSING DATA

        self.rso=None
        self.rsb=None

        self.lwrite =lwrite
        self.lverb  =lverb 
        return None

    def Write2File (self , varname , pname , value , dt ):
        # OUT PATH ( BASEDIR/out)
        os.system( "mkdir -p "+ self.basedir+"/out" )
        file_=self.basedir+"/out/"+varname+"_"+pname

        outfile=open(file_  , "w" )
        if isinstance ( value , list):
           for i,j in enumerate (value):
               print( dt +"   "+  str(i+1)+"    "+str(j) )
               outfile.write(dt +"   "+  str(i+1)+"    "+str(j)+"\n")
            #outfile.close()
        else:
            outfile.write(str(value) )


    def NotNone (self, item):
        if item != None:
           return True
        else:
           return False 

    def CheckInstance(self, var):
        if isinstance( var , list ):
           return True
        else:
           return False 
    def CatchExcept(self, _dict, _key):
        lst=[]
        try:
           lst= _dict[_key]
           return lst
        except:
           KeyError
           return None 
      
    def ComputeRatios(self, pred , diag , rednmc,  target  ):
        if pred != self.rabso  and diag != self.rabso :
           if target   == "sigmao":
              ratio =diag/pred
              return ratio
           elif target == "sigmab":
              ratio =diag/(pred * float(rednmc))
              return ratio
           else:
              ratio =None
              return ratio

    def GetByDate(self):
        """
        Rso = sqrt( (roq**2 * pq /nobs  +rot**2*pt/nobs + 
                     robt**2*pbt/nobs + roke**2*pke/nobs  ) )
        """
        dict_rso={}
        dict_rsb={}

        for dt in self.cdtg:

            # NOBS FOR EACH OBS SUBSET 
            
            lst_tp   = self.CatchExcept(self.so_tp ,dt ) 
            lst_btp  = self.CatchExcept(self.so_btp,dt )  
            lst_qp   = self.CatchExcept(self.so_qp ,dt )  
            lst_kep  = self.CatchExcept(self.so_kep,dt )  

            if self.CheckInstance(lst_tp  ): self.pt =len(lst_tp  )
            if self.CheckInstance(lst_btp ): self.pbt=len(lst_btp )
            if self.CheckInstance(lst_qp  ): self.pq =len(lst_qp  )
            if self.CheckInstance(lst_kep ): self.pke=len(lst_kep )
  
            lst_td   = self.CatchExcept(self.so_td , dt  )
            lst_btd  = self.CatchExcept(self.so_btd, dt  )
            lst_qd   = self.CatchExcept(self.so_qd , dt  )
            lst_ked  = self.CatchExcept(self.so_ked, dt  )

                   
            #  SIGMA DIAG  BY DATE/CYCLE                             FG     , # AN 
            if self.NotNone(lst_td)  : 
               sigo_td = self.d.ComputeSigmao( lst_td [0] , lst_td [1] )
            else:
               sigo_td=self.rabso
            if self.NotNone(lst_btd) : 
               sigo_btd= self.d.ComputeSigmao( lst_btd[0] , lst_btd[1] )
            else:
               sigo_btd=self.rabso
            if self.NotNone(lst_qd)  : 
               sigo_qd = self.d.ComputeSigmao( lst_qd [0] , lst_qd [1] )
            else:
               sigo_qd = self.rabso
    
            if self.NotNone(lst_ked) : 
               sigo_ked= self.d.ComputeSigmao( lst_ked[0] , lst_ked[1] )
            else:
               sigo_ked= self.rabso 




            # SIGMA B DIAG BY DATE/CYCLE  
            if self.NotNone(lst_td)  :
               sigb_td = self.d.ComputeSigmab( lst_td [0] , lst_td [1] )
            else:
               sigb_td=self.rabso
            if self.NotNone(lst_btd) :
               sigb_btd= self.d.ComputeSigmab( lst_btd[0] , lst_btd[1] )
            else:
               sigb_btd=self.rabso
            if self.NotNone(lst_qd)  :
               sigb_qd = self.d.ComputeSigmab( lst_qd [0] , lst_qd [1] )
            else:
               sigb_qd = self.rabso

            if self.NotNone(lst_ked) :
               sigb_ked= self.d.ComputeSigmab( lst_ked[0] , lst_ked[1] )
            else:
               sigb_ked= self.rabso



            # OBS RATIOS FOR EACH DATA/CYCLE             
            target = "sigmao"
            rot, robt, roq, roke =0,0,0, 0
            try:
               rot = self.ComputeRatios( self.so_tp [dt]  , sigo_td   ,self.rednmc , target )
               robt= self.ComputeRatios( self.so_btp[dt]  , sigo_btd  ,self.rednmc , target )
               roq = self.ComputeRatios( self.so_qp [dt]  , sigo_qd   ,self.rednmc , target )
               roke= self.ComputeRatios( self.so_kep[dt]  , sigo_ked  ,self.rednmc , target )
            except:
               KeyError 
               print("No DATA FOR THE DATE:" , dt )
               # THE OBS WEIGHT IS ZERO IF NO OBS (CAN SET IT TO rabso , BUT WILL BE EVEN MULTIPLIED BY pt=0)
            if not self.NotNone(rot ): rot =0 ; pt =0
            if not self.NotNone(robt): robt=0 ; pbt=0
            if not self.NotNone(roq ): roq =0 ; qt =0
            if not self.NotNone(roke): roke=0 ; ket=0

            # Rso AVG 
            self.rso = sqrt( (rot**2 * self.pt /self.ptot  +robt**2* self.pbt/self.ptot + roq**2*self.pq/self.ptot + roke**2* self.pke/self.ptot  ) )
            #if self.lwrite ==True:
            self.Write2File( "ratio", "t" , rot , dt )


            

            # B RATIOS FOR EACH DATA/CYCLE
            target="sigmab"

            rbt  = self.ComputeRatios( self.sb_tp  , sigb_td    ,self.rednmc , target )
            rbq  = self.ComputeRatios( self.sb_qp  , sigb_qd    ,self.rednmc , target )
            rbke = self.ComputeRatios( self.sb_kep , sigb_ked   ,self.rednmc , target )

      
            # Rrb AVG 
            if not self.NotNone(rbt ): rbt =0 ; pt =0
            if not self.NotNone(rbq ): rbq =0 ; qt =0
            if not self.NotNone(rbke): rbke=0 ; ket=0

            self.rsb =sqrt (rbt**2 *(self.pt /self.ptot ) + rbq**2 *(self.pq /self.ptot ) + rbke**2*(self.pke/self.ptot ) )

            dict_rso[dt]= self.rso 
            dict_rsb[dt]= self.rsb

        return  dict_rso , dict_rsb 
