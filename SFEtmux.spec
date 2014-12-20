#
# spec file for package: tmux
#
# Copyright 2010 Guido Berhoerster.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc
%define srcname tmux
%define _pkg_docdir %_docdir/%srcname

Name:           SFE%srcname
IPS_Package_Name:	terminal/tmux
Summary:        Terminal multiplexer
IPS_Component_Version: 1.9.0.1
Version:        1.9a
License:        ISC ; BSD3c ; BSD 2-Clause
Url:            http://tmux.sourceforge.net/
Source:         %{sf_download}/tmux/%{srcname}-%{version}.tar.gz
Patch5:         tmux-05-include-errno.h.diff
Patch6:         tmux-06-client.c-missing-flock-modify-tio-cfmakeraw.diff
Group:          Applications/System Utilities
Distribution:   OpenIndiana
Vendor:         OpenIndiana Community
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
SUNW_Copyright:	tmux.copyright
SUNW_Basedir:   %{_basedir}
%include default-depend.inc

Requires:       SFElibevent2
BuildRequires:  SFElibevent2

# OpenSolaris IPS Package Manifest Fields
Meta(info.upstream):            Nicholas Marriott <nicm@users.sf.net>
Meta(info.maintainer):          Guido Berhoerster <gber@openindiana.org>
Meta(info.repository_url):      http://tmux.cvs.sourceforge.net/viewvc/tmux/tmux/

%description
tmux is a terminal multiplexer: it enables a number of terminals (or windows),
each running a separate program, to be created, accessed, and controlled from a
single screen. tmux may be detached from a screen and continue running in the
background, then later reattached. tmux is intended to be a modern,
BSD-licensed alternative to programs such as GNU screen.

tmux uses a client-server model. The server holds multiple sessions and each
window is a independent entity which may be freely linked to multiple sessions,
moved between sessions and otherwise manipulated. Each session may be attached
to (display and accept keyboard input from) multiple clients.

%prep
%setup -q -n %{srcname}-%{version}
%patch5 -p1
%patch6 -p1

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CFLAGS="%optflags -I/usr/gnu/include"
# Need to supply -lcurses, because otherwise, it tries to link against ncurses,
# leading to "Undefined Symbol: delterm" error
export LDFLAGS="%_ldflags -lcurses -L/usr/gnu/lib -R/usr/gnu/lib"
./configure
make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
install -d -m 755 %{buildroot}%{_bindir}
install -m 0755 tmux %{buildroot}%{_bindir}/tmux
install -d -m 755 %{buildroot}%{_mandir}/man1
install -m 0644 tmux.1 %{buildroot}%{_mandir}/man1/tmux.1
mkdir %buildroot%_docdir

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%_bindir/tmux
%dir %attr (-, root, sys) %_datadir
%dir %attr (0755, root, other) %dir %_docdir
%doc CHANGES FAQ TODO
%doc examples/screen-keys.conf examples/t-williams.conf examples/vim-keys.conf
%doc examples/h-boetes.conf examples/tmux.vim examples/n-marriott.conf
%doc %_mandir/man1/tmux.1


%changelog
* Sat Dec 20 2014 - Thomas Wagner
- bump to 1.9a, add IPS_Component_Version 1.9.0.1
- remove patch1, remove/replace patch2 and patch3 by new patch6 (adopted from Solaris Userland), 
- add patch5 errno.h
* Tue Dec 18 2012 - Logan Bruns <logan@gedanken.org>
- updated to 1.7, added ips name and updated patches
* Mon Oct 31 2011 - Alex Viskovatoff
- Add patch fixing window name updates in statusbar for debug OS builds
* Sun Oct  2 2011 - Alex Viskovatoff
- Adapt to SFElibevent2 being moved to /usr/gnu; update to 1.5
* Mon Jul 25 2011 - N.B.Prashanth
- Add SUNW_Copyright
* Sun Apr 10 2011 - Alex Viskovatoff
- Use SFElibevent2
* Mon Mar 14 2011 - Alex Viskovatoff
- Import spec from http://hg.openindiana.org/spec-files-oi-extra/
  installing in /usr and bumping to 1.4
* Wed Oct  6 2010 - gber@openindiana.org
- Initial version.
