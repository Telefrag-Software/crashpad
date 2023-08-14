include_guard()

hunter_add_package(mini_chromium)
hunter_add_package(ZLIB)

find_package(mini_chromium CONFIG REQUIRED)
find_package(ZLIB CONFIG REQUIRED)
