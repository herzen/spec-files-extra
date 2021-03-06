#
# spec file for package SFEqt47
#
# includes module: qt
#

# NOTE: The easiest way to make pkgtool find the patches used by this spec
# is to install experimental/SFEpkgbuild.spec, and rename pkgbuild and pkgtool
# in /opt/dtbld/bin to something else, so that your updated pgbuild and
# pkgtool are found instead.
# Otherwise, build with
# pkgtool build --patches=patches/qt47 SFEqt47.spec
# If you use the --autodeps flag, use
# pkgtool build --patches=patches:patches/qt47 --autodeps SFEqt47.spec

# NOTE: This spec makes use of patches which are hard-coded to enable features
# of the Intel Nehalem processor, specifically, the SSE 4.2 instruction set.
# However, the enabling of these features is overriden in the call to configure
# below, to conform with the practice at SFE of assuming that an i386 CPU is not
# higher than Pentium.  Thus, if your CPU has a bigger feature set than a
# Pentium CPU, you should remove the corresponding flags in the call to
# configure.

# TODO: Autodetect CPU features and configure correspondingly.

# NOTE FOR USERS:
# If you want nice looking fonts with aliasing, you should create .fonts.conf in your homedir
# qt apps don't respect GNOME settings without KDE stuff installed
# Example .fonts.conf from my machine:
#<?xml version='1.0'?>
#<!DOCTYPE fontconfig SYSTEM 'fonts.dtd'>
#<fontconfig>
#    <match target="font" >
#        <edit mode="assign" name="hinting" >
#            <bool>true</bool>
#        </edit>
#    </match>
#
#    <match target="font" >
#        <edit mode="assign" name="antialias" >
#            <bool>true</bool>
#        </edit>
#   </match>
#</fontconfig>


# NOTE: To build software using this library which uses qmake, use
# export PATH=/usr/stdcxx/bin:$PATH
# export QMAKESPEC=solaris-cc-stdcxx
# export QTDIR=/usr/stdcxx

%define _basedir /usr/stdcxx
%include Solaris.inc
%define srcname qt-everywhere-opensource-src
%include packagenamemacros.inc

Name:                SFEqt-stdcxx
IPS_Package_Name:	library/desktop/stdcxx/qt
Summary:             Cross-platform development framework/toolkit (stdcxx)
URL:                 http://qt-project.org
License:             LGPLv2
Version:             4.7.4
%define major_minor_version $( echo %{version} |  awk -F'.' '{print $1 "." $2}' )
Source:		http://download.qt-project.org/archive/qt/%{major_minor_version}/qt-everywhere-opensource-src-%{version}.tar.gz
Source1:	     qmake.conf
Patch1:		     qt47/qt471-01-configure-ext.diff
Patch2:		     qt47/qt471-02-ext.diff
Patch3:		     qt47/qt-ext2.diff
Patch4:		     qt47/qt471-04-sse42.diff
#These patches are stolen from KDE guys and affect WebKit 
#(I'm not first who stole them, most of them are stolen from cvsdude old repo)
Patch5:		     qt47/webkit01-17.diff
Patch6:		     qt47/webkit04-17.diff
Patch7:		     qt47/webkit05-17.diff
Patch8:		     qt47/webkit08-17.diff
Patch9:		     qt47/webkit10-17.diff
Patch10:	     qt47/webkit11-17.diff
Patch11:	     qt47/webkit13-17.diff
Patch12:	     qt47/webkit14-17.diff
Patch13:	     qt47/webkit15-17.diff
Patch14:	     qt47/webkit16-17.diff
Patch15:	     qt47/webkit17-17.diff
#These don't affect Webkit, I've decided they are nice and steal from KDE guys
Patch16:	     qt47/qt-fastmalloc.diff
Patch17:	     qt47/qt-align.diff 
Patch18:	     qt47/qt-qglobal.diff
Patch19:	     qt47/qt-4.6.2-iconv-XPG5.diff
Patch20: 	     qt47/qt-thread.diff
Patch21:	     qt47/qt-arch.diff 
Patch22:	     qt47/qt-4.6.2-webkit-CSSComputedStyleDeclaration.cpp.221.diff
Patch23:	     qt47/qt-4.6.2-networkaccessmanager.cpp.233.diff
Patch24:	     qt47/qt-4.7.0-webkit-runtime_array.h.234.diff
Patch25:	     qt47/qt-MathExtras.diff
Patch26:	     qt47/qt-webkit-exceptioncode.diff 
Patch27:	     qt47/qt-uistring.diff 
Patch28:	     qt47/template.diff 
Patch29:	     qt47/plugin-loader.diff 
Patch30:	     qt47/qt-qxmlquery.cpp.diff
Patch31:	     qt47/qt-clucene.diff 
Patch32:	     qt47/qt-configure-iconv.diff 
Patch33:	     qt47/qt-4.6.2-iconv.diff
Patch34:	     qt47/qt-qmutex_unix.cpp.diff
#These exclusive to SFE
Patch35:	     qt47/qt471-05-pluginqlib.diff
Patch36:	     qt47/qt-4.7.1-webkit-jscore-munmap.diff
Patch37:	     qt47/qt-4.7.1-webkit-jsc-wts-systemalloc.diff
Patch38:	     qt47/qt-4.7.1-mathextras.diff
Patch39: 	     qt47/qt-4.7.1-qiconvcodec.diff
Patch40:	     qt47/qt-471-shm.diff
Patch41:	     qt47/solaris-g++-qmake-conf.diff
Patch42:             qt47/qt-q_atomic_test_and_set_ptr.diff
Patch43:             qt47/qt-ctype.diff
SUNW_BaseDir:        %{_basedir}
SUNW_Copyright:      qt.copyright
BuildRoot:           %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires: %{pnm_buildrequires_SUNWlibstdcxx4}
Requires:      %{pnm_requires_SUNWlibstdcxx4}

