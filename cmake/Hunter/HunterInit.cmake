include_guard()

include(${CMAKE_CURRENT_LIST_DIR}/HunterGate.cmake)

HunterGate(
	URL "https://github.com/cpp-pm/hunter/archive/v0.24.10.tar.gz"
	SHA1 "52997241a19026f428bd2c0c1782606bb456ba90"
	FILEPATH "${CMAKE_CURRENT_LIST_DIR}/HunterConfig.cmake"
)
