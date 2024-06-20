cmake_minimum_required(VERSION 3.18   )

project(readgsa  LANGUAGES C Fortran  )


# Safety net
if(PROJECT_SOURCE_DIR STREQUAL PROJECT_BINARY_DIR)
  message(
    FATAL_ERROR
      " In-source builds not allowed.\n Please make a new directory (called a build directory) and run CMake from there.\n"
  )
endif()

# GRAB Python, 3.8 or HIGHER 
find_package(Python 3.8 REQUIRED  COMPONENTS Interpreter Development.Module NumPy)

# PYTHON CMD + F2PY HEADERS 
execute_process(
  COMMAND "${Python_EXECUTABLE}"
  -c "import numpy.f2py; print(numpy.f2py.get_include())"
  OUTPUT_VARIABLE F2PY_INCLUDE_DIR
  OUTPUT_STRIP_TRAILING_WHITESPACE
)


# GET THE MODULE SUFFIX 
execute_process( COMMAND "${Python_EXECUTABLE}" -c  "import importlib.machinery as imp ; print( imp.all_suffixes()[2])" OUTPUT_VARIABLE Module_SUFFIX)


# SOME F2PY INCLUDE PATHS 
include(CMakePrintHelpers)
cmake_print_variables(Python_INCLUDE_DIRS)
cmake_print_variables(F2PY_INCLUDE_DIR)
cmake_print_variables(Python_NumPy_INCLUDE_DIRS)

# COMMON VARIABLES 
set(f2py_module_name "readgsa")
set(fortran_src_file "${CMAKE_SOURCE_DIR}/src/readgsa.F90")
set(f2py_module_c    "${f2py_module_name}module.c")
set(numpy_module     "numpy.f2py" )
set(f90_source       readgsa.F90 )


# GENERATE C SOURCE FILE 
add_custom_target ( genpyf   DEPENDS "${CMAKE_CURRENT_BINARY_DIR}/${f2py_module_c}" )

# COMPILATION VERBOSITY LEVEL 
set (ENV{VERBOSE}  "0" )
if     ( VERBOSE MATCHES "0"   )
        set (VERBOSE  --quiet  )
elseif ( VERBOSE MATCHES "1"   )
        set ( VERBOSE "" )
elseif  (VERBOSE MATCHES "2"   )
	set (VERBOSE --verbose )
endif ()


add_custom_command( OUTPUT "${CMAKE_CURRENT_BINARY_DIR}/${f2py_module_c}"
                    COMMAND ${Python_EXECUTABLE}  -m  ${numpy_module} 
                      "${fortran_src_file}"
		      -m ${f2py_module_name}    ${VERBOSE} --overwrite-signature  --lower    DEPENDS ${f90_source} )

set( arg1  ${f2py_module_name} )
set( arg2  ${Module_SUFFIX}   )
string(CONCAT fmodule   ${arg1} ${arg2} )


# TARGET 
Python_add_library(${CMAKE_PROJECT_NAME} MODULE WITH_SOABI
                  "${CMAKE_CURRENT_BINARY_DIR}/${f2py_module_c}"
                  "${F2PY_INCLUDE_DIR}/fortranobject.c" 
                  "${fortran_src_file}" 
                   )



# DEPENDANCIES 
target_link_libraries    (${CMAKE_PROJECT_NAME} PRIVATE Python::NumPy)
add_dependencies          (${CMAKE_PROJECT_NAME} genpyf)
target_include_directories(${CMAKE_PROJECT_NAME} PRIVATE "${F2PY_INCLUDE_DIR}")

install( CODE "file(COPY $<TARGET_FILE:${CMAKE_PROJECT_NAME}>/ DESTINATION ${CMAKE_SOURCE_DIR}/modules/readgsa.so)" )
#message( "-----------SUCCESSFULLY ADDED readgsa.so  TO  tuneBR/modules ----------" )

