#
# spec file for package SFEliborcus
#
# includes module: liborcus
#
## TODO ##

%include Solaris.inc
%define cc_is_gcc 1
%include usr-g++.inc
%include base.inc
%include packagenamemacros.inc
%define _use_internal_dependency_generator 0

%define src_name liborcus
%define src_url  http://kohei.us/files/orcus/src

# Dunno what it is with people putting 0.8.0 config in a download file with 0.7.0 in it
%define major_version 0.7
%define minor_version 1
#%define major_version 0.8
#%define minor_version 0
#%define major_version 0.9
#%define minor_version 2

Name:			SFEliborcus
IPS_Package_Name:	sfe/library/g++/liborcus
Summary:		Standalone file import filter library for spreadsheet documents (/usr/g++)
Group:			System/Libraries
URL:			https://gitlab.com/orcus/orcus
Version:		%major_version.%minor_version
License:		MPL2.0
SUNW_Copyright:		%{license}.copyright
Source:			%{src_url}/%{src_name}-%{version}.tar.xz
#Source:		%{src_url}/%{src_name}-0.7.0.tar.bz2
SUNW_BaseDir:		%_basedir
BuildRoot:		%_tmppath/%name-%version-build

%include default-depend.inc

BuildRequires:	SFEgcc
Requires:	SFEgccruntime

# BuildRequires aclocal-1.14 (part of automake)

BuildRequires:	%{pnm_buildrequires_boost_gpp_default}
Requires:	%{pnm_requires_boost_gpp_default}

BuildRequires:	%{pnm_buildrequires_icu_gpp_default}
Requires:	%{pnm_requires_icu_gpp_default}

##TODO## check this dependency. Is it a hard 2.7 or just a default module needed for 2.6?
# probably a fib but 0.9.2 requires python >= 2.7.1
##BuildRequires:	runtime/python-27 >= 2.7.1
##Requires:	runtime/python-27 >= 2.7.1
BuildRequires: %{pnm_buildrequires_python_default}
Requires:      %{pnm_requires_python_default}

BuildRequires:	%{pnm_buildrequires_system_library_math_header_math}
Requires:	%{pnm_requires_system_library_math_header_math}


BuildRequires:  %{pnm_buildrequires_SUNWzlib}
Requires:       %{pnm_requires_SUNWzlib}

%if %( expr %{solaris11} '+' %{solaris12}  '+' %{openindiana} '>=' 1 )
#S11 S12 openindiana need zlib.pc (should not bother oihipster, which probably already has a propper zlib.pc)
BuildRequires:  %{pnm_buildrequires_SFEzlib_pkgconfig} 
#for pkgtool's dependency resoultion
Requires:       %{pnm_buildrequires_SFEzlib_pkgconfig} 
%endif

BuildRequires:  %{pnm_buildrequires_SFExz_gnu}

BuildRequires:  SFElibrevenge
Requires:       SFElibrevenge

BuildRequires:	SFElibixion
Requires:	SFElibixion

BuildRequires:	SFEmdds
Requires:	SFEmdds

%description
liborcus is a standalone file import filter library for spreadsheet
documents. Currently under development are ODS, XLSX and CSV import
filters.

%package devel
Summary:        %summary - development files
SUNW_BaseDir:   %_basedir
%include default-depend.inc
Requires: %name



%prep
#don't unpack please
%setup -q -c -T -n %src_name-%version
xz -dc %SOURCE0 | (cd ${RPM_BUILD_DIR}; tar xf -)


%build

CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CC=gcc
export CXX=g++
export CFLAGS="%optflags -I/usr/g++/include"
export CXXFLAGS="%cxx_optflags -I/usr/g++/include"
export LDFLAGS="%_ldflags -L/usr/g++/lib -R/usr/g++/lib"

##try #mdds.pc in wrong location!
##try export PKG_CONFIG_PATH=/usr/share/pkgconfig:$PKG_CONFIG_PATH
# pja 20150920 - re-introduce PKG_CONFIG_PATH to suit /usr/g++
export PKG_CONFIG_PATH=/usr/gnu/lib/pkgconfig:/usr/g++/lib/pkgconfig

##TODO## Verified on S11 S12 to not appear, remove the comment of the folowing osdistro are (now) w/o this error
##TODO## verify on OIHipster if this appears
##TODO## verify on oi151a9 if this appears
## TODO ##
# Fix this
#checking boost/thread.hpp presence... no
#checking boost/thread.hpp usability... yes
#checking boost/thread.hpp presence... no
#configure: WARNING: boost/thread.hpp: accepted by the compiler, rejected by the preprocessor!
#configure: WARNING: boost/thread.hpp: proceeding with the compiler's result
#checking for boost/thread.hpp... yes
#checking for the Boost thread library... (cached) yes

# boost/iostreams/device/file_descriptor.hpp
# above doesn't like -pthreads


