#
# spec file for package SFEsdl-sound
#
# includes module(s): SDL
#
%include Solaris.inc
%include packagenamemacros.inc

%ifarch amd64 sparcv9
%include arch64.inc
%use sdl_64 = sdl-sound.spec
%endif

%if %arch_sse2
%include x86_sse2.inc
%use sdl_sse2 = sdl-sound.spec
%endif

%include base.inc
%use sdl = sdl-sound.spec

%define SUNWlibsdl	%(/usr/bin/pkginfo -q SUNWlibsdl && echo 1 || echo 0)

Name:			SFEsdl-sound
IPS_Package_Name:	library/audio/sdl-sound
Summary: 		%{sdl.summary}
Version:		%{sdl.version}
SUNW_BaseDir:		%{_basedir}
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: %{pnm_buildrequires_SUNWlibsdl_devel}
Requires:      %{pnm_requires_SUNWlibsdl}
BuildRequires: SUNWogg-vorbis-devel
Requires: SUNWogg-vorbis
BuildRequires:  %{pnm_buildrequires_SUNWlibmikmod_devel}
Requires:       %{pnm_requires_SUNWlibmikmod}
BuildRequires: SUNWflac-devel
Requires: SUNWflac
BuildRequires: SUNWspeex-devel
Requires: SUNWspeex
BuildRequires: SFEphysfs-devel
Requires: SFEphysfs

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %{name}

%prep
rm -rf %name-%version
mkdir %name-%version

%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%sdl_64.prep -d %name-%version/%_arch64
%endif

%if %arch_sse2
mkdir %name-%version/%sse2_arch
%sdl_sse2.prep -d %name-%version/%sse2_arch
%endif

mkdir %name-%version/%base_arch
%sdl.prep -d %name-%version/%base_arch

%build
%ifarch amd64 sparcv9
%sdl_64.build -d %name-%version/%_arch64
%endif

%if %arch_sse2
%sdl_sse2.build -d %name-%version/%sse2_arch
%endif

%sdl.build -d %name-%version/%base_arch

%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
%sdl_64.install -d %name-%version/%_arch64
%endif

%if %arch_sse2
%sdl_sse2.install -d %name-%version/%sse2_arch
%endif

%sdl.install -d %name-%version/%base_arch

%clean:
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/playsound*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/*
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif
%if %arch_sse2
%dir %attr (0755, root, bin) %{_bindir}/%{sse2_arch}
%{_bindir}/%{sse2_arch}/*
%dir %attr (0755, root, bin) %{_libdir}/%{sse2_arch}
%{_libdir}/%{sse2_arch}/lib*.so*
%endif
%doc -d %{base_arch}/SDL_sound-%{version} README CHANGELOG COPYING CREDITS
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc

%files devel
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/SDL/

%changelog
* Mon Jul 30 2012 - Thomas Wagner
- change (Build)Requires to %{pnm_buildrequires_SUNWlibmikmod_devel}, %include packagenamemacros.inc
- change (Build)Requires to %{pnm_buildrequires_SUNWlibsdl_devel}
* Mon Oct 17 2011 - Milan Jurik
- add IPS package name
* Sun May 16 2010 - Milan Jurik
- added missing build dependencies
* Tue Mar 02 2010 - matt@greenviolet.net
- Update packaging
* Tue Dec 30 2008 - brian.cameron@sun.com
- Fix packaging.
* Mon May 05 2008 - brian.cameron@sun.com
- Remove dependency on SFEogg-vorbis.spec since now SUNWogg-vorbis.spec has
  the 64-bit libraries.
* Mon Feb 25 2008 - Albert Lee
- Initial spec
