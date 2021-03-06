#
# spec file for package fvwm.spec
#
# includes module(s): fvwm
#
%include Solaris.inc

%define src_url		ftp://ftp.fvwm.org/pub/fvwm/version-2

Name:                   fvwm
Summary:                fvwm window manager
Version:                2.6.2
Source:                 %{src_url}/%{name}-%{version}.tar.gz
Patch1:			fvwm-01-png12.diff

%prep
%setup -q -n %{name}-%{version}
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

X11LIB="-L/usr/X11/lib -R/usr/X11/lib"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CPPFLAGS="-I/usr/gnu/lib -I/usr/X11/include"
export CFLAGS="%{optflags} -I/usr/X11/include"
export LDFLAGS="%{_ldflags} $X11LIB -lfontconfig"

libtoolize --copy --force
aclocal $ACLOCAL_FLAGS
automake --add-missing
autoconf --force

# Force configure to run with /bin/bash to work around build failure
# on snv_151a. The workaround does not appear to be needed in newer
# builds (tested snv_171).
/bin/bash \
./configure --prefix=%{_prefix}			\
	    --bindir=%{_bindir}			\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}			\
            --datadir=%{_datadir}		\
            --libexecdir=%{_libexecdir} 	\
            --sysconfdir=%{_sysconfdir}         \
            --without-rplay-library             \
            --without-gnome                     \
            --disable-gtk

make -j$CPUS 

%install
make install DESTDIR=$RPM_BUILD_ROOT
fvwmdir=$RPM_BUILD_ROOT%{_datadir}/fvwm
mv $fvwmdir/system.fvwm2rc-sample-95 $fvwmdir/system.fvwm2rc

%changelog
* Mon Aug 15 2011 - Knut Anders Hatlen
- Run configure with /bin/bash
* Fri Aug 12 2011 - Knut Anders Hatlen
- bump to 2.6.2
- update dependencies
* Mon Jul 11 2011 - Milan Jurik
- bump to 2.5.31
* Fri Apr 27 2006 - dougs@truemail.co.th
- Initial version
