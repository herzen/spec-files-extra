#
# spec file for package SFElibmpdclient
#
# includes module: libmpdclient
#

%include Solaris.inc
%define _use_internal_dependency_generator 0

%define srcname libmpdclient

Name:		SFElibmpdclient
IPS_package_name:	library/audio/mpd/libmpdclient
Summary:	Asynchronous API library for interfacing to MPD
URL:		http://mpd.wikia.com/wiki/ClientLib:libmpdclient
Meta(info.upstream):	Max Kellermann <max@duempel.org>
Version:	2.10
License:	BSD
Group:		System/Multimedia Libraries
SUNW_Copyright:	libmpdclient.copyright
Source:		http://www.musicpd.org/download/%srcname/2/%srcname-%version.tar.xz
SUNW_BaseDir:	%_basedir
BuildRoot:	%_tmppath/%name-%version-build
%include default-depend.inc


%package devel
Summary:        %summary - development files
SUNW_BaseDir:   %_basedir
%include default-depend.inc
Requires: %name


%prep
#don't unpack please
%setup -q -c -T -n %{srcname}-%{version}
xz -dc %SOURCE0 | (cd ${RPM_BUILD_DIR}; tar xf -)



%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

# --disable-static doesn't do what it's supposed to, but use it anyway
./configure --prefix=%_prefix --disable-static

# Be modern and use libxnet instead of libsocket
#sed 's/-lsocket -lnsl/-lxnet/' Makefile > Makefile.xnet
#mv Makefile.xnet Makefile

gmake -j$CPUS


%install
rm -rf $RPM_BUILD_ROOT
gmake install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%_libdir/*.la

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %_libdir
%_libdir/lib*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %_includedir
%dir %attr (0755, root, other) %_includedir/mpd
%_includedir/mpd/*
%dir %attr (0755, root, other) %_libdir/pkgconfig 
%_libdir/pkgconfig/%srcname.pc
%dir %attr (0755, root, sys) %_datadir
%_datadir/vala
%dir %attr (0755, root, other) %_datadir/doc
%_datadir/doc/*


%changelog
* Wed Mar 16 2016 - Thomas Wagner
- disable dependency generator 
* Mon Sep  1 2015 - Thomas Wagner
- unpack with xz
* Thu Apr 02 2015 - Ian Johnson <ianj@tsundoku.ne.jp>
- bump to 2.10
* Sat Jan 25 2013 - Alex Viskovatoff
- update to 2.9; follow new naming convention for mpd clients
* Tue Apr 17 2012 - Thomas Wagner
- bump to 2.7
* Thu Jul 21 2011 - Alex Viskovatoff
- Add SUNW_Copyright
* Tue Jan 18 2011 - Alex Viskovatoff
- Initial spec
