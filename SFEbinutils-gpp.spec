# /* vim: set filetype=spec : */ 
#
# spec file for package SFEbinutils-gpp
#
# includes module(s): GNU binutils-gpp
#
%include Solaris.inc
%define cc_is_gcc 1
%include base.inc
%define _prefix /usr/g++
%include osdistro.inc


Name:                SFEbinutils-gpp
IPS_package_name:    developer/g++/gnu-binutils
Summary:             GNU binutils (/usr/g++)
Version:             2.23.2
Source:              http://ftp.gnu.org/gnu/binutils/binutils-%{version}.tar.bz2
Patch1:              binutils-01-bug-2495.diff
#Patch2:              binutils-02-ld-m-elf_i386.diff
#Patch3:              binutils-03-lib-amd64-ld-so-1.diff
Patch4:              binutils-04-non-constant_initializer_op.diff
Patch5:              binutils-05-lm.diff
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

#Requires: runtime ... gcc-3

%if %{os2nnn}
#no need for postrun
%else
BuildRequires: SUNWpostrun
Requires: SUNWpostrun
%endif

%package devel
Summary:                 %{summary} - developer files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -c -n %name-%version
cd binutils-%{version}
%ifarch amd64
%patch1 -p1 -b .patch01
%endif
%patch4 -p1 -b .patch04
%patch5 -p1 -b .patch05
cd ..
%ifarch i386 amd64
cd binutils-%{version}
#%patch2 -p1 -b .patch02
#%patch3 -p1 -b .patch03
cd ..
%endif
%ifarch amd64 sparcv9
cp -pr binutils-%{version} binutils-%{version}-64
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

%if %build_l10n
nlsopt=-enable-nls
%else
nlsopt=-disable-nls
%endif

export CC=gcc
export CXX=g++
export CFLAGS32="%optflags"
export CFLAGS64="%optflags"
export LDFLAGS32="-L/usr/g++/lib -R/usr/g++/lib"
export LDFLAGS64="-L/usr/g++/lib -R/usr/g++/lib"

%ifarch amd64 sparcv9
export CFLAGS="$CFLAGS64"
export LDFLAGS="$LDFLAGS64"

cd binutils-%{version}-64

gsed -i.bak -e 's/-Werror//g' gold/configure

./configure --prefix=%{_prefix}			\
            --libdir=%{_libdir}/%{_arch64}	\
            --libexecdir=%{_libdir}/%{_arch64}	\
            --mandir=%{_mandir}			\
	    --infodir=%{_infodir}		\
	    --enable-shared			\
	    --disable-static			\
	    --enable-lto			\
	    --enable-gold			\
	    $nlsopt

#around 2.23.x started to error with:
#In file included from ehframe.h:31,
#                 from ehframe.cc:32:
#merge.h: In constructor `gold::Output_merge_base::Output_merge_base(uint64_t, uint64_t)':
#merge.h:222: warning: converting of negative value `-0x00000000000000001' to `unsigned int'

gsed -i.bak -e 's/-Werror//g' gold/configure

make -j$CPUS
cd ..
%endif

cd binutils-%{version}

#export CC=${CC32:-$CC}
export CFLAGS="$CFLAGS32"
export LDFLAGS="$LDFLAGS32"

./configure --prefix=%{_prefix}			\
            --libdir=%{_libdir}			\
            --libexecdir=%{_libexecdir}		\
            --mandir=%{_mandir}			\
	    --infodir=%{_infodir}		\
	    --enable-shared			\
	    --disable-static			\
	    $nlsopt

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
cd binutils-%{version}-64
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT/%{_libdir}/%{_arch64}/*.a
rm -f $RPM_BUILD_ROOT/%{_libdir}/%{_arch64}/*.la
cd ..
%endif

cd binutils-%{version}
make install DESTDIR=$RPM_BUILD_ROOT

cd $RPM_BUILD_ROOT%{_prefix}
ln -s share/man man

rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.la

#
# Workaround for a potential problem
#
%ifarch amd64 sparcv9
rm -rf $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/%{_arch64}
%endif

# Clashes with autoconf
#rm $RPM_BUILD_ROOT%{_std_datadir}/info/standards.info
rm $RPM_BUILD_ROOT%{_datadir}/info/standards.info

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'as.info binutils.info autosprintf.info gprof.info bfd.info configure.info ld.info' ;
  echo '"';
  echo 'retval=0';
  echo 'for info in $infos; do';
  echo '  install-info --info-dir=%{_infodir} %{_infodir}/$info || retval=1';
  echo 'done';
  echo 'exit $retval' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%preun
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'as.info binutils.info autosprintf.info gprof.info bfd.info configure.info ld.info' ;
  echo '"';
  echo 'for info in $infos; do';
  echo '  install-info --info-dir=%{_infodir} --delete %{_infodir}/$info';
  echo 'done';
  echo 'exit 0' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_prefix}
%{_prefix}/man
%{_prefix}/*-solaris*
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*.1
%dir %attr(0755, root, bin) %{_infodir}
%{_infodir}/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_prefix}
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Sat Feb  7 2015 - Thomas Wagner
- exclude SUNWpostrun on IPS 
* Sun Nov 10 2013 - Milan Jurik
- bump to 2.23.2
- fix IPS name
* Sun Feb 24 2013 - Logan Bruns <logan@gedanken.org>
- also build gold
* Sat Feb 23 2013 - Logan Bruns <logan@gedanken.org>
- added ips name
* Wed Feb 20 2013 - Ken Mays <kmays2000@gmail.com>
- bump to 2.23.1
* Thu Feb 09 2012 - James Choi
- bump to 2.22, use g++ path to not interfere with gnu-binutils pkg
- fork from archive/SFEbinutils, build with gcc
* Sat Jan 26 2008 - moinak.ghosh@sun.com
- Add workaround for a potential spurious build issue.
* Sun Oct 14 2007 - Mark Wright <markwright@internode.on.net>
- Bump to 2.18.  Comment patch2, as already applied to 2.18.
- Add patch4 to avoid avoid sun cc error:
 "elf.c", line 854: non-constant initializer: op "?"
- Add patch5 to add -lm to gprof link.  Add export CPP="cc -E -Xs".
* Wed Aug 15 2007 - Mark Wright <markwright@internode.on.net>
- Add patch1 http://sourceware.org/bugzilla/show_bug.cgi?id=2495
- Add patch2 http://www.cygwin.com/ml/binutils/2006-06/msg00299.html
- Add patch3 http://sourceware.org/ml/binutils/2007-03/msg00175.html
* Mon Mar 18 2007 - Doug Scott <dougs@truemail.co.th>
- Removed standards.info
* Tue Feb  7 2007 - Doug Scott <dougs@truemail.co.th>
- Initial spec
