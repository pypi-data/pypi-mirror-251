cmake_minimum_required (VERSION 2.8)
project (beam C)

find_package (LibXml2 REQUIRED)

add_executable (beam beam.c)
target_include_directories (beam PUBLIC ${LIBXML2_INCLUDE_DIR})
target_link_libraries(beam ${LIBXML2_LIBRARIES})
