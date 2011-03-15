#
# spec file for package SFEweechat
#
# includes module: weechat
#

# NOTE: To get this to build, you need to supply -erroff to the compiler.
# This is odd, since -erroff is only supposed to suppress warnings, not errors.

# NOTE: The Ruby plugin does not work, since it is unable to find libruby.so

# NOTE: It is not clear if spell checking works.  WeeChat is aware of aspell,
# at least.

# TODO: Update and use the patch below to use Enchant instead of aspell:
# http://savannah.nongnu.org/patch/?6858

%include Solaris.inc
%define srcname weechat

Name:		SFE%srcname
Summary:	Lightweight console IRC client
URL:		http://www.weechat.org/
Vendor:		Sebastien Helleu <flashcode@flashtux.org>
Version:	0.3.4
License:	GPLv2
Source:		http://www.weechat.org/files/src/%srcname-%version.tar.bz2
Patch1:		weechat-01-fix-strftime.diff
Patch2:		weechat-02-remove-date-time.diff
Patch3:		weechat-03-fix-array-overflow.diff
SUNW_BaseDir:	%_basedir
BuildRoot:	%_tmppath/%name-%version-build
%include default-depend.inc

BuildRequires:	SFEcmake
BuildRequires:	SFEaspell-devel
Requires:	SFEaspell

%if %build_l10n
%package l10n
Summary:        %summary - l10n files
SUNW_BaseDir:   %_basedir
%include default-depend.inc
Requires:       %name
%endif

%description
WeeChat (Wee Enhanced Environment for Chat) is a fast and light cross-platform
chat environment. It can be entirely controlled with the keyboard, has a
plugin-based architecture and is customizable and extensible with scripts in
several scripting languages.
 
Authors:
--------
Sebastien Helleu <flashcode@flashtux.org>


%prep
%setup -q -n %srcname-%version
%patch1 -p1
%patch2 -p0
%patch3 -p1
mkdir build


%build

CPUS=$(psrinfo | awk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

sed 's| -Wall -W -Werror-implicit-function-declaration||' CMakeLists.txt > foo
mv foo CMakeLists.txt
cd build


# Removing -erroff makes the build fail.
# Which is strange, since erroff supresses warnings, not errors.
cmake -DPREFIX=/usr -DCMAKE_C_FLAGS="%optflags -I/usr/include/ncurses -erroff" -DCMAKE_EXE_LINKER_FLAGS="%_ldflags -lxnet -L/usr/gnu/lib -L/usr/ruby/1.8/lib -R/usr/gnu/lib:/usr/ruby/1.8/lib" ..
#cmake -DPREFIX=/usr -DCMAKE_C_FLAGS="%optflags -I/usr/include/ncurses" -DCMAKE_EXE_LINKER_FLAGS="%_ldflags -lxnet -L/usr/gnu/lib -L/usr/ruby/1.8/lib -R/usr/gnu/lib:/usr/ruby/1.8/lib" ..
#cmake -DPREFIX=/usr -DCMAKE_C_FLAGS="%optflags -I/usr/include/ncurses" -DCMAKE_EXE_LINKER_FLAGS="%_ldflags -lxnet %gnu_lib_path" ..
gmake -j$CPUS


%install
rm -rf $RPM_BUILD_ROOT
cd build
gmake install DESTDIR=%buildroot INSTALL="%_bindir/ginstall -c -p"

%if %build_l10n
%else
rm -rf $RPM_BUILD_ROOT%_datadir/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%_bindir/weechat-curses
%_libdir/%srcname
%dir %attr (-, root, other) %_libdir/pkgconfig
%_libdir/pkgconfig/%srcname.pc
%_includedir/%srcname
%dir %attr (-, root, sys) %_datadir
%_mandir/man1/weechat-curses.1

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %_datadir
%attr (-, root, other) %_datadir/locale
%endif


%changelog
* Sun Mar 13 2011 - Alex Viskovatoff
- Initial spec
