Summary:	XIE extension library
Summary(pl):	Biblioteka rozszerzenia XIE
Name:		XFree86-XIE
Version:	4.3.0
Release:	1
License:	MIT
Group:		X11/Libraries
# XIE files/directories extracted from X430src-{1,2,3,6,7}.tgz:
# xc/include/extensions/XIE*.h
# xc/lib/XIE
# xc/programs/xieperf
# xc/programs/Xserver/XIE
# xc/doc/specs/XIE
# xc/doc/hardcopy/XIE
Source0:	%{name}-%{version}.tar.bz2
# Source0-md5:	6ae53620997b77ebc7b0b6cac8d1a4a0
URL:		http://www.xfree86.org/
BuildRequires:	XFree86-Xserver-devel >= 4.3.0
BuildRequires:	XFree86-devel >= 4.3.0
Requires:	XFree86-libs >= 4.3.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man

%description
XIE (X Image Extension) extension library.

%description -l pl
Biblioteka rozszerzenia XIE (X Image Extension).

%package devel
Summary:	XIE extension headers
Summary(pl):	Pliki nag³ówkowe rozszerzenia XIE
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}
Requires:	XFree86-devel >= 4.3.0

%description devel
XIE extension headers.

%description devel -l pl
Pliki nag³ówkowe rozszerzenia XIE.

%package static
Summary:	XIE extension static library
Summary(pl):	Statyczna biblioteka rozszerzenia XIE
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
XIE extension static library.

%description static -l pl
Statyczna biblioteka rozszerzenia XIE.

%package doc
Summary:	XIE extension documentation
Summary(pl):	Dokumentacja do rozszerzenia XIE
Group:		X11/XFree86

%description doc
XIE extension documentation.

%description doc -l pl
Dokumentacja do rozszerzenia XIE.

%package -n XFree86-module-XIE
Summary:	XIE extension module
Summary(pl):	Modu³ rozszerzenia XIE
Group:		X11/XFree86
Requires:	XFree86-modules >= 4.3.0

%description -n XFree86-module-XIE
XIE (X Image Extension) extension module for X server.

%description -n XFree86-module-XIE -l pl
Modu³ rozszerzenia XIE (X Image Extension) dla X serwera.

%prep
%setup -q

%build
cd xc
ln -s . include/X11
XDIR="`pwd`"
cd lib/XIE
imake -DUseInstalled -I/usr/X11R6/lib/X11/config \
	-DNormalLibXie=YES \
	-DSharedLibXie=YES \
	-DDebugLibXie=NO \
	-DProfileLibXie=NO \
	-DSharedXieReqs="-L/usr/X11R6/lib -lX11"
ln -sf ../../lib/XIE/XIElib.h ../../include/X11/extensions
%{__make} \
	CDEBUGFLAGS="%{rpmcflags} -I../../include" \
	SOXIEREV="6.0"

cd ../../programs/xieperf
xmkmf
ln -sf ../../include X11
%{__make} \
	CDEBUGFLAGS="%{rpmcflags} -I../../include" \
	XIELIB="-L../../lib/XIE -lXIE"

cd ../Xserver/XIE
xmkmf
%{__make} Makefiles
%{__make} includes
%{__make} depend \
	EXTRA_INCLUDES="-I${XDIR}/include/extensions -I${XDIR}/include -I/usr/X11R6/include/X11/Xserver -I/usr/X11R6/include/X11"

%{__make} \
	CDEBUGFLAGS="%{rpmcflags} -I${XDIR}/include/extensions -I${XDIR}/include -I/usr/X11R6/include/X11/Xserver -I/usr/X11R6/include/X11"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_includedir}/X11/extensions

install xc/include/extensions/{XIE,XIEproto,XIEprotost}.h \
	$RPM_BUILD_ROOT%{_includedir}/X11/extensions

%{__make} -C xc/lib/XIE install \
	DESTDIR=$RPM_BUILD_ROOT \
	SOXIEREV="6.0"

%{__make} -C xc/programs/xieperf install install.man \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -C xc/programs/Xserver/XIE install \
	DESTDIR=$RPM_BUILD_ROOT

find xc/doc/hardcopy -name Imakefile | xargs rm -f

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/xieperf
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%{_mandir}/man1/xieperf.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/X11/extensions/*.h

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%files doc
%defattr(644,root,root,755)
%doc xc/doc/hardcopy/XIE/*

%files -n XFree86-module-XIE
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/modules/extensions/libxie.a
