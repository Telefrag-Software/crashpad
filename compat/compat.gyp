# Copyright 2014 The Crashpad Authors. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

{
  'includes': [
    '../build/crashpad.gypi',
  ],
  'targets': [
    {
      'target_name': 'crashpad_compat',
      'type': 'static_library',
      'sources': [
        'android/elf.h',
        'android/linux/elf.h',
        'android/linux/prctl.h',
        'android/linux/ptrace.h',
        'android/sched.h',
        'android/sys/mman.cc',
        'android/sys/mman.h',
        'android/sys/syscall.h',
        'android/sys/user.h',
        'linux/signal.h',
        'linux/sys/ptrace.h',
        'mac/AvailabilityMacros.h',
        'mac/kern/exc_resource.h',
        'mac/mach/i386/thread_state.h',
        'mac/mach/mach.h',
        'mac/mach-o/getsect.cc',
        'mac/mach-o/getsect.h',
        'mac/mach-o/loader.h',
        'mac/sys/resource.h',
        'non_cxx11_lib/type_traits',
        'non_cxx11_lib/utility',
        'non_mac/mach/mach.h',
        'non_win/dbghelp.h',
        'non_win/minwinbase.h',
        'non_win/timezoneapi.h',
        'non_win/verrsrc.h',
        'non_win/windows.h',
        'non_win/winnt.h',
        'win/getopt.h',
        'win/strings.cc',
        'win/strings.h',
        'win/sys/time.h',
        'win/sys/types.h',
        'win/time.cc',
        'win/time.h',
        'win/winnt.h',
        'win/winternl.h',
      ],
      'conditions': [
        ['OS=="mac"', {
          'dependencies': [
            '../third_party/apple_cctools/apple_cctools.gyp:apple_cctools',
          ],
          'include_dirs': [
            'mac',
            'non_cxx11_lib',
          ],
          'direct_dependent_settings': {
            'include_dirs': [
              'mac',
              'non_cxx11_lib',
            ],
          },
        }],
        ['OS=="win"', {
          'include_dirs': [
            'win',
          ],
          'direct_dependent_settings': {
            'include_dirs': [
              'win',
            ],
          },
          'dependencies': [
            '../third_party/getopt/getopt.gyp:getopt',
          ],
        }, {
          'include_dirs': [
            'non_win',
          ],
          'direct_dependent_settings': {
            'include_dirs': [
              'non_win',
            ],
          },
        }],
        ['OS=="android"', {
          'include_dirs': [
            'android',
            'linux',
          ],
          'direct_dependent_settings': {
            'include_dirs': [
              'android',
              'linux',
            ],
          },
          'link_settings': {
            'libraries': [
              '-ldl',
            ],
          },
        }],
        ['OS=="linux"', {
          'include_dirs': [
            'linux',
          ],
          'direct_dependent_settings': {
            'include_dirs': [
              'linux',
            ],
          },
        }],
      ],
    },
  ],
}
