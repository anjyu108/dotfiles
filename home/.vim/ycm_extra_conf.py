# Modified by midchildan

# Copyright (C) 2014 Google Inc.
#
# This file is part of ycmd.
#
# ycmd is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ycmd is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ycmd.  If not, see <http://www.gnu.org/licenses/>.

import os
import ycm_core

# These are the compilation flags that will be used in case there's no
# compilation database set (by default, one is not set).
# CHANGE THIS LIST OF FLAGS. YES, THIS IS THE DROID YOU HAVE BEEN LOOKING FOR.
flags = [
'-Wall',
'-Wextra',
'-Werror',
'-fexceptions',
'-DNDEBUG',
'-isystem',
'/usr/include',
'-isystem',
'/usr/local/include',
'-isystem',
'/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/../lib/c++/v1',
'-isystem',
'/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/include',
]


# Set this to the absolute path to the folder (NOT the file!) containing the
# compile_commands.json file to use that instead of 'flags'. See here for
# more details: http://clang.llvm.org/docs/JSONCompilationDatabase.html
#
# Most projects will NOT need to set this to anything; you can just change the
# 'flags' list of compilation flags.
compilation_database_folder = ''

if os.path.exists( compilation_database_folder ):
  database = ycm_core.CompilationDatabase( compilation_database_folder )
else:
  database = None

SOURCE_EXTENSIONS = [ '.cpp', '.cxx', '.cc', '.c', '.cu', '.m', '.mm' ]

def DirectoryOfThisScript():
  return os.path.dirname( os.path.abspath( __file__ ) )


def IsHeaderFile( filename ):
  extension = os.path.splitext( filename )[ 1 ]
  return extension in [ '.h', '.hxx', '.hpp', '.hh', '.cuh' ]


def ListCorrespondingSource( filename ):
  basename = os.path.splitext( filename )[ 0 ]
  for extension in SOURCE_EXTENSIONS:
    replacement_file = basename + extension
    if os.path.exists( replacement_file ):
      yield replacement_file


def GetCompilationInfoForFile( filename ):
  # The compilation_commands.json file generated by CMake does not have entries
  # for header files. So we do our best by asking the db for flags for a
  # corresponding source file, if any. If one exists, the flags for that file
  # should be good enough.
  if IsHeaderFile( filename ):
    for replacement_file in ListCorrespondingSource( filename ):
      compilation_info = database.GetCompilationInfoForFile( replacement_file )
      if compilation_info.compiler_flags_:
        return compilation_info
    return None
  return database.GetCompilationInfoForFile( filename )


# This is the last resort; this function is called when no compilation database
# is found.
def GuessFlagsForFile( filename, filetype, flags=[] ):
  # THIS IS IMPORTANT! Without a "-std=<something>" flag, clang won't know which
  # language to use when compiling headers. So it will guess. Badly. So C++
  # headers will be compiled as C headers. You don't want that so ALWAYS specify
  # a "-std=<something>".
  #
  # ...and the same thing goes for the magic -x option which specifies the
  # language that the files to be compiled are written in. This is mostly
  # relevant for c++ headers.
  # For a C project, you would set this to 'c' instead of 'c++'.
  LANGS = {
    'c': { 'flags': [ '-xc', '--std=c11' ], 'ext': [ '.c' ] },
    'cpp': { 'flags': [ '-xc++', '--std=c++14' ],
             'ext': [ '.cpp', '.cxx', '.cc' ] },
    'cuda': { 'flags': [ '-xcuda', '--std=c++14' ], 'ext': [ '.cu', '.cuh' ] },
    'objc': { 'flags': [ '-xobjective-c' ], 'ext': [ '.m' ] },
    'objcpp': { 'flags': [ '-xobjective-c++' ], 'ext': [ '.mm' ] },
  }

  extension = os.path.splitext( filename )[ 1 ]
  if IsHeaderFile( filename ) and extension != '.cuh':
    extension = next( ListCorrespondingSource( filename ), None )

  for l in LANGS.values():
    if extension in l[ 'ext' ]:
      return l[ 'flags' ] + flags

  return LANGS.get( filetype, LANGS[ 'cpp' ] )[ 'flags' ] + flags


# This is the entry point; this function is called by ycmd to produce flags for
# a file.
def FlagsForFile( filename, **kwargs ):
  if not database:
    filetype = None
    client_data = kwargs.get( 'client_data' )
    if client_data:
      filetype = client_data.get( '&filetype' )
    return {
      'flags': GuessFlagsForFile( filename, filetype, flags ),
      'include_paths_relative_to_dir': DirectoryOfThisScript()
    }

  compilation_info = GetCompilationInfoForFile( filename )
  if not compilation_info:
    return None

  # Bear in mind that compilation_info.compiler_flags_ does NOT return a
  # python list, but a "list-like" StringVec object.
  return {
    'flags': list( compilation_info.compiler_flags_ ),
    'include_paths_relative_to_dir': compilation_info.compiler_working_dir_
  }

  # vim:set et sw=2:
