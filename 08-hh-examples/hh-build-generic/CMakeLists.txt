cmake_minimum_required(VERSION 3.5)
project(conan_third_party_include)
message("====== CMAKE_SYSTEM_PROCESSOR: " ${CMAKE_SYSTEM_PROCESSOR})

set(CMAKE_CXX_STANDARD 11)
include(conan_install${CONAN_INSTALL_DIR_SUFFIX}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS NO_OUTPUT_DIRS KEEP_RPATHS)

# Add an executable
add_executable(third_party_include main.cpp)

# link against the fmt target supplied by conan
target_link_libraries(third_party_include
    PRIVATE
    CONAN_PKG::fmt
)