# Guarantee X/freetype environment concisely (hopefully):
BuildRequires: SUNWgtk2
Requires:      SUNWgtk2
BuildRequires: %{pnm_buildrequires_SUNWxwplt}
Requires: %{pnm_requires_SUNWxwplt}
# The above bring in many things, including SUNWxwice and SUNWzlib
Requires: SUNWxwxft
# The above also pulls in SUNWfreetype2

BuildRequires: %{pnm_buildrequires_mysql_default}
Requires: %{pnm_requires_mysql_default}
BuildRequires: SUNWdbus
Requires: SUNWdbus

# Follow example of developer/icu for IPS package name
%package devel
IPS_package_name:       developer/desktop/stdcxx/qt
Summary:        %{summary} - development files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires: %{name}

%package doc
IPS_package_name:	library/desktop/stdcxx/qt/documentation
Summary:        %{summary} - documentation files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires: %{name}

%prep
%setup -q -n %{srcname}-%{version}
# Don't pass --fuzz=0 to patch
%define _patch_options --unified
%patch1 -p0
%patch2 -p0
%patch3 -p0
%patch4 -p0
%patch5 -p0
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p0
%patch18 -p1
%patch19 -p1
%patch20 -p0
%patch21 -p0
%patch22 -p1
#%patch23 -p1
%patch24 -p1
%patch25 -p0
%patch26 -p0
%patch27 -p0
%patch28 -p0
%patch29 -p0
%patch30 -p0
%patch31 -p0
%patch32 -p0
%patch33 -p0
%patch34 -p1
%patch35 -p0
%patch36 -p0
%patch37 -p0
%patch38 -p0
%patch39 -p0
%patch40 -p0
%patch42 -p0
%patch43 -p0

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

%define extra_includes -I/usr/include/dbus-1.0 -I/usr/lib/dbus-1.0/include -I/usr/include/libpng14 -I%{standard_prefix}/%{mysql_default_includedir}/mysql
%define extra_libs  -L%{standard_prefix}/%{mysql_default_libdir}/mysql -R%{standard_prefix}/%{mysql_default_libdir}/mysql

export CFLAGS="%{optflags} -I/usr/include/libpng14"
export CXXFLAGS="%{cxx_optflags} -library=stdcxx4 -I/usr/include/libpng14 -D_REENTRANT -DNDEBUG -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64 -D_POSIX_PTHREAD_SEMANTICS -DSOLARIS -DNO_DEBUG -D_UNICODE -DUNICODE -D_RWSTD_REENTRANT -D_XOPEN_SOURCE=500 -D__EXTENSIONS__ -D_XPG5 -features=anachronisms,except,rtti,export,extensions,nestedaccess,tmplife,tmplrefstatic,zla -xlang=c99 -instances=global -template=geninlinefuncs -xalias_level -xbuiltin -xustr=ascii_utf16_ushort -s -xdebugformat=dwarf -Qoption ccfe  ++boolflag:sunwcch=false"
export LDFLAGS="%{_ldflags} -library=stdcxx4"

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

##TODO##	-no-mmx -no-3dnow -no-sse -no-sse2 -no-sse3 -no-ssse3 -no-sse4.1 -no-sse4.2 \
##TODO##	-no-exceptions \
##TODO##	-plugin-sql-sqlite \
##TODO##	-system-sqlite \
##TODO##	-no-sql-sqlite2 \

# Elliminate -Winline, which Solaris Studio 12.2 rejects
cd src/gui
sed 's/ -Winline//' Makefile > Makefile.fixed
mv Makefile.fixed Makefile
cd ../..
	   
gmake -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

gmake install INSTALL_ROOT=$RPM_BUILD_ROOT

