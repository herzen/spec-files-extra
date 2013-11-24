#
# spec file for package SFElyx
#
# includes module: lyx
#

# To be able to typeset LyX documents, you need to have TeX installed.
# Since SFEtexlive.spec is not currently maintained, it is probably best
# to install TeX Live using its own native installer.  See
#   http://www.tug.org/texlive/acquire-netinstall.html.
# You need to make sure that the various TeX executables are in your PATH.
# The TeX Live installer gives you the option of creating symbolic links
# to them automatically; creating symbolic links of TeX executables to
# a directory in your PATH is probably the best way of making LyX find them.

# Since the libraries of SFEqt47-gpp are now in a non-standard location,
# you will need to do, for example:
# pfexec elfedit -e 'dyn:runpath /usr/gnu/lib' pdftex

%include Solaris.inc
#%include packagenamemacros.inc

%define cc_is_gcc 1
%include base.inc
%define srcname lyx
%define _pkg_docdir %_docdir/%srcname

Name:		SFElyx
IPS_Package_Name:	desktop/publishing/lyx
Summary:	Graphical LaTeX front end
URL:		http://www.lyx.org
License:	GPLv2
Group:		Applications/Office
SUNW_Copyright:	lyx.copyright
Version:	2.0.6
Source:		ftp://ftp.lyx.org/pub/lyx/stable/2.0.x/%srcname-%version.tar.gz
Source1:	%srcname.desktop
SUNW_BaseDir:	%_basedir
%include default-depend.inc

BuildRequires:	SFEqt-gpp-devel
BuildRequires:	SFEboost-gpp-devel
# Build fails if libiconv is not installed
#BuildRequires:	SFElibiconv-devel
BuildRequires:	SUNWgnome-spell
BuildRequires:	python-26
Requires:	python-26

%if %build_l10n
%package l10n
Summary:        %summary - l10n files
SUNW_BaseDir:   %_basedir
%include default-depend.inc
Requires:       %name
%endif

%description
LyX is a document processor that encourages an approach to writing based on the
structure of your documents (WYSIWYM) and not simply their appearance (WYSIWYG).
LyX combines the power and flexibility of TeX/LaTeX with the ease of use of a
graphical interface. This results in world-class support for creation of
mathematical content (via a fully integrated equation editor) and structured
documents like academic articles, theses, and books. In addition, staples of
scientific authoring such as reference list and index creation come
standard. But you can also use LyX to create a letter or a novel or a theatre
play or film script. A broad array of ready, well-designed document layouts are
built in.  LyX is for people who want their writing to look great, right out of
the box. No more endless tinkering with formatting details, “finger painting”
font attributes or futzing around with page boundaries. You just write. On
screen, LyX looks like any word processor; its printed output — or richly
cross-referenced PDF, just as readily produced — looks like nothing else.


%prep
%setup -q -n %srcname-%version


%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CC=gcc
export CXX=g++
export CPPFLAGS="-I/usr/g++/include -I/usr/g++/include/qt"
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags -pthreads -fpermissive"
export LDFLAGS="%_ldflags -pthreads -lxnet -L/usr/g++/lib -R/usr/g++/lib"

# LyX can use enchant, so no need for hunspell; aspell is obsolete
./configure --prefix=%_prefix --with-qt4-dir=/usr/g++ --enable-threads=posix --without-included-boost --without-aspell --without-hunspell

make -j$CPUS


%install
rm -rf %buildroot

make install DESTDIR=%buildroot
mkdir %buildroot%_datadir/applications
cp %SOURCE1 %buildroot%_datadir/applications

%if %build_l10n
%else
rm -rf %buildroot%_datadir/locale
%endif

%clean
rm -rf %buildroot


%files
%defattr (-, root, bin)
%doc ABOUT-NLS ANNOUNCE NEWS README RELEASE-NOTES UPGRADING
%_bindir/lyx
%_bindir/lyxclient
%_bindir/tex2lyx
%dir %attr (-, root, sys) %_datadir
%_datadir/%srcname
%_mandir
%dir %attr(0755, root, other) %_datadir/applications
%_datadir/applications/%srcname.desktop

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %_datadir
%attr (-, root, other) %_datadir/locale
%endif


%changelog
* Wed Dec  5 2012 - Logan Bruns <logan@gedanken.org>
- updated to 2.0.5
* Sun Aug 05 2012 - Milan Jurik
- bump to 2.0.4
* Sat Jun 23 2012 - Thomas Wagner
- make (Build)Requries  %{pnm_buildrequires_python_default}
* Sun Jan 08 2012 - Milan Jurik
- bump to 2.0.2
* Sun Jul 31 2011 - Alex Viskovatoff
- Add missing (build) dependency
* Sat Jul 23 2011 - Alex Viskovatoff
- Use system Boost; add SUNW_Copyright
* Sun Apr  3 2011 - Alex Viskovatoff <herzen@imap.cc>
- Disable aspell; LyX can use library/spell-checking/enchant
* Wed Mar 30 2011 - Alex Viskovatoff
- Adapt to gcc-built Qt now being in /usr/g++
- Update to 2.0.0rc2; disable hunspell; remove build dependency on Boost
* Tue Feb  8 2011 - Alex Viskovatoff
- Adapt to Qt gcc libs now being in /usr/stdcxx
* Sun Jan 30 2011 - Alex Viskovatoff
- Initial spec