##TODO## oh, this might need a review, if it is still needed. Check with visibility fixes for the SFEgcc on OmniOS, might apply for S12 too
#S12
%if %{solaris12}
   gsed -i.bak0 -e '/^CXXFLAGS=/ s/-fvisibility=hidden//' \
   configure.ac \
   ;
%endif

#debug [ -f configure.ac.bak0 ] && (diff -u configure.ac.bak0 configure.ac; exit 0)

#  Peter Tribbles' sneaky hack to insert -pthreads in all the Makefiles at:
#For liborcus, run the following against all the Makefiles that the configure step generates:
#gsed -i 's:-DMDDS_HASH_CONTAINER_BOOST:-pthreads -DMDDS_HASH_CONTAINER_BOOST:'

#this is the same then Peter did to Makefile but this time done to configure.ac (gets rebuilt, creates Makefile at ./configure time)
gsed -i.bak1 -e 's/-DMDDS_HASH_CONTAINER_BOOST/-pthreads -DMDDS_HASH_CONTAINER_BOOST/' configure.ac

#debug [ -f configure.ac.bak1 ] && (diff -u configure.ac.bak1 configure.ac; exit 0)

echo "verify that \"-pthreads\" is in CXXFLAGS"
grep "CXXFLAGS.*pthreads" configure*

#note, boost for example on %{oihipster} is /usr, other osdistro use SFEboost-gpp in /usr/g++

./configure	\
	--prefix=%_prefix	\
        --with-boost=%{boost_gpp_default_prefix} \
	;

echo "verify that \"-pthreads\" is in CXXFLAGS"
grep "CXXFLAGS.*pthreads" configure*

#touch Makefile.in
#touch configure
#touch config.status
#touch Makefile
#touch stamp-h1

#I can't help, that super smart Makefile immediately re-creates everything by running: 
#/bin/bash ./config.status --recheck
#you'll see in "make" for the second time a configure run. Only costs a bit of time, so stop fixing an overly sensitive Makefile.
make V=2 -j$CPUS


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%_libdir/*.*a

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)

%dir %attr (0755, root, bin) %_bindir
%_bindir/orcus-*

%dir %attr (0755, root, bin) %_libdir
%_libdir/%src_name-*.so*
#%_libdir/%src_name-mso-*.so*
#%_libdir/%src_name-parser-*.so*
#%_libdir/%src_name-spreadsheet-model-*.so*

%dir %attr (0755, root, other) %_libdir/pkgconfig
%_libdir/pkgconfig/%src_name-*.pc
#%_libdir/pkgconfig/%src_name-spreadsheet-model-*.pc

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %_includedir
%dir %_includedir/%src_name-*
%_includedir/%src_name-*/orcus


%changelog
* Fri Apr 22 2016 - Thomas Wagner
- change (Build)Requires to pnm_buildrequires_SFEzlib_pkgconfig
* Fri Oct 23 2015 - Thomas Wagner
- merge in pjama's changes
* Sun Oct 11 2015 - Thomas Wagner
- change to (Build)Requires %{pnm_buildrequires_icu_gpp_default}
* Sun Sep 20 2015 - pjama
- %include usr-g++.inc
- set (Build)Requires: for SFE gcc
- icu is not required
- pnm BuildRequires default python as opposed to fixed version 2.7  because Openindiana only has 2.6
* Sat Aug 22 2015 - Thomas Wagner
- move injection of "-pthreads" to CXXFLAGS from Makefile to configure.ac (avoid throwing out the "-fvisibility=hidden" removal from configure configure.ac (S12)
- leave a bit debug output on, don't set PKG_CONFIG_PATH to /usr/share/pkgconfig and see if mdds.pc is still propperly / configured (tested on S11, S12)
* Thu Aug 20 2015 - Thomas Wagner
- add BuildRequires SFEzlib-pkgconfig, remove variables pointing to ZLIB
- remove in configure script -fvisibility=hidden from CXXFLAGS on S12
* Sat Aug 15 2015 - Thomas Wagner
- override configure autodetection (missing zlib.pc) (S11 S12 OI)
- use --with-boost=%{boost_gpp_default_prefix} for e.g. /usr/g++ (S11 S12 OI)
- add Requires: runtime/python-27 (to get pkgtool --autodeps work)
* Mon Aug 10 2015 - Thomas Wagner
- rename IPS_Package_Name to propperly reflect g++ compiler
##TODO## relocation to /usr/g++ (depends on LO package)
- initial commit to svn for pjama
- unpack with xz
##TODO## check python 2.7 only or is python 2.6 plus modules enough?
- change to (Build)Requires %{pnm_buildrequires_SUNWzlib}, %{pnm_buildrequires_boost_gpp_default}, developer_icu, library_math_header_math, SUNWlxml_devel, add SFExz_gnu, library_math_header_math, add SFExz_gnu
* Sun Jun 14 2015 - pjama
- initial spec
