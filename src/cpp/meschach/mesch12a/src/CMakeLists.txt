file(GLOB SRC_FILES ${PROJECT_SOURCE_DIR}/src/cpp/meschach/mesch12a/src/*.c)


add_library(meschach STATIC ${SRC_FILES})
set_target_properties(meschach PROPERTIES LINKER_LANGUAGE C)
target_include_directories(meschach PUBLIC ${PROJECT_SOURCE_DIR}/src/cpp/meschach/mesch12a/include)
