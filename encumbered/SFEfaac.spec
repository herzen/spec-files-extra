#
# spec file for package SFEfaac.spec
#
# includes module(s): faac
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%use faac_64 = faac.spec
%endif

%include base.inc
%use faac = faac.spec

Name:		SFEfaac
IPS_Package_Name:	audio/faac 
Summary:	%{faac.summary}
Version:	%{faac.version}
License:	%{faac.license}
SUNW_Copyright:	faac.copyright
Group:		%{faac.group}
URL:		%{faac.url}
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

# No support for the latest mp4v2 API
#BuildRequires:	SFElibmp4v2-devel
#Requires:	SFElibmp4v2

%description
FAAC is an AAC audio encoder. It currently supports MPEG-4 LTP, MAIN and LOW
COMPLEXITY object types and MAIN and LOW MPEG-2 object types. It also supports
multichannel and gapless encoding.


%package devel
Summary: Development libraries of the FAAC AAC encoder
Group: Development/Libraries
Requires: %{name}

%description devel
FAAC is an AAC audio encoder. It currently supports MPEG-4 LTP, MAIN and LOW
COMPLEXITY object types and MAIN and LOW MPEG-2 object types. It also supports
multichannel and gapless encoding.

This package contains development files and documentation for libfaac.


%prep
rm -rf %name-%version
mkdir %name-%version
%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%faac_64.prep -d %name-%version/%_arch64
gsed -i -e 's?-Wall??' -e 's?-lstdc++??' %name-%version/%_arch64/faac-%{version}/configure* %name-%version/%_arch64/faac-%{version}/common/mp4v2/Makefile* %name-%version/%_arch64/faac-%{version}/frontend/Makefile*
%endif

mkdir %name-%version/%{base_arch}
%faac.prep -d %name-%version/%{base_arch}
gsed -i -e 's?-Wall??' -e 's?-lstdc++??' %name-%version/%base_arch/faac-%{version}/configure* %name-%version/%base_arch/faac-%{version}/common/mp4v2/Makefile* %name-%version/%_arch64/faac-%{version}/frontend/Makefile*

%build

export AR=/usr/bin/ar
export LD=`which ld-wrapper`

%ifarch amd64 sparcv9
%faac_64.build -d %name-%version/%_arch64
%endif

%faac.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%faac_64.install -d %name-%version/%_arch64
%endif

%faac.install -d %name-%version/%{base_arch}

%clean
rm -rf %{buildroot}


%files
%defattr(-, root, bin)
%{_bindir}/*
%{_libdir}/*.so*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}/man1

%files devel
%defattr(-, root, bin)
%{_includedir}/*.h

%changelog
* Mon Dec 23 2013 - Thomas Wagner
- export AR=/usr/bin/ar (or get C++ Symbol errors on S12)
- export LD=`which ld-wrapper`
- remove -Wall and -lstdc++ if built with Studio compiler
* Mon Dec 23 2013 - Thomas Wagner
- remove "-Wall" and "-lstdc++" from configure* mp4v2/Makefile* frontend/Makefile*
* Sun Aug 11 2013 - Thomas Wagner
- fix linking to C++ libs %if %{cc_is_gcc}  ( s/-lCrun/-lstdc++/ )
- %if %{cc_is_gcc} change Name, IPS_Package_Name to SFEfaac-gpp, audio/g++/faac
- %if %{cc_is_gcc} add (Build)Requires: SFEgcc(runtime)
* Wed Aug 16 2012 - Milan Jurik
- build with internal mp4v2
* Mon Oct 17 2011 - Milan Jurik
- revert previous change to unbreak build
- add IPS package name
* Sat Aug 13 2011 - Thomas Wagner
- fix build by:
- use /usr/bin/libtoolize and not new SFE version from /usr/gnu/bin/
- use CC/CXX /usr/gnu/bin/gcc g++
* Sat Jul 23 2011 - Guido Berhoerster <gber@openindiana.org>
- added License and SUNW_Copyright tags
* Thu Jun 18 2010 - Milan Jurik
- Initial version
