#
# spec file for package SFElibmspub
#
# includes module: libmspub
#
## TODO ##
# It would be nice if libs linked to libicui18n.so and libicuuc.so instead of libicuuc.so.<version_no_at_compile_time> and friends

%include Solaris.inc
%define cc_is_gcc 1
%include usr-g++.inc
%include base.inc
%include packagenamemacros.inc
%define _use_internal_dependency_generator 0

%define src_name libmspub
%define src_url  http://dev-www.libreoffice.org/src/libmspub/

%define major_version 0.1
%define minor_version 2

Name:			SFElibmspub
IPS_Package_Name:	sfe/library/g++/libmspub
Summary:		Microsoft Publisher file format parser library. (/usr/g++)
Group:			System/Libraries
URL:			https://wiki.documentfoundation.org/DLP/Libraries/libmspub
Version:		%major_version.%minor_version
License:		MPL2.0
SUNW_Copyright:		%{license}.copyright
Source:			%{src_url}/%{src_name}-%{version}.tar.xz
Patch1:			libmspub-01-pow.diff
SUNW_BaseDir:		%_basedir
BuildRoot:		%_tmppath/%name-%version-build

%include default-depend.inc

BuildRequires:	SFEgcc
Requires:	SFEgccruntime
BuildRequires:	%{pnm_buildrequires_boost_gpp_default}
Requires:	%{pnm_requires_boost_gpp_default}

BuildRequires:  %{pnm_buildrequires_icu_gpp_default}
Requires:	%{pnm_requires_icu_gpp_default}
BuildRequires:	%{pnm_buildrequires_system_library_math_header_math}
Requires:	%{pnm_requires_system_library_math_header_math}

BuildRequires:  %{pnm_buildrequires_SUNWzlib}
Requires:       %{pnm_requires_SUNWzlib}

BuildRequires:	SFElibrevenge
Requires:	SFElibrevenge

BuildRequires:  %{pnm_buildrequires_SFExz_gnu}

%description
libmspub is a library for parsing the Microsoft Publisher file format structure.

%package devel
Summary:        %summary - development files
SUNW_BaseDir:   %_basedir
%include default-depend.inc
Requires: %name



%prep
#don't unpack please
%setup -q -c -T -n %src_name-%version
xz -dc %SOURCE0 | (cd ${RPM_BUILD_DIR}; tar xf -)

%patch1 -p0


%build

CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CC=gcc
export CXX=g++
export CFLAGS="%optflags -I/usr/g++/include"
export CXXFLAGS="%cxx_optflags -I/usr/g++/include"
export LDFLAGS="%_ldflags -L/usr/g++/lib -R/usr/g++/lib"
%if %{solaris12}
#symbol not found:  boost::system::system_category boost::system::generic_category
export LDFLAGS="$LDFLAGS -lboost_system"
%endif

export PKG_CONFIG_PATH=/usr/gnu/lib/pkgconfig:/usr/g++/lib/pkgconfig

### Should really be if using SFEicu-gpp, which OI does
##%if %{openindiana}
export ICU_CONFIG='/usr/g++/bin/icu-config'
##%endif

./configure	\
	--prefix=%_prefix	\
	;

#from studio compiled icu.pc
#g++: error: unrecognized command line option '-compat=5'
#./Makefile:ICU_CFLAGS =   -compat=5
#./Makefile:LIBVISIO_CXXFLAGS = -I/usr/include/librevenge-0.0   -I/usr/include/libxml2      -compat=5

grep "compat=5" Makefile && \
  perl -w -pi -e "s,-compat=5,," Makefile src/test/Makefile src/conv/text/Makefile src/conv/Makefile src/conv/raw/Makefile src/conv/svg/Makefile src/Makefile src/lib/Makefile inc/libvisio/Makefile inc/Makefile build/Makefile 

gmake V=2 -j$CPUS


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%_libdir/*.*a

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)

%dir %attr (0755, root, bin) %_bindir
%_bindir/pub2*

%dir %attr (0755, root, bin) %_libdir
%_libdir/%src_name-%major_version.so*

%dir %attr (0755, root, other) %_libdir/pkgconfig
%_libdir/pkgconfig/%src_name-%major_version.pc

%dir %attr (0755, root, sys) %_datadir
%dir %attr (0755, root, other) %_datadir/doc
%_datadir/doc/%src_name

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %_includedir
%dir %_includedir/%src_name-%major_version
%_includedir/%src_name-%major_version/%src_name


%changelog
* Tue Nov 17 2015 - Thomas Wagner
- fix linking by adding -lboost_system because  boost::system::system_category boost::system::generic_category not found  (S12)
* Sun Oct 25 2015 - Thomas Wagner
- now really change to (Build)Requires %{pnm_buildrequires_icu_gpp_default}
* Fri Oct 23 2015 - Thomas Wagner
- merge in pjama's changes
- stay with all osdistro default to icu_gpp determined by pnm macro. keeps this spec file simple.
* Sun Oct 11 2015 - Thomas Wagner
- change to (Build)Requires %{pnm_buildrequires_icu_gpp_default}
* Sun 20 Sep 2015 - pjama
- %include usr-g++.inc
- set (Build)Requires: SFEgcc
- set PKG_CONFIG_PATH to find stuff in /usr/g++ and /usr/gnu
- set  ICU_CONFIG so OI finds it. Probably need this for others
- prefix as /usr/g++
- set (Build)Requires: SFEgcc
- set PKG_CONFIG_PATH to find stuff in /usr/g++ and /usr/gnu
- set  ICU_CONFIG so OI finds it. Probably need this for others
* Fri Aug 14 2015 - Thomas Wagner
- edit out -compat=5 from all files, comes from studio compiles icu libraries but g++ doesn't know that switch
* Mon Aug 10 2015 - Thomas Wagner
- rename IPS_Package_Name to propperly reflect g++ compiler
##TODO## relocation to /usr/g++ (depends on LO package)
* Sat Aug  8 2015 - Thomas Wagner
- edit out -compat=5 from all files, comes from studio compiles icu libraries but g++ doesn't know that switch
- initial commit to svn for pjama
- unpack with xz
- change to (Build)Requires %{pnm_buildrequires_SUNWzlib}, %{pnm_buildrequires_boost_gpp_default}, developer_icu, library_math_header_math, add SFExz_gnu
- add (Build)Requires developer_gperf
- disable _use_internal_dependency_generator
* Sun Jun 14 2015 - pjama
- initial spec
- Thanks to Peter Tribble for sharing http://ptribble.blogspot.co.uk/2015/06/building-libreoffice-on-tribblix.html
