cmake_minimum_required(VERSION 3.8)
project(rqt_crazyflies)


if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

set(CMAKE_INCLUDE_CURRENT_DIR ON)


find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(qt_gui_cpp REQUIRED)
find_package(rqt_gui_cpp REQUIRED)
find_package(Qt5Widgets REQUIRED)

find_package(crazyflie_interfaces REQUIRED)
find_package(crtp_interfaces REQUIRED)

set(state_plugin_SRCS
  src/state_plugin.cpp
  src/crazyflie_status_frame.cpp
  src/crazyflie_connection.cpp
  src/crazyflie_control_modal.cpp
  src/crazyflie_status_widget.cpp
)

set(state_plugin_HDRS
  include/rqt_crazyflies/state_plugin.hpp
  include/rqt_crazyflies/crazyflie_status_frame.hpp
  include/rqt_crazyflies/crazyflie_connection.hpp
  include/rqt_crazyflies/crazyflie_control_modal.hpp
  include/rqt_crazyflies/crazyflie_status_widget.hpp
)

set(state_plugin_UIS
 src/uis/crazyflies_batteries_list.ui
 src/uis/crazyflie_status_widget.ui
 src/uis/crazyflie_control_modal.ui
)


qt5_wrap_cpp(state_plugin_MOCS ${state_plugin_HDRS})
qt5_wrap_ui(state_plugin_UIS_H ${state_plugin_UIS})

add_library(${PROJECT_NAME} SHARED
 ${state_plugin_SRCS}
 ${state_plugin_MOCS}
 ${state_plugin_UIS_H}
)

target_include_directories(${PROJECT_NAME} PUBLIC
  "$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>"
  "$<INSTALL_INTERFACE:include/${PROJECT_NAME}>"
)

ament_target_dependencies(${PROJECT_NAME}
  rclcpp
  qt_gui_cpp
  rqt_gui_cpp
  crazyflie_interfaces
  crtp_interfaces
)

target_link_libraries(${PROJECT_NAME} 
  Qt5::Widgets
)

install(
  TARGETS ${PROJECT_NAME}
  EXPORT ${PROJECT_NAME}
  ARCHIVE DESTINATION lib/${PROJECT_NAME}
  LIBRARY DESTINATION lib/${PROJECT_NAME}
  RUNTIME DESTINATION bin/${PROJECT_NAME})

install(PROGRAMS scripts/state_plugin
  DESTINATION lib/${PROJECT_NAME}
)
install(                           # include to include folder
  DIRECTORY include/
  DESTINATION include/${PROJECT_NAME}
)
install(FILES
  include/rqt_crazyflies/state_plugin.hpp
  scripts/state_plugin
  DESTINATION share/${PROJECT_NAME}
)
install(DIRECTORY resource/       # resources into shared folder
  DESTINATION share/${PROJECT_NAME}
)
install(FILES state_plugin.xml     # plugin-xml into shared folder
  DESTINATION share/${PROJECT_NAME}
)
pluginlib_export_plugin_description_file(rqt_gui "state_plugin.xml")

ament_export_include_directories("include/${PROJECT_NAME}")
ament_export_libraries(${PROJECT_NAME})
ament_export_targets(${PROJECT_NAME})



# find dependencies
find_package(ament_cmake REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
