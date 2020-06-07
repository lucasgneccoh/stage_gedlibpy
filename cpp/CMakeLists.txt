cmake_minimum_required(VERSION 2.6)

                

#Configuration du projet

project(stage_cpp)

set(EXECUTABLE_OUTPUT_PATH bin/${CMAKE_BUILD_TYPE})

# Define variables.


set(EXEC_NAME stage_cpp)

set(GEDLIB /home/lucas/Documents/stage_gedlibpy/gedlib/gedlib)
set(LIBRARY_OUTPUT_PATH ${GEDLIB}/lib)
set(LSAPE_HOME ${GEDLIB}/ext/lsape.5)
set(NOMAD_HOME ${GEDLIB}/ext/nomad.3.8.1)
set(LIBSVM_HOME ${GEDLIB}/ext/libsvm.3.22)
set(EIGEN_HOME ${GEDLIB}/ext/eigen.3.3.4)
set(FANN_HOME ${GEDLIB}/ext/fann.2.2.0)
set(BOOST_HOME ${GEDLIB}/ext/boost.1.69.0)

# Add include and link directories.

include_directories(SYSTEM ${BOOST_HOME} ${NOMAD_HOME}/ext/sgtelib/src ${NOMAD_HOME}/src ${LSAPE_HOME}/include ${EIGEN_HOME}/Eigen ${LIBSVM_HOME} ${FANN_HOME}/include ${GUROBI_HOME}/include ${OMP_HOME}/include)
link_directories(${NOMAD_HOME}/lib ${FANN_HOME}/lib ${LIBSVM_HOME} ${GUROBI_HOME}/lib ${OMP_HOME}/lib)

#Génération de la liste des fichiers sources

file(
        GLOB_RECURSE
        source_files
        src/*
)




#Déclaration de l'exécutable

add_executable(
        ${EXEC_NAME} ${source_files}
)

target_link_libraries(

        ${EXEC_NAME}

        ${FANN_HOME}/lib/libdoublefann.so.2.2.0
		${LIBSVM_HOME}/libsvm.so
		${NOMAD_HOME}/lib/libnomad.so
)
