cmake_minimum_required(VERSION 3.5)
project(readgsa LANGUAGES C Fortran)

find_package (Python3 COMPONENTS Interpreter)

enable_testing()

# GNU COMPILERS 
if(CMAKE_Fortran_COMPILER_ID MATCHES "GNU")
	set(ENV{FC}    "gfortran")
	set(ENV{FFLAGS}  " "      )   # ADDITIONAL OPTIONAL FLAGS 
	set(Fortran_FLAGS    -Wcpp -O3 -w)
	add_compile_options( ${Fortran_FLAGS} ${FFLAGS})
#endif()

elseif (CMAKE_C_COMPILER_ID MATCHES "GNU")
	set(ENV{CC}    "gcc")
	set(ENV{CFLAGS}  " "      )  # ADDITIONAL OPTIONAL FLAGS
	set(C_FLAGS    -Wcpp -O3 -w)
        add_compile_options( ${C_FLAGS} ${CFLAGS} )
endif()

# INTEL COMPILERS 
if(CMAKE_Fortran_COMPILER_ID MATCHES "Intel")
    set (ENV{FC}  "ifort" ) 
    set (ENV{FFLAGS}  ""  )
    set (ENV{Fortran_FLAGS}  -fPIC -g  -w )
    add_compile_options(${Fortran_FLAGS} ${FFLAGS})
    #endif()

elseif(CMAKE_C_COMPILER_ID MATCHES "Intel")
    set (ENV{CC}  "icc" )
    set (ENV{CFLAGS}  ""      )   
    set (ENV{C_FLAGS}  -fPIC -g  -w )
    add_compile_options(${Fortran_FLAGS} ${CFLAGS} )
endif()

# COMPILE THE FORTRAN ROUTINE 
add_subdirectory ( src )
