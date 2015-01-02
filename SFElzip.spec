#
# spec file for package SFElzip
#
# includes module(s): lzip
#

%include Solaris.inc
%define cc_is_gcc 1
%include usr-gnu.inc

%include arch64.inc
%include base.inc
%use lzip_64 = lzip.spec


%use lzip = lzip.spec


Name:                    %{lzip.name}
IPS_Package_Name:	compress/gnu/lzip
Summary:    	         %{lzip.summary} (/usr/gnu)
Version:                 %{lzip.version}
URL:			 %{lzip.url}
Source:         http://download.savannah.gnu.org/releases/lzip/lzip-%{version}.tar.gz
#SUNW_Copyright: lzip-utils.copyright
Group:		Applications/Archivers
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc


%description
Lzip is a lossless data compressor with a user interface similar to the one of gzip or bzip2. Lzip is about as fast as gzip, compresses most files more than bzip2, and is better than both from a data recovery perspective. Lzip is a clean implementation of the LZMA algorithm.

%prep
rm -rf %{name}-%{version}
mkdir -p %{name}-%{version}/%_arch64
%lzip_64.prep -d %{name}-%{version}


%build
%lzip_64.build -d %{name}-%{version}


%install
rm -rf %{buildroot}
%lzip_64.install -d %{name}-%{version}

rm ${RPM_BUILD_ROOT}%{_datadir}/info/dir

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(0755, root, bin)
%{_bindir}/lzip
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/info/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man*/*


%changelog
* Fri Jan  1 2014 - Thomas Wagner
- initial spec
- derived from SFExz.spec
- build 64-bit only, bindir is /usr/gnu/bin/
