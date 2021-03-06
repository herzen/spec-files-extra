#
# spec file for package SFEperl-Digest-SHA1
#
# includes module(s): Digest-SHA1
#

%define module_version 2.13
%define module_name Digest-SHA1
%define module_name_major Digest
%define module_package_name digest-sha1
#still unused: %define module_name_minor SHA1


%include Solaris.inc
%include packagenamemacros.inc
Name:                    SFEperl-%{module_package_name}
IPS_Package_Name:	library/perl-5/digest-sha1
Summary:                 %{module_name}-%{module_version} PERL module
License:                 GPL+ or Artistic
Group:		Development/Perl
SUNW_Copyright:          digest-sha1.copyright
Version:                 %{perl_version}.%{module_version}
Source:                  http://www.cpan.org/modules/by-module/%{module_name_major}/GAAS/%{module_name}-%{module_version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
BuildRequires:           %{pnm_buildrequires_perl_default}
Requires:                %{pnm_requires_perl_default}

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
perl Makefile.PL \
    UNINST=0 \
    PREFIX=$RPM_BUILD_ROOT%{_prefix} \
    INSTALLSITELIB=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version} \
    INSTALLSITEARCH=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version}/%{perl_dir} \
    INSTALLSITEMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
    INSTALLSITEMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3 \
    INSTALLMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
    INSTALLMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3
make CC=$CC CCCDLFLAGS="%picflags" OPTIMIZE="%optflags" LD=$CC

%install
rm -rf $RPM_BUILD_ROOT
cd %{module_name}-%{module_version}
make install

rm -rf $RPM_BUILD_ROOT%{_prefix}/lib
find $RPM_BUILD_ROOT -name .packlist -exec %{__rm} {} \;


%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr(0755, root, bin) %{_prefix}/%{perl_path_vendor_perl_version}
%dir %attr(0755, root, bin) %{_prefix}/%{perl_path_vendor_perl_version}/%{perl_dir}/%{module_name_major}
%{_prefix}/%{perl_path_vendor_perl_version}/%{perl_dir}/%{module_name_major}/*
%dir %attr(0755, root, bin) %{_prefix}/%{perl_path_vendor_perl_version}/%{perl_dir}/auto
%{_prefix}/%{perl_path_vendor_perl_version}/%{perl_dir}/auto/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*

%changelog
* Sat May 12 2012 - Thomas Wagner
- remove file .packlist
* Fri Jul 29 2011 - Alex Viskovatoff
- add SUNW_Copyright
* Fri Jun 23 2011 - Thomas Wagner
- change (Build)Requires to %{pnm_buildrequires_perl_default} and make module 
  paths dynamic, define fewer directories in %files
* Sat Mar 05 2011 - Milan Jurik
- bump to 2.13
* Tue Mar 02 2010 - matt@greenviolet.net
- Bump version to 2.12
- Removed dependency on obsolete SUNSsfwhea
* Wed Nov 28 2007 - Thomas Wagner
- renamed package and if necessary (Build-)Requires
* Sat Nov 24 2007 - Thomas Wagner
- moved from site_perl to vendor_perl
- released into the wild
* Sat, 19 May 2007  - Thomas Wagner
- Initial spec file
- parametrize module-name and version ( %define module_version 2.11 %define module_name Digest-SHA1)
