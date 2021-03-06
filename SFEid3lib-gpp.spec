#
# spec file for package SFEid3lib-gpp
#
# includes module(s): id3lib
#
#
%include Solaris.inc
%define cc_is_gcc 1
%include usr-g++.inc
%include base.inc
%include packagenamemacros.inc

Name:                    SFEid3lib-gpp
IPS_package_name:	 library/audio/g++/id3lib
Summary:                 id3lib (g++) - a software library for manipulating ID3v1/v1.1 and ID3v2 tags (/usr/g++)
URL:                     http://id3lib.sourceforge.net/
Version:                 3.8.3
Source:                  %{sf_download}/id3lib/id3lib-%{version}.tar.gz
Patch1:                  id3lib-01-wall.diff
Patch2:                  id3lib-02-uchar.diff
Patch3:                  id3lib-03-gcc4.diff
Patch4:		id3lib-04-iconv.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEgcc
Requires: SFEgccruntime
BuildRequires:  %{pnm_buildrequires_SUNWzlib}
Requires:       %{pnm_requires_SUNWzlib}
Requires: SUNWlibms

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n id3lib-%version
%patch1  -p1
%patch2  -p1
%patch3  -p1
%patch4  -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export ACLOCAL_FLAGS="-I %{_std_datadir}/aclocal"
export CC=gcc
export CFLAGS="%{optflags}"
export CXX=g++
#oi151a4 g++ 4.6.3 needs -fpermissiv, s11 doesn't (can't tell why)
export CXXFLAGS="%{cxx_optflags} -fpermissive"
export LDFLAGS="%{_ldflags}"
export LD_OPTIONS="-i -L%{_libdir} -R%{_libdir}"

aclocal -I ./m4 $ACLOCAL_FLAGS
automake -a -c -f
autoconf
libtoolize --copy --force
./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --enable-fpm=%{fp_arch}          \
            --enable-shared		     \
	    --disable-static

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Sun Nov 29 2015 - Thomas Wagner
- change to (Build)Requires %{pnm_buildrequires_SUNWzlib} (OIH)
* Sun Aug 16 2015 - Thomas Wagner
- fix order %include usr-g.*inc base.inc
* Sat Jun 29 2013 - Thomas Wagner
- use std macros for *FLAGS, cc_is_gcc switches content for us
- remove dependency on SUNWlibC (we use gcc)
- add URL
- add (Build)Requires: SFEgcc(runtime)  (or get pkgtool 1.3.105 fail with broken depend line in manifest: depend fmri=depend fmri=pkg:/sfe/system/library/gcc-47-runtime@4.7.3-5.12.0.0.0.24.1 fmri=pkg:/system/library/gcc-45-runtime@4.5.2-5.12.0.0.0.24.1 type=require-any type=require
* Sun Jun 24 2012 - Thomas Wagner
- add -fpermissive to CXXFLAGS, oi151a4 g++ 4.6.3 needs -fpermissiv, s11 doesn't (can't tell why)
* Sat Apr 21 2012 - Thomas Wagner
- %include usr-g++.inc to relocate out from /usr/gnu to --prefix=/usr/g++
- use _std_datadir in ACLOCAL_FLAGS
- add IPS_package_name
- rename package to reflect gcc/g++ compiler and propper location
* Fri Sep 25 2009 - trisk@opensolaris.org
- Add patch3
- Update build system
* Tue Jul 17 2007 - dougs@truemail.co.th
- Converted from SFEid3lib
