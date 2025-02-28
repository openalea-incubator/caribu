add_library(bibliotek STATIC
            ferrlog.cpp
            GetOpt.cpp
            outils.cpp
            primitive.cpp
            T_geometrie.cpp
            getallfilename.cpp
            decodeclef.cpp
            chrono.cpp)

target_include_directories(bibliotek PUBLIC ${PROJECT_SOURCE_DIR}/src/cpp/include)