#
# spec file for package SFEperl-Net-DNS
#
# includes module(s): Net-DNS
#

#TODO# re-work perl specific prerequisites...

%define module_version 0.65
%define module_name Net-DNS
%define module_name_major Net
%define module_package_name net-dns
#still unused: %define module_name_minor DNS


%include Solaris.inc
%include packagenamemacros.inc
Name:                    SFEperl-%{module_package_name}
IPS_package_name:        library/perl-5/%{module_package_name}
Summary:                 %{module_name}-%{module_version} PERL module
Version:                 %{perl_version}.%{module_version}
Source:                  http://www.cpan.org/modules/by-module/%{module_name_major}/%{module_name}-%{module_version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
BuildRequires:           %{pnm_buildrequires_perl_default}
Requires:  	         %{pnm_requires_perl_default}
BuildRequires:           %{pnm_buildrequires_SUNWsfwhea}
BuildRequires:           SFEperl-io-socket-inet6
Requires:                SFEperl-io-socket-inet6

#TODO# re-work perl specific prerequisites...
#prerequisites from the modules README
#  (Test::More)
#  IO::Socket
#  MIME::Base64
#  Digest::MD5
#  Digest::HMAC_MD5
#  Net::IP


%ifarch sparc
%define perl_dir sun4-solaris-64int
%else
%define perl_dir i86pc-solaris-64int 
%endif
%include default-depend.inc

%prep
%setup -q            -c -n %name-%version

%build
cd %{module_name}-%{module_version}

#NOTE# special to this module: --no-online-tests

perl Makefile.PL \
    UNINST=0 \
    PREFIX=$RPM_BUILD_ROOT%{_prefix} \
    INSTALLSITELIB=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version} \
    INSTALLSITEARCH=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version}/%{perl_dir} \
    INSTALLSITEMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
    INSTALLSITEMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3 \
    INSTALLMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
    INSTALLMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3 \
    --no-online-tests \
    --no-IPv6-tests

make CC=$CC CCCDLFLAGS="%picflags" OPTIMIZE="%optflags" LD=$CC

%install
rm -rf $RPM_BUILD_ROOT
cd %{module_name}-%{module_version}
make install

rm -rf $RPM_BUILD_ROOT%{_prefix}/lib

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr(0755, root, bin) %{_prefix}/%{perl_path_vendor_perl_version}/%{perl_dir}
%dir %attr(0755, root, bin) %{_prefix}/%{perl_path_vendor_perl_version}/%{perl_dir}/%{module_name_major}
%{_prefix}/%{perl_path_vendor_perl_version}/%{perl_dir}/%{module_name_major}/*
%dir %attr(0755, root, bin) %{_prefix}/%{perl_path_vendor_perl_version}/%{perl_dir}/auto
%{_prefix}/%{perl_path_vendor_perl_version}/%{perl_dir}/auto/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*

%changelog
* Mon Dec 13 2011 - Thomas Wagner
- add IPS_package_name library/perl-5/net-dns
* Fri Jun 23 2011 - Thomas Wagner
- change (Build)Requires to %{pnm_buildrequires_perl_default} and make module 
  paths dynamic, define fewer directories in %files
- change BuildRequires: %{pnm_buildrequires_SUNWsfwhea}
* Sun Apr 26 2009 - Thomas Wagner
- add --no-IPv6-tests
* Sat Apr 18 2009 - Thomas Wagner
- bump to 0.65 (0.59 too old for SpamAssassin)
* Thu Feb 21 2008 - Thomas Wagner
- (Build-)Requires corrected to be lowercase (SFEperl-io-socket-inet6)
* Wed Nov 28 2007 - Thomas Wagner
- renamed package and if necessary (Build-)Requires
* Sat Nov 24 2007 - Thomas Wagner
- moved from site_perl to vendor_perl
- special to this module: --no-online-tests for Makefile.PL
- released into the wild
* Sat, 19 May 2007  - Thomas Wagner
- Initial spec file
