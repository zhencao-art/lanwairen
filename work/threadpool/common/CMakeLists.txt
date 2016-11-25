cmake_minimum_required(VERSION 3.5)

aux_source_directory(. COMMON_SOURCES)
add_library(common STATIC ${COMMON_SOURCES})
