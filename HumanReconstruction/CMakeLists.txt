cmake_minimum_required (VERSION 3.2)
project (HumanReconstruction)
add_executable(HumanReconstruction main.cpp)
list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR})

# link to openvdb (local relative path)
add_library(libopenvdb IMPORTED SHARED GLOBAL)
set_target_properties(libopenvdb PROPERTIES
    "IMPORTED_LOCATION" "${CMAKE_CURRENT_SOURCE_DIR}/../openvdb/libopenvdb.so.3.1.0"
)
include_directories(SYSTEM "${CMAKE_CURRENT_SOURCE_DIR}/../openvdb/")
target_link_libraries(HumanReconstruction libopenvdb)


# link to libHalf (find it in system)
list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR})
find_package(Half REQUIRED)
add_library(libHalf IMPORTED SHARED GLOBAL)
set_target_properties(libHalf PROPERTIES
    "IMPORTED_LOCATION" "${HALF_LIBRARY}/"
)
target_link_libraries(HumanReconstruction ${HALF_LIBRARIES})


# link to libtbb (find it in system)
find_package(TBB REQUIRED)
add_library(libtbb IMPORTED SHARED GLOBAL)
set_target_properties(libtbb PROPERTIES
    "IMPORTED_LOCATION" "${TBB_LIBRARY}/"
)
target_link_libraries(HumanReconstruction ${TBB_LIBRARIES})