rm ${RPM_BUILD_ROOT}%{_libdir}/*.la

# Eliminate QML imports stuff for now:
# Who is Nokia to create a new subdirectary in /usr?
rm -r ${RPM_BUILD_ROOT}%{_prefix}/imports

# Create qmake.conf for building against this library
cd ${RPM_BUILD_ROOT}%{_datadir}/qt/mkspecs/solaris-cc
sed 's/ -O2/ -xO3 -xspace/' qmake.conf > qmake.conf.new
mv qmake.conf.new qmake.conf
cd ..
mkdir solaris-cc-stdcxx
cd solaris-cc-stdcxx
install %{SOURCE1} .
cp -p ../solaris-cc-stlport/qplatformdefs.h .
cd ..
%patch41 -p0

%clean
rm -rf $RPM_BUILD_ROOT

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


%files -n devel
%defattr (-, root, bin)
#see devel %dir %attr (0755, root, bin) %{_bindir}
#see devel %{_bindir}/*
%dir %attr (0755, root, bin) %{_includedir}
%dir %attr (0755, root, other) %{_includedir}/qt
%{_includedir}/qt/*
%dir %attr (0755, root, bin) %dir %{_libdir} 
%dir %attr (0755, root, other) %{_libdir}/pkgconfig 
%{_libdir}/pkgconfig/*

%files doc
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*


%changelog
* Tue Oct  1 2013 - Thomas Wagner
- new URL, new Source download URL
- rename library/desktop/stdcxx/qt/header-qt to developer/desktop/stdcxx/qt
- align SFEqt-stdcxx.spec with SFEqt-gpp.spec SFEqt.spec
* Mon Nov  5 2012 - Thomas Wagner
- align SFEqt-stdcxx.spec / SFEqt.spec / SFEqt-gpp.spec
* Sun Jun 24 2012 - Thomas Wagner
- change (Build)Requires to %{pnm_buildrequires_SUNWlibstdcxx4}
* Sat Jan 07 2012 - Milan Jurik
- bump to 4.7.4 (with help from KDE specs)
- rename to SFEqt-stdcxx
* Tue Jul 26 2011 - N.B.Prashanth
- Added SUNW_Copyright
* Wed Mar 30 2011 - Alex Viskovatoff
- create separate doc package
* Tue Mar 29 2011 - Thomas Wagner
- create a separate development IPS package
- change BuildRequires to %{pnm_buildrequires_library_desktop_gtk1}
* Mar 23 2011 - Alex Viskovatoff
- Stop supplying the g++ qmake.conf; SFEqt47-gpp can do that
* Sun Mar  6 2011 - Alex Viskovatoff
- Enable Phonon, since it builds now
* Tue Mar  1 2011 - Alex Viskovatoff
- Patch /usr/stdcxx/share/qt/mkspecs/solaris-g++/qmake.conf
* Fri Jan 28 2011 - Alex Viskovatoff
- Change optimization flags in share/qt/mkspecs/solaris-cc/qmake.conf
* Thu Jan 27 2011 - Alex Viskovatoff
- Use -library=stdcxx4 instead of include/stdcxx.inc
- Install in /usr/stdcxx (no longer conflicting with SFEqt4)
* Dec 10 2010 - Alex Viskovatoff
- Add 40 patches supplied by russiane39 which enable WebKit among other things.
- Install qmake.conf file for solaris-cc-stdcxx
* Nov 11 2010 - Alex Viskovatoff
- Fork SFEqt47.spec off SFEqt4.spec, disregarding stlport and snv < 147
- To make the build work, disable examples and phonon.  Disable demos
  because that is what kde-solaris does.
* Nov  4 2010 - Alex Viskovatoff
- Spec needs "%include osdistro.inc" (pointed out by Thomas Wagner)
* Nov  3 2010 - Alex Viskovatoff
- Add patch by Milan Jurik to use new libpng names only for osbuild >= 147
- Use cxx_optflags
* Oct 16 2010 - Alex Viskovatoff
- Fix broken use of stlport: if -library=stlport4 is passed to the compiler,
  it must also be passed to the linker
- Update to version 4.5.3, obviating the need for the existing patches
- Add a patch to use changed field names in libpng-1.4
- Use stdcxx instead of stlport, while allowing use of the deprecated
  stlport as an option. (BionicMutton uses stdcxx.)
- Remove dependency on SUNWgccruntime
* Mar 07 2009 - Thomas Wagner
- rework shared patch qt-01-use_bash.diff (to be more independent of qt version SFEqt SFEqt4 in verison 4.x / 4.5)
* Wed Mar 04 2009 - Thomas Wagner
- fix path to SunStudio compiler. Tested with SunStudioExpress November 2008 in /opt/SUNWspro/bin
- enable configure's hint -no-exceptions (smaller code, less memory)
* Sat Nov 29 2008 - dauphin@enst.fr
- Try to compile with studio12
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
