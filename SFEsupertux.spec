#
# spec file for package: SFEsupertux
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#


%include Solaris.inc
%define cc_is_gcc 1
%include base.inc

%define src_name supertux

Name:           SFEsupertux
IPS_Package_Name:	games/supertux
Summary:        Classic 2D jump 'n run sidescroller with Tux
Version:        0.1.3
License:        GPLv2
Source:         http://download.berlios.de/%{src_name}/%{src_name}-%{version}.tar.bz2
Patch1:		supertux-01-gcc.diff
URL:            http://supertux.lethargik.org
Group:          Amusements/Games
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
SUNW_Basedir:   %{_basedir}

# OpenSolaris IPS Manifest Fields
Meta(info.upstream): The SuperTux Team
Meta(info.repository_url): http://supertux.lethargik.org/viewvc/viewvc.cgi/trunk/supertux
Meta(info.maintainer): Andras Barna <andras.barna@gmail.com>
Meta(pkg.detailed_url): http://supertux.lethargik.org
Meta(info.classification): org.opensolaris.category.2008:Applications/Games

%include default-depend.inc
BuildRequires: SFEsdl-mixer-devel
BuildRequires: SFEsdl-image-devel
Requires: SFEsdl-mixer
Requires: SFEsdl-image

%description
SuperTux is a classic 2D jump'n run sidescroller game in a style similar to the original SuperMario games.

%prep
rm -rf %{src_name}-%{version}
%setup -q -n %{src_name}-%{version}
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CC=gcc
export CXX=g++
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags"

%build
./configure --prefix=%{_prefix} \
            --mandir=%{_mandir} \
            --libdir=%{_libdir} \
            --libexecdir=%{_libexecdir} \

make -j$CPUS

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755,root,sys) %{_datadir}
%{_datadir}/supertux/*
%dir %attr (0755,root,other) %{_datadir}/applications
%dir %attr (0755,root,other) %{_datadir}/pixmaps
%{_datadir}/applications/*
%{_datadir}/pixmaps/*
%doc COPYING INSTALL LEVELDESIGN NEWS README ChangeLog AUTHORS 
%dir %attr (0755, root, other) %{_datadir}/doc

%changelog
* Sat Nov 19 2011 - Milan Jurik
- add IPS package name
- fix GCC build
* Sun May 16 2010 - Milan Jurik
- readded stable supertux version to SFE
* Wed Mar 25 2009 - andras.barna@gmail.com
- initial version
