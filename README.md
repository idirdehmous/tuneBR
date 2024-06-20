""
This package is a "pure python" re-implementation of   an 
existing tool ( tuneBR ) which has been already developed 
by the RC-LACE colleagues Benedikt Strajnar &  Gergely Boloni 
( shared on RC-LACE forum 12/2010 )
It was a mixed of bash/fortran code which is "translated" to 
python classes (OOP approach)

It's an  "easy and quick" application of a' posteriori diagnosis
and tuning for B and R variances and based on the method of
"covariance of residuals in observation space

proposed by Desroziers et al (2005), see below:
https://rmets.onlinelibrary.wiley.com/doi/pdf/10.1256/qj.05.108
"""




GENERAL INFO :
MODULE NAME         : tuneBR 
USED LANGUAGE       : fortran/python 
NEEDS INSTALLATION  : NO 
NEEDS COMPILATION   : YES 
DEPENDECIES         : gfortran 
                    : python3.8.x  or HIGHER
                    : cmake 3.20.x or HIGHER   


HOW IT WORKS  ? 

I-)  IF IT'S  BUILD  USING CMAKE, ONE HAS ONLY TO MERGE THE BOTH
     CMAKE FILES WITH THE ONE OF AccordDaTools !
     SEE THE FUTURE README OF AccordDaTools REPOSITORY 



II-) IF IT IS USED AS STANDOLONE ( NOT IN AccordDaTools )

( ON ATOS , BELENOS AND RMI LOCAL HPC "PBS ENV"  )  
module load python3/3.8.8-01  
module load cmake   


STEP1 : INSTALL TE FORTRAN/Python EXTENSION TO READ THE GSA FILE (Bmatrix COVARIANCES )
        mkdir -p tuneBR/build 
        cd tuneBR/build  
        
        cmake   ../  
        make 
        make install  
    
        OPTIONS :        
        FC=your fortran compiler   ( optional )
        CC=your C       compiler   ( optional )
        FFLAGS= 
        CFLAGS=           
        VERBOSE=0, 1 or 2    # Verbosity Level (Default =0)




SETP2 : PREPARE SOME ODB FILES ( CCMA FROM MINIMISATION )
        (IN THE DOCUMENTATION, A PERIOD OF 10 DAYS SHOULD BE ENOUGH )

STEP3 : GENERATE A MANDALAY BINARY WITH THE FOLLOWING sql REQUEST 
        "CREATE VIEW mandalay AS
         SELECT  obstype,varno,an_depar,fg_depar,final_obs_error FROM hdr, body, errstat"       
 

STEP3 : CONFIGURE THE "config.ini"  FILE ACCORDING TO YOUR PATHS AND ENVIRONMENT  


STEP4 : RUN 
        python3    tuneBR.py   config.ini  

THE SIGMA_B ,SIGMA_O RATIOS ,AVERAGE RATIOS AND 
THE NUMBER OF USED OBSERVATIONS WILL BE PRINTED ON THE SCREEN

-------------------RUNTIME PERFORMANCE ---------------------
PLATFORM                 :  ECMWF (ATOS )
N DAYS PERIOD            :  10 
N PARALELL PROCESSES     :  6 
ODB CONTENT              :  SYNOP , AMDAR , TEMP & GPSSOL 
CYCLE INCREMENT          :  3 hours 
N SLURM CPU              :  1

RUNTIME DURATION         :  00:02:45
------------------------------------------------------------

