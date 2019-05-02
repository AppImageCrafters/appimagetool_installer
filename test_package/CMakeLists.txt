project(TestAppImageKit CXX)


add_executable(AppRun main.cpp)
install(TARGETS AppRun RUNTIME DESTINATION ".")
install(FILES res/appimage.svg res/org.appimagecraft.TestApp.desktop DESTINATION ".")
