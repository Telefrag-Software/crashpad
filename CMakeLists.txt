cmake_minimum_required(VERSION 3.14)

list(INSERT CMAKE_MODULE_PATH 0 ${CMAKE_CURRENT_SOURCE_DIR}/CMake)

include(Hunter/HunterInit)

project(crashpad VERSION 0.8.0 LANGUAGES CXX ASM)

include(ThirdPartyLibraries)

if(WIN32)
	enable_language(ASM_MASM)

	set(PLATFORM "Windows")
elseif(APPLE)
	set(PLATFORM "MacOS")
else()
	set(PLATFORM "Linux")
endif()

string(TOLOWER "${PLATFORM}" PLATFORM_LOWER)
string(TOUPPER "${PLATFORM}" PLATFORM_UPPER)

include(SourceFiles)

add_library(${PROJECT_NAME}
	STATIC
		${CRASHPAD_SOURCE_FILES}
)

target_include_directories(${PROJECT_NAME}
	PUBLIC
		$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
		$<INSTALL_INTERFACE:>
)

set_target_properties(${PROJECT_NAME}
	PROPERTIES
		CXX_STANDARD 17
		C_STANDARD 11
)

target_compile_definitions(${PROJECT_NAME}
	PRIVATE
		ZLIB_CONST
		CRASHPAD_ZLIB_SOURCE_EXTERNAL
		CRASHPAD_LSS_SOURCE_EXTERNAL
)

if(UNIX)
	target_compile_options(${PROJECT_NAME}
		PRIVATE
			-Wno-multichar
			-fPIC
	)

	target_compile_definitions(${PROJECT_NAME}
		PRIVATE
			_FILE_OFFSET_BITS=64
	)
endif()

if(WIN32)
	target_include_directories(${PROJECT_NAME}
		PUBLIC
			$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/compat/win>
			$<INSTALL_INTERFACE:>
	)

	target_compile_definitions(${PROJECT_NAME}
		PRIVATE
			NOMINMAX
			UNICODE
			WIN32
			WIN32_LEAN_AND_MEAN
			_CRT_SECURE_NO_WARNINGS
			_HAS_EXCEPTIONS=0
			_UNICODE
	)

	target_compile_options(${PROJECT_NAME}
		PRIVATE
			/FS
			/W4
			/Zi
			/bigobj  # Support larger number of sections in obj file.
			/wd4100  # Unreferenced formal parameter.
			/wd4127  # Conditional expression is constant.
			/wd4324  # Structure was padded due to alignment specifier.
			/wd4351  # New behavior: elements of array will be default initialized.
			/wd4577  # 'noexcept' used with no exception handling mode specified.
			/wd4996  # 'X' was declared deprecated.
			/wd4201  # nonstandard extension used : nameless struct/union
	)

	target_link_libraries(${PROJECT_NAME}
		PUBLIC
			rpcrt4
			user32
			version
			winhttp
	)
elseif(APPLE)
	target_include_directories(${PROJECT_NAME}
		PUBLIC
			third_party/xnu/EXTERNAL_HEADERS/mach-o
			${CMAKE_CURRENT_BINARY_DIR}
	)

	find_package (Python COMPONENTS Interpreter REQUIRED)

	set(CRASHPAD_UTIL_OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/util/mach/child_portUser.c
		${CMAKE_CURRENT_BINARY_DIR}/util/mach/child_portServer.c
		${CMAKE_CURRENT_BINARY_DIR}/util/mach/child_port.h
		${CMAKE_CURRENT_BINARY_DIR}/util/mach/child_portServer.h
	)

	add_custom_command(
		COMMAND ${Python_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/util/mach/mig.py --sdk ${CMAKE_OSX_SYSROOT} --include ${CMAKE_CURRENT_SOURCE_DIR}/util/mac ${CMAKE_CURRENT_SOURCE_DIR}/util/mach/child_port.defs ${CMAKE_CURRENT_BINARY_DIR}/util/mach/child_portUser.c ${CMAKE_CURRENT_BINARY_DIR}/util/mach/child_portServer.c ${CMAKE_CURRENT_BINARY_DIR}/util/mach/child_port.h ${CMAKE_CURRENT_BINARY_DIR}/util/mach/child_portServer.h
		DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/util/mach/mig.py ${CMAKE_CURRENT_SOURCE_DIR}/util/mach/mig_gen.py ${CMAKE_CURRENT_SOURCE_DIR}/util/mach/mig_fix.py ${CMAKE_CURRENT_SOURCE_DIR}/util/mach/child_port.defs
		OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/util/mach/child_portUser.c ${CMAKE_CURRENT_BINARY_DIR}/util/mach/child_portServer.c ${CMAKE_CURRENT_BINARY_DIR}/util/mach/child_port.h ${CMAKE_CURRENT_BINARY_DIR}/util/mach/child_portServer.h
		COMMENT "Generating code using MIG for child_port."
	)

	foreach(source exc mach_exc notify)
		set(CRASHPAD_UTIL_OUTPUT ${CRASHPAD_UTIL_OUTPUT}
			${CMAKE_CURRENT_BINARY_DIR}/util/mach/${source}User.c
			${CMAKE_CURRENT_BINARY_DIR}/util/mach/${source}Server.c
			${CMAKE_CURRENT_BINARY_DIR}/util/mach/${source}.h
			${CMAKE_CURRENT_BINARY_DIR}/util/mach/${source}Server.h
		)

		add_custom_command(
			COMMAND ${Python_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/util/mach/mig.py --sdk ${CMAKE_OSX_SYSROOT} --include ${CMAKE_CURRENT_SOURCE_DIR}/util/mac ${CMAKE_OSX_SYSROOT}/usr/include/mach/${source}.defs ${CMAKE_CURRENT_BINARY_DIR}/util/mach/${source}User.c ${CMAKE_CURRENT_BINARY_DIR}/util/mach/${source}Server.c ${CMAKE_CURRENT_BINARY_DIR}/util/mach/${source}.h ${CMAKE_CURRENT_BINARY_DIR}/util/mach/${source}Server.h
			DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/util/mach/mig.py ${CMAKE_CURRENT_SOURCE_DIR}/util/mach/mig_gen.py ${CMAKE_CURRENT_SOURCE_DIR}/util/mach/mig_fix.py ${CMAKE_OSX_SYSROOT}/usr/include/mach/${source}.defs
			OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/util/mach/${source}User.c ${CMAKE_CURRENT_BINARY_DIR}/util/mach/${source}Server.c ${CMAKE_CURRENT_BINARY_DIR}/util/mach/${source}.h ${CMAKE_CURRENT_BINARY_DIR}/util/mach/${source}Server.h
			COMMENT "Generating code using MIG for ${source}."
		)
	endforeach()

	target_link_libraries(${PROJECT_NAME}
		PUBLIC
			bsm
			dl
			"-framework CoreFoundation"
			"-framework Foundation"
			"-framework IOKit"
	)
else()
	target_include_directories(${PROJECT_NAME}
		PUBLIC
			$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/compat/linux>
			$<INSTALL_INTERFACE:>
	)
endif()

target_link_libraries(${PROJECT_NAME}
	PUBLIC
		mini_chromium
		ZLIB::zlib
)
