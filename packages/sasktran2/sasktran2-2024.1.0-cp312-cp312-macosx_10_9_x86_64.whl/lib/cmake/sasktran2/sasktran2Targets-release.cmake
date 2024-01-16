#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "sasktran2::sasktran2" for configuration "Release"
set_property(TARGET sasktran2::sasktran2 APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(sasktran2::sasktran2 PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libsasktran2.a"
  )

list(APPEND _cmake_import_check_targets sasktran2::sasktran2 )
list(APPEND _cmake_import_check_files_for_sasktran2::sasktran2 "${_IMPORT_PREFIX}/lib/libsasktran2.a" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
