# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.16

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/lucas/Documents/stage_gedlibpy/stage/cpp

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/lucas/Documents/stage_gedlibpy/stage/cpp/bin

# Include any dependencies generated for this target.
include CMakeFiles/stage_cpp.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/stage_cpp.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/stage_cpp.dir/flags.make

CMakeFiles/stage_cpp.dir/src/edit_graph.cpp.o: CMakeFiles/stage_cpp.dir/flags.make
CMakeFiles/stage_cpp.dir/src/edit_graph.cpp.o: ../src/edit_graph.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/lucas/Documents/stage_gedlibpy/stage/cpp/bin/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/stage_cpp.dir/src/edit_graph.cpp.o"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/stage_cpp.dir/src/edit_graph.cpp.o -c /home/lucas/Documents/stage_gedlibpy/stage/cpp/src/edit_graph.cpp

CMakeFiles/stage_cpp.dir/src/edit_graph.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/stage_cpp.dir/src/edit_graph.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/lucas/Documents/stage_gedlibpy/stage/cpp/src/edit_graph.cpp > CMakeFiles/stage_cpp.dir/src/edit_graph.cpp.i

CMakeFiles/stage_cpp.dir/src/edit_graph.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/stage_cpp.dir/src/edit_graph.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/lucas/Documents/stage_gedlibpy/stage/cpp/src/edit_graph.cpp -o CMakeFiles/stage_cpp.dir/src/edit_graph.cpp.s

# Object files for target stage_cpp
stage_cpp_OBJECTS = \
"CMakeFiles/stage_cpp.dir/src/edit_graph.cpp.o"

# External object files for target stage_cpp
stage_cpp_EXTERNAL_OBJECTS =

bin/stage_cpp: CMakeFiles/stage_cpp.dir/src/edit_graph.cpp.o
bin/stage_cpp: CMakeFiles/stage_cpp.dir/build.make
bin/stage_cpp: /home/lucas/Documents/stage_gedlibpy/gedlib/gedlib/ext/fann.2.2.0/lib/libdoublefann.so.2.2.0
bin/stage_cpp: /home/lucas/Documents/stage_gedlibpy/gedlib/gedlib/ext/libsvm.3.22/libsvm.so
bin/stage_cpp: /home/lucas/Documents/stage_gedlibpy/gedlib/gedlib/ext/nomad.3.8.1/lib/libnomad.so
bin/stage_cpp: CMakeFiles/stage_cpp.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/lucas/Documents/stage_gedlibpy/stage/cpp/bin/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable bin/stage_cpp"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/stage_cpp.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/stage_cpp.dir/build: bin/stage_cpp

.PHONY : CMakeFiles/stage_cpp.dir/build

CMakeFiles/stage_cpp.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/stage_cpp.dir/cmake_clean.cmake
.PHONY : CMakeFiles/stage_cpp.dir/clean

CMakeFiles/stage_cpp.dir/depend:
	cd /home/lucas/Documents/stage_gedlibpy/stage/cpp/bin && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/lucas/Documents/stage_gedlibpy/stage/cpp /home/lucas/Documents/stage_gedlibpy/stage/cpp /home/lucas/Documents/stage_gedlibpy/stage/cpp/bin /home/lucas/Documents/stage_gedlibpy/stage/cpp/bin /home/lucas/Documents/stage_gedlibpy/stage/cpp/bin/CMakeFiles/stage_cpp.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/stage_cpp.dir/depend

