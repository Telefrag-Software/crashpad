cmake_minimum_required(VERSION 3.14)

list(INSERT CMAKE_MODULE_PATH 0 ${CMAKE_CURRENT_SOURCE_DIR}/CMake)

include(SourceFiles)

if(APPLE)
	find_package (Python COMPONENTS Interpreter REQUIRED)

	set(CRASHPAD_UTIL_OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/util/mach/child_portUser.c
		${CMAKE_CURRENT_BINARY_DIR}/util/mach/child_portServer.c
		${CMAKE_CURRENT_BINARY_DIR}/util/mach/child_port.h
		${CMAKE_CURRENT_BINARY_DIR}/util/mach/child_portServer.h
	)

	add_custom_command(
		COMMAND ${Python_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/vendor/crashpad/util/mach/mig.py --sdk ${CMAKE_OSX_SYSROOT} --include ${CMAKE_CURRENT_SOURCE_DIR}/mac
		${CMAKE_CURRENT_SOURCE_DIR}/vendor/crashpad/util/mach/child_port.defs ${CMAKE_CURRENT_BINARY_DIR}/util/mach/child_portUser.c ${CMAKE_CURRENT_BINARY_DIR}/util/mach/child_portServer.c ${CMAKE_CURRENT_BINARY_DIR}/util/mach/child_port.h ${CMAKE_CURRENT_BINARY_DIR}/util/mach/child_portServer.h
		DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/vendor/crashpad/util/mach/mig.py ${CMAKE_CURRENT_SOURCE_DIR}/vendor/crashpad/util/mach/mig_gen.py ${CMAKE_CURRENT_SOURCE_DIR}/vendor/crashpad/util/mach/mig_fix.py ${CMAKE_CURRENT_SOURCE_DIR}/vendor/crashpad/util/mach/child_port.defs
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
			COMMAND ${Python_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/vendor/crashpad/util/mach/mig.py --sdk ${CMAKE_OSX_SYSROOT} --include ${CMAKE_CURRENT_SOURCE_DIR}/mac
			${CMAKE_OSX_SYSROOT}/usr/include/mach/${source}.defs ${CMAKE_CURRENT_BINARY_DIR}/util/mach/${source}User.c ${CMAKE_CURRENT_BINARY_DIR}/util/mach/${source}Server.c ${CMAKE_CURRENT_BINARY_DIR}/util/mach/${source}.h ${CMAKE_CURRENT_BINARY_DIR}/util/mach/${source}Server.h
			DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/vendor/crashpad/util/mach/mig.py ${CMAKE_CURRENT_SOURCE_DIR}/vendor/crashpad/util/mach/mig_gen.py ${CMAKE_CURRENT_SOURCE_DIR}/vendor/crashpad/util/mach/mig_fix.py ${CMAKE_OSX_SYSROOT}/usr/include/mach/${source}.defs
			OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/util/mach/${source}User.c ${CMAKE_CURRENT_BINARY_DIR}/util/mach/${source}Server.c ${CMAKE_CURRENT_BINARY_DIR}/util/mach/${source}.h ${CMAKE_CURRENT_BINARY_DIR}/util/mach/${source}Server.h
			COMMENT "Generating code using MIG for ${source}."
		)
	endforeach()
endif()

add_library(crashpad_util
	STATIC
		${CRASHPAD_UTIL_SOURCE_FILES}
)

target_include_directories(crashpad_util
	PUBLIC
		$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
		$<INSTALL_INTERFACE:>
)

target_compile_definitions(crashpad_util
	PRIVATE
		ZLIB_CONST
		CRASHPAD_ZLIB_SOURCE_EXTERNAL
		CRASHPAD_LSS_SOURCE_EXTERNAL
)

target_link_libraries(crashpad_util
	PUBLIC
		mini_chromium
)

if(WIN32)
	target_compile_definitions(crashpad_util
		PRIVATE
			NOMINMAX
			UNICODE
			WIN32
			WIN32_LEAN_AND_MEAN
			_CRT_SECURE_NO_WARNINGS
			_HAS_EXCEPTIONS=0
			_UNICODE
	)

	target_compile_options(crashpad_util
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
	)

	target_link_libraries(crashpad_util
		PUBLIC
			crashpad_compat
			ZLIB::zlib
			user32
			version
			winhttp
	)
elseif(UNIX)
	set_target_properties(crashpad_util
		PROPERTIES
			CXX_STANDARD 17
			C_STANDARD 11
	)

	target_compile_options(crashpad_util
		PRIVATE
			-Wno-multichar
			-fPIC
	)

	if(NOT APPLE)
		target_link_libraries(crashpad_util
			PUBLIC
				crashpad_compat
				ZLIB::zlib
		)

		target_compile_definitions(crashpad_util
			PRIVATE
				_FILE_OFFSET_BITS=64
		)
	else()
		target_link_libraries(crashpad_util
			PUBLIC
				ZLIB::zlib
				bsm
				"-framework CoreFoundation"
				"-framework Foundation"
				"-framework IOKit"
		)
	endif()
endif()

#target_include_directories(crashpad_util
#	PUBLIC
#		vendor/crashpad
#		vendor
#)

if(APPLE)
	target_include_directories(crashpad_util
		PUBLIC
			..//third_party/xnu/EXTERNAL_HEADERS/mach-o
			mac
			${CMAKE_CURRENT_BINARY_DIR}
	)
endif()
