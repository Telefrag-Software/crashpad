cmake_minimum_required(VERSION 3.14)

list(INSERT CMAKE_MODULE_PATH 0 ${CMAKE_CURRENT_SOURCE_DIR}/CMake)

include(SourceFiles)

add_library(crashpad_client
	STATIC
		${CRASHPAD_CLIENT_SOURCE_FILES}
)

target_include_directories(crashpad_client
	PUBLIC
		$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
		$<INSTALL_INTERFACE:>
)

target_link_libraries(crashpad_client
	PUBLIC
		mini_chromium
)

target_compile_definitions(crashpad_client
	PRIVATE
		CRASHPAD_LSS_SOURCE_EXTERNAL
)

if(WIN32)
	target_compile_definitions(crashpad_client
		PRIVATE
			NOMINMAX
			UNICODE
			WIN32
			WIN32_LEAN_AND_MEAN
			_CRT_SECURE_NO_WARNINGS
			_HAS_EXCEPTIONS=0
			_UNICODE
	)

	target_compile_options(crashpad_client
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

	target_link_libraries(crashpad_client
		PUBLIC
			crashpad_compat
			crashpad_util
			rpcrt4
	)
elseif(UNIX)
	set_target_properties(crashpad_client
		PROPERTIES
			CXX_STANDARD 17
			C_STANDARD 11
	)

	target_compile_options(crashpad_client
		PRIVATE
			-Wno-multichar
			-fPIC
	)

	if(NOT APPLE)
		target_link_libraries(crashpad_client
			PUBLIC
				crashpad_compat
				crashpad_util
		)

		target_compile_definitions(crashpad_client
			PRIVATE
				_FILE_OFFSET_BITS=64
		)
	else()
		target_link_libraries(crashpad_client
			PUBLIC
				crashpad_util
		)
	endif()
endif()
