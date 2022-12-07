%bcond_without tests
%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/galactic/.*$
%global __requires_exclude_from ^/opt/ros/galactic/.*$

Name:           ros-galactic-logging-demo
Version:        0.14.4
Release:        1%{?dist}%{?release_suffix}
Summary:        ROS logging_demo package

License:        Apache License 2.0
Source0:        %{name}-%{version}.tar.gz

Requires:       ros-galactic-rclcpp
Requires:       ros-galactic-rclcpp-components
Requires:       ros-galactic-rcutils
Requires:       ros-galactic-rosidl-default-runtime
Requires:       ros-galactic-std-msgs
Requires:       ros-galactic-ros-workspace
BuildRequires:  ros-galactic-ament-cmake
BuildRequires:  ros-galactic-rclcpp
BuildRequires:  ros-galactic-rclcpp-components
BuildRequires:  ros-galactic-rcutils
BuildRequires:  ros-galactic-rosidl-cmake
BuildRequires:  ros-galactic-rosidl-default-generators
BuildRequires:  ros-galactic-std-msgs
BuildRequires:  ros-galactic-ros-workspace
BuildRequires:  ros-galactic-rosidl-typesupport-fastrtps-c
BuildRequires:  ros-galactic-rosidl-typesupport-fastrtps-cpp
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}
Provides:       %{name}-runtime = %{version}-%{release}
Provides:       ros-galactic-rosidl-interface-packages(member)

%if 0%{?with_tests}
BuildRequires:  ros-galactic-ament-cmake-pytest
BuildRequires:  ros-galactic-ament-lint-auto
BuildRequires:  ros-galactic-ament-lint-common
BuildRequires:  ros-galactic-launch
BuildRequires:  ros-galactic-launch-testing
BuildRequires:  ros-galactic-launch-testing-ament-cmake
BuildRequires:  ros-galactic-launch-testing-ros
BuildRequires:  ros-galactic-rmw-implementation-cmake
%endif

%if 0%{?with_weak_deps}
Supplements:    ros-galactic-rosidl-interface-packages(all)
%endif

%description
Examples for using and configuring loggers.

%prep
%autosetup -p1

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/galactic/setup.sh" ]; then . "/opt/ros/galactic/setup.sh"; fi
mkdir -p .obj-%{_target_platform} && cd .obj-%{_target_platform}
%cmake3 \
    -UINCLUDE_INSTALL_DIR \
    -ULIB_INSTALL_DIR \
    -USYSCONF_INSTALL_DIR \
    -USHARE_INSTALL_PREFIX \
    -ULIB_SUFFIX \
    -DCMAKE_INSTALL_PREFIX="/opt/ros/galactic" \
    -DAMENT_PREFIX_PATH="/opt/ros/galactic" \
    -DCMAKE_PREFIX_PATH="/opt/ros/galactic" \
    -DSETUPTOOLS_DEB_LAYOUT=OFF \
%if !0%{?with_tests}
    -DBUILD_TESTING=OFF \
%endif
    ..

%make_build

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/galactic/setup.sh" ]; then . "/opt/ros/galactic/setup.sh"; fi
%make_install -C .obj-%{_target_platform}

%if 0%{?with_tests}
%check
# Look for a Makefile target with a name indicating that it runs tests
TEST_TARGET=$(%__make -qp -C .obj-%{_target_platform} | sed "s/^\(test\|check\):.*/\\1/;t f;d;:f;q0")
if [ -n "$TEST_TARGET" ]; then
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/galactic/setup.sh" ]; then . "/opt/ros/galactic/setup.sh"; fi
CTEST_OUTPUT_ON_FAILURE=1 \
    %make_build -C .obj-%{_target_platform} $TEST_TARGET || echo "RPM TESTS FAILED"
else echo "RPM TESTS SKIPPED"; fi
%endif

%files
/opt/ros/galactic

%changelog
* Tue Dec 06 2022 Mabel Zhang <mabel@openrobotics.org> - 0.14.4-1
- Autogenerated by Bloom

* Mon May 10 2021 Mabel Zhang <mabel@openrobotics.org> - 0.14.3-1
- Autogenerated by Bloom

* Tue Apr 27 2021 Mabel Zhang <mabel@openrobotics.org> - 0.14.2-1
- Autogenerated by Bloom

* Tue Apr 20 2021 Mabel Zhang <mabel@openrobotics.org> - 0.14.1-2
- Autogenerated by Bloom

* Mon Apr 19 2021 Mabel Zhang <mabel@openrobotics.org> - 0.14.1-1
- Autogenerated by Bloom

* Tue Apr 06 2021 Mabel Zhang <mabel@openrobotics.org> - 0.14.0-1
- Autogenerated by Bloom

* Thu Mar 25 2021 Mabel Zhang <mabel@openrobotics.org> - 0.13.0-1
- Autogenerated by Bloom

* Thu Mar 18 2021 Mabel Zhang <mabel@openrobotics.org> - 0.12.1-1
- Autogenerated by Bloom

* Thu Mar 11 2021 Mabel Zhang <mabel@openrobotics.org> - 0.12.0-3
- Autogenerated by Bloom

* Thu Mar 11 2021 Mabel Zhang <mabel@openrobotics.org> - 0.12.0-2
- Autogenerated by Bloom

* Mon Mar 08 2021 Mabel Zhang <mabel@openrobotics.org> - 0.12.0-1
- Autogenerated by Bloom

