#
# spec file for package gnupg2
#

Name:         gnupg
Version:      2.0.22
Release:      1
Summary:      gnupg - GNU Utility for data encryption and digital signatures.
License:      GPL
Group:        Applications/Cryptography
Copyright:    GPL
Autoreqprov:  on
URL:          http://www.gnupg.org/
Source:       ftp://ftp.gnupg.org/gcrypt/gnupg/%{name}-%{version}.tar.bz2
BuildRoot:    %{_tmppath}/%{name}-%{version}-build

%description
GnuPG (GNU Privacy Guard) is a GNU utility for encrypting data and
creating digital signatures. GnuPG has advanced key management
capabilities and is compliant with the proposed OpenPGP Internet
standard described in RFC-2440.  Since GnuPG doesn't use any patented
algorithms, it is not compatible with some versions of PGP 2 which use
only the patented IDEA algorithm.  See
http://www.gnupg.org/why-not-idea.html for information on using IDEA
if the patent does not apply to you and you need to be compatible with
these versions of PGP 2.

%prep
%setup -n %{name}-%{version}

%build
%if %build_l10n
CFLAGS="$RPM_OPT_FLAGS" ./configure \
                        --prefix=%{_prefix} \
                        --libexecdir=%{_libexecdir} \
                        --mandir=%{_mandir}         \
                        --infodir=%{_datadir}/info  \
                        --with-included-gettext     \
#  --with-libassuan-prefix=PFX
%else
CFLAGS="$RPM_OPT_FLAGS" ./configure \
                        --prefix=%{_prefix} \
                        --libexecdir=%{_libexecdir} \
			--mandir=%{_mandir}         \
			--infodir=%{_datadir}/info  \
#  --with-libassuan-prefix=PFX
%endif

make 

%install
[ "$RPM_BUILD_ROOT" != "/" ] && [ -d $RPM_BUILD_ROOT ] && rm -rf $RPM_BUILD_ROOT;
make DESTDIR=$RPM_BUILD_ROOT install
cd doc
make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -fr $RPM_BUILD_ROOT
make distclean

%post
/sbin/install-info %{_infodir}/gpg.info %{_infodir}/dir 2>/dev/null || :
/sbin/install-info %{_infodir}/gpgv.info %{_infodir}/dir 2>/dev/null || :

%preun
if [ $1 = 0 ]; then
   /sbin/install-info --delete %{_infodir}/gpg.info \
        %{_infodir}/dir 2>/dev/null || :
   /sbin/install-info --delete %{_infodir}/gpgv.info \
        %{_infodir}/dir 2>/dev/null || :
fi

%files
%defattr (-,root,root)

%doc INSTALL AUTHORS COPYING NEWS README THANKS TODO PROJECTS doc/DETAILS
%doc doc/FAQ doc/faq.html doc/HACKING doc/OpenPGP doc/samplekeys.asc
%doc %attr (0755,root,root) tools/convert-from-106
%config %{_datadir}/%{name}/options.skel
%{_mandir}/man1/*
%{_mandir}/man7/*
%{_infodir}/gpg.info*
%{_infodir}/gpgv.info*
%attr (4755,root,root) %{_bindir}/gpg
%attr (0755,root,root) %{_bindir}/gpgv
%attr (0755,root,root) %{_bindir}/gpgsplit
%attr (0755,root,root) %{_libexecdir}/gnupg/*

%changelog -n gnupg
* Mon Oct 14 2013 - Thomas Wagner
- bump to 2.0.22
* Mon Jan 21 2008 - moinak.ghosh@sun.com
- Fixed l10n build.
* Sat Dec 29 2007 - jijun.yu@sun.com
- Intial spec
