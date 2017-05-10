cmake_minimum_required(VERSION 3.5)

option(WITH_TEST "test option" ON)


add_subdirectory(2)

add_executable(1 1.cc)
target_link_libraries(1 2)
