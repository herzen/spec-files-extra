#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%define standard_prefix /usr
%include Solaris.inc
%define srcname qt-everywhere-opensource-src
%include packagenamemacros.inc

Name:                SFEqt
IPS_Package_Name:	library/desktop/qt
Summary:             Cross-platform development framework/toolkit
URL:                 http://qt-project.org
License:             LGPLv2
Version:             4.7.4
%define major_minor_version $( echo %{version} |  awk -F'.' '{print $1 "." $2}' )
Source:		http://download.qt-project.org/archive/qt/%{major_minor_version}/qt-everywhere-opensource-src-%{version}.tar.gz
Patch1:		qt-01-q_atomic_test_and_set_ptr.diff
Patch2:		qt-02-ctype.diff
Patch3:		qt-03-disable-helloconcurrent.diff
SUNW_Copyright:	     qt.copyright
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

# Guarantee X/freetype environment concisely (hopefully):
BuildRequires: SUNWgtk2
Requires:      SUNWgtk2
BuildRequires: %{pnm_buildrequires_SUNWxwplt}
Requires: %{pnm_requires_SUNWxwplt}
# The above bring in many things, including SUNWxwice and SUNWzlib
Requires: SUNWxwxft
# The above also pulls in SUNWfreetype2
# This package only provides libraries
BuildRequires: %{pnm_buildrequires_mysql_default}
Requires: %{pnm_requires_mysql_default}
BuildRequires: SUNWdbus
Requires: SUNWdbus

# Follow example of developer/icu for IPS package name
%package devel
IPS_package_name:       developer/desktop/qt
IPS_package_name:	library/desktop/qt/header-qt
Summary:        %{summary} - development files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires: %{name}

%package doc
IPS_package_name:	library/desktop/qt/documentation
Summary:        %{summary} - documentation files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires: %{name}

%prep
%setup -q -n %{srcname}-%{version}
%patch1 -p0
%patch2 -p0

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

%define extra_includes -I/usr/include/dbus-1.0 -I/usr/lib/dbus-1.0/include -I/usr/include/libpng14 -I%{standard_prefix}/%{mysql_default_includedir}/mysql
%define extra_libs  -L%{standard_prefix}/%{mysql_default_libdir}/mysql -R%{standard_prefix}/%{mysql_default_libdir}/mysql

export CFLAGS="%{optflags} -I/usr/include/libpng14"
export CXXFLAGS="%cxx_optflags -I/usr/include/libpng14"
export LDFLAGS="%_ldflags"

./configure -prefix %{_prefix} \
           -confirm-license \
           -opensource \
           -platform solaris-cc \
           -docdir %{_docdir}/qt \
	   -bindir %{_bindir} \
	   -libdir %{_libdir} \
           -headerdir %{_includedir}/qt \
           -plugindir %{_libdir}/qt/plugins \
           -datadir %{_datadir}/qt \
           -translationdir %{_datadir}/qt/translations \
           -examplesdir %{_datadir}/qt/examples \
           -demosdir %{_datadir}/qt/demos \
           -nomake examples \
           -nomake demos \
           -sysconfdir %{_sysconfdir} \
           -L /usr/gnu/lib \
           -R /usr/gnu/lib \
	   -optimized-qmake \
           -reduce-relocations \
           -opengl desktop \
           -shared \
           -plugin-sql-mysql \
           %{extra_includes} \
           %{extra_libs}

#we have '-nomake examples' ?
[ -f examples/tutorials/threads/Makefile ] && %patch3 -p0

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install INSTALL_ROOT=$RPM_BUILD_ROOT

rm ${RPM_BUILD_ROOT}%{_libdir}/*.la

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr (-, root, bin)
#see devel %dir %attr (0755, root, bin) %{_bindir}
#see devel %{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/lib*.prl
%{_libdir}/libQtUiTools.a
%dir %attr (0755, root, bin) %{_libdir}/qt
%{_libdir}/qt/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/qt


%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_includedir}
%dir %attr (0755, root, other) %{_includedir}/qt
%{_includedir}/qt/*
%dir %attr (0755, root, bin) %dir %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig 
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/qt/mkspecs
%dir %attr (0755, root, other) %{_prefix}/imports
%{_prefix}/imports/*

%files doc
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/qt/q3porting.xml
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*


%changelog
* Sun Nov 10 2013 - Thomas Wagner
- new Source download URL
- rename library/desktop/qt/header-qt to developer/desktop/qt 
- align SFEqt-stdcxx.spec with SFEqt-gpp.spec SFEqt.spec
* Sun Nov  4 2012 - Thomas Wagner
- align SFEqt-gpp.spec and SFEqt.spec
* Mon Jul  9 2012 - Thomas Wagner
- rework to align with SFEgt-gpp.spec
- add IPS_Package_Name
* Mon Jan 09 2012 - Milan Jurik
- use libCstd (SFEqt-gpp is QT built with GCC)
- bump to 4.7.4
* Wed Mar 10 2010 - Brian Cameron
- Add -no-webkit to configure, otherwise the linker crashes.
  Looks like this will go away when binutils is updated to 2.21 (which is not
  yet released).  Refer:
  http://bugs.gentoo.org/show_bug.cgi?id=295765
* Tue Feb 02 2010 - Brian Cameron
- Fix spec-file so it builds.  Now use define cc_is_gcc, for example.
* Mar 07 2009 - Thomas Wagner
- rework shared patch qt-01-use_bash.diff (to be more independent of qt version
  SFEqt SFEqt4 in verison 4.x / 4.5)
* Wed Mar 04 2009 - Thomas Wagner
- can't find libcstd++.6.*, add to configure:
  -L /usr/gnu/lib -R /usr/gnu/lib (gcc4, for gcc3 this would be sfw instead
  gnu)
- enable configure's hint -no-exceptions (smaller code, less memory)
- force to SFEgcc 4.x because sfw/gcc3 failed to compile
  qdrawhelper_mmx3dnow.cpp with missing mm3dnow.h (to be found only in gcc4)
  (change Requires from SUNWgccruntime to SFEgcc(runtime),
   <CC|CXX>=/usr/gnu/bin/<gcc|g++>)
  ##TODO## is this a failure of configure/something else to depend on a *.h not
  present?
* Mon Nov 24 2008 - alexander@skwar.name
- Add qt-01-use_bash.diff, which replaces all calls to sh with bash,
  because Qt won't build when sh isn't bash.
  Cf. http://markmail.org/message/hzb3fypsc5sopf2b ff. and there
  http://markmail.org/message/l7yleonbjqnl7nfv
- Remove tarball_version - version is good enough
* Sun Nov 11 2008 - dick@nagual.nl
- Bump to 4.4.3
* Sun Sep 21 2008 - dick@nagual.nl
- Bump to 4.4.2
* Tue May 13 2008 - nonsea@users.sourceforge.net
- Bump to 4.4.0
* Fri Mar 21 2008 - nonsea@users.sourceforge.net
- Bump to 4.4.0-rc1
- Remove upstreamed patch time.diff
* Fri Mar 21 2008 - nonsea@users.sourceforge.net
- Bump to 4.4.0-beta1, and update %files
- Add patch time.diff
* Mon Mar 19 2007 - dougs@truemail.co.th
- Fixed -fno-omit-frame-pointer flag
- Bump to 4.2.3
* Thu Dec 07 2006 - Eric Boutilier
- Initial spec
