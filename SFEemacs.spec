#
# spec file for package SFEemacs
#

%include Solaris.inc
%define cc_is_gcc 1

# Avoid conflict with editor/gnu-emacs
%include usr-gnu.inc
%include base.inc
%define _infodir %_datadir/info

%include packagenamemacros.inc

Name:                    SFEemacs
IPS_Package_Name:	 sfe/editor/gnu-emacs
Summary:                 GNU Emacs - an operating system in a text editor
Version:                 24.5
License:                 GPLv3+
SUNW_Copyright:          GPLv3.copyright
Source:                  http://ftp.gnu.org/pub/gnu/emacs/emacs-%version.tar.xz
URL:                     http://www.gnu.org/software/emacs/emacs.html
SUNW_BaseDir:            %_basedir
%include default-depend.inc

%define _with_gtk 1

BuildRequires:      SFEgcc
Requires:           SFEgccruntime
BuildRequires: SUNWgnome-common-devel
BuildRequires: SUNWgtk2
BuildRequires: SUNWtexi
Requires: SUNWTiff
Requires: SUNWpng
Requires: SUNWjpg
Requires: SUNWlibms
Requires: SUNWzlib
Requires: %pnm_requires_perl_default
Requires: SUNWtexi
Requires: SUNWdbus
Requires: %{name}-root
%if %{?_with_gtk:1}%{?!_with_gtk}
%define toolkit gtk
Requires: SUNWgtk2
Requires: SUNWglib2
Requires: SUNWcairo
%else
%define toolkit motif
Requires: SUNWxwrtl
Requires: SUNWxwplt
Requires: SUNWxwice
%endif
BuildRequires: SFEgiflib-devel
Requires: SFEgiflib
BuildRequires: SFElibmagick-gpp-devel
Requires: SFElibmagick-gpp

%package root
Summary:                 %{summary} - root
SUNW_BaseDir:            /
%include default-depend.inc

%prep
%setup -q -n emacs-%version

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')
export CC=gcc
export CFLAGS="$CFLAGS -O6"
export CXX=g++
export LDFLAGS="$LDFLAGS -L/usr/gnu/lib -R/usr/gnu/lib:/usr/g++/lib -lncurses"

export PERL=/usr/perl5/bin/perl

export PKG_CONFIG_PATH=/usr/g++/lib/pkgconfig:/usr/gnu/lib/pkgconfig:/usr/lib/pkgconfig

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --infodir=%{_infodir}            \
            --sysconfdir=%{_sysconfdir}      \
            --localstatedir=%{_localstatedir}   \
            --with-gif=yes			\
            --with-x-toolkit=%toolkit		\
            --with-xft				\
	    --without-sound

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install prefix=%buildroot%_prefix \
	mandir=%buildroot%_mandir \
	libexecdir=%buildroot%_libexecdir \
	infodir=%buildroot%_infodir \
	localstatedir=%buildroot%_localstatedir
# Avoid conflict with system gnu-emacs.  (It uses /usr/gnu/bin)
mkdir -p %buildroot/usr/g++/bin
mv %buildroot%_bindir/ctags %buildroot%_bindir/etags %buildroot/usr/g++/bin
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%clean
rm -rf %buildroot

%files
%defattr (-, root, bin)
%dir %_prefix
%_bindir
%_libdir
%dir %attr (0755, root, sys) %{_datadir}
%dir %_datadir/emacs
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/emacs.desktop
%dir %attr (0755, root, other) %{_datadir}/icons
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/scalable/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/scalable/apps/
%{_datadir}/icons/hicolor/scalable/apps/*
%{_datadir}/icons/hicolor/scalable/mimetypes/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/16x16
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/16x16/apps/
%{_datadir}/icons/hicolor/16x16/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/32x32/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/32x32/apps/
%{_datadir}/icons/hicolor/32x32/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/24x24/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/24x24/apps/
%{_datadir}/icons/hicolor/24x24/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/48x48/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/48x48/apps/
%{_datadir}/icons/hicolor/48x48/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/128x128/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/128x128/apps/
%{_datadir}/icons/hicolor/128x128/apps/*
%{_datadir}/emacs/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%attr (0755, root, bin) %{_infodir}
%dir /usr/g++
%dir /usr/g++/bin
/usr/g++/bin/ctags
/usr/g++/bin/etags

%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, root, bin) %{_localstatedir}/games
%dir %attr (0755, root, sys) %{_localstatedir}/games/emacs
%{_localstatedir}/games/emacs/*

%changelog
* Tue Aug 24 2015 - Alex Viskovatoff <herzen@imap.cc>
- bump to 24.5; follow Oracle's practice of ignoring third number of version
- install two files in /usr/g++/bin to avoid conflicts with system Emacs
* Sun Aug 16 2015 - Thomas Wagner
- fix order %include usr-g.*inc base.inc
* Thu Sep 12 2014 - Alex Viskovatoff
- disable sound - the only reason I added alsa was because the documentation
  indicated that sound does not work on Solaris
* Mon Apr 22 2013 - Logan Bruns <logan@gedanken.org>
- updated to 24.3
* Sun Feb 24 2013 - Logan Bruns <logan@gedanken.org>
- added missing (build)requires for sfegcc(runtime)
* Wed Feb 20 2013 - Logan Bruns <logan@gedanken.org>
- minor tweaks and cleanups.
* Fri Feb  8 2013 - Logan Bruns <logan@gedanken.org>
- updated to 24.2
- added IPS name
* Sun Apr 01 2012 - Pavel Heimlich
- bump to 23.3b, workaround for Studio 12.3
* Sun Oct  2 2011 - Alex Viskovatoff
- Work around usr-gnu.inc not placing info dir in /usr/gnu
* Mon Sep 12 2011 - Alex Viskovatoff
- bump to version 23.3a
* Sat Jul 23 2011 - Guido Berhoerster <gber@openindiana.org>
- added License and SUNW_Copyright tags
* Mon Jun 27 2011 - Alex Viskovatoff
- Install in /usr/gnu so as not to conflict with system gnu-emacs
* Sun Apr 12 2011 - Alex Viskovatoff
- Add missing build dependencies
* Thu Mar 17 2011 - Alex Viskovatoff
- Bump to 23.3; reenable sound support
* Wed Sep 15 2010 - knut.hatlen@oracle.com
- Add missing dependencies.
* Mon Jul 19 2010 - markwright@internode.on.net
- Bump to 23.2
* Tue Aug 04 2009 - jedy.wang@sun.com
- Bump to 23.1
* Thu Oct 2 2008 - markwright@internode.on.net
- Bump to 22.3
* Wed Oct 17 2007 - laca@sun.com
- change /var/games owner to root:bin to match Maelstrom
* Tue Oct 16 2007 - laca@sun.com
- enable building with gtk if the --with-gtk build option is used (default
  remains motif)
- disable sound support (alsa breaks the build currently)
* Wed Jul 24 2007 - markwright@internode.on.net
- Bump to 22.1, change CPP="cc -E -Xs", add --with-gcc=no --with-x-toolkit=motif, add %{_localstatedir}/games/emacs.
* Mon Jun 12 2006 - laca@sun.com
- rename to SFEemacs
- add missing deps
* Wed Oct 12 2005 - laca@sun.com
- create
