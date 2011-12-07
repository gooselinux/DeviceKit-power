%define glib2_version           2.6.0
%define dbus_version            0.90
%define dbus_glib_version       0.70
%define polkit_version          0.92
%define parted_version          1.8.8

Summary: Power Management Service
Name: DeviceKit-power
Version: 014
Release: 1%{?dist}
License: GPLv2+
Group: System Environment/Libraries
URL: http://cgit.freedesktop.org/DeviceKit/DeviceKit-power/
Source0: http://hal.freedesktop.org/releases/%{name}-%{version}.tar.gz
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: dbus-devel  >= %{dbus_version}
BuildRequires: dbus-glib-devel >= %{dbus_glib_version}
BuildRequires: polkit-devel >= %{polkit_version}
BuildRequires: sqlite-devel
BuildRequires: libtool
BuildRequires: intltool
BuildRequires: gettext
BuildRequires: libgudev1-devel
BuildRequires: libusb-devel

Requires: dbus >= %{dbus_version}
Requires: dbus-glib >= %{dbus_glib_version}
Requires: glib2 >= %{glib2_version}
Requires: polkit >= %{polkit_version}
Requires: udev
Requires: pm-utils >= 1.2.2.1

%description
DeviceKit-power provides a daemon, API and command line tools for
managing power devices attached to the system.

%package devel
Summary: Headers and libraries for DeviceKit-power
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
Headers and libraries for DeviceKit-power.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

mkdir -p $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-%{version}
cp README AUTHORS NEWS COPYING HACKING doc/TODO $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)

%doc %dir %{_datadir}/doc/%{name}-%{version}
%doc %{_datadir}/doc/%{name}-%{version}/NEWS
%doc %{_datadir}/doc/%{name}-%{version}/COPYING
%doc %{_datadir}/doc/%{name}-%{version}/AUTHORS
%doc %{_datadir}/doc/%{name}-%{version}/HACKING
%doc %{_datadir}/doc/%{name}-%{version}/README
%doc %{_datadir}/doc/%{name}-%{version}/TODO
%{_libdir}/libdevkit-power-gobject*.so.*
%{_sysconfdir}/dbus-1/system.d/*.conf
/lib/udev/rules.d/*.rules
%dir %{_localstatedir}/lib/DeviceKit-power
%{_bindir}/*
%{_libexecdir}/*

%{_mandir}/man1/*
%{_mandir}/man7/*
%{_mandir}/man8/*

%{_datadir}/polkit-1/actions/*.policy
%{_datadir}/dbus-1/system-services/*.service

%files devel
%defattr(-,root,root,-)
%{_datadir}/dbus-1/interfaces/*.xml
%dir %{_datadir}/gtk-doc/html/devkit-power
%{_datadir}/gtk-doc/html/devkit-power/*
%{_libdir}/libdevkit-power-gobject*.so
%{_libdir}/pkgconfig/*.pc
%dir %{_includedir}/DeviceKit-power/devkit-power-gobject
%{_includedir}/DeviceKit-power/devkit-power-gobject/*.h

%changelog
* Fri Jan 08 2010 Richard Hughes <rhughes@redhat.com> - 014-1
- Check if swap exists before determining how much is free
- Prevent segfault if connection to system dbus fails
- Fix segfault in the history code.
- Resolves: #553589

* Mon Dec 07 2009 Richard Hughes <richard@hughsie.com> - 013-1
- Update to 013
- Detect more supported UPS devices.
- Fix the Toshiba battery recall data.
- Fix a crash when the battery NVRAM is invalid.
- Add a couple of fixes for very new battery support.

* Wed Nov 18 2009 Richard Hughes  <rhughes@redhat.com> - 013-0.1.20091118git
- Update to a git snapshot
- Don't crash the daemon if the battery is broken. Fixes #533654
- Avoid going from discharging to pending-discharge when the battery is very low
- Fix the toshiba battery recall notices

* Wed Oct 28 2009 Matthias Clasen <mclasen@redhat.com> - 012-2
- Make hibernate work again

* Mon Oct 19 2009 Richard Hughes <richard@hughsie.com> - 012-1
- Update to 012
- Detect encrypted swap and prevent hibernate in this case.
- When we do a delayed refresh, actually do 5 x 1 second apart rather
  than 1 x 3 seconds which should fix some slow battery devices.

* Mon Sep 14 2009 Richard Hughes  <rhughes@redhat.com> - 011-0.1.20090914git
- Update to todays git snapshot to fix the session exploding when a USB UPS is
  inserted then removed a few times.

* Mon Aug 03 2009 Richard Hughes <richard@hughsie.com> - 010-4
- Continue to poll when we guessed a status value, and only stop when the
  kernel says definitively that we are fully charged.

* Sun Aug 02 2009 Richard Hughes <richard@hughsie.com> - 010-3
- Put the development include files in the devel package not the main package.
- Fixes #515104

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 010-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 Richard Hughes <richard@hughsie.com> - 010-1
- Update to 010
- Fixes a few problems with multi-battery laptops
- Port to GUdev and PolicyKit1

* Mon Jul 06 2009 Richard Hughes <richard@hughsie.com> - 009-1
- Update to 009
- Fixes many problems with multi-battery laptops
- Use pm-powersave like HAL used to
- Fix detecting UPS devices
- Add support for recalled laptop batteries

* Tue Jun 16 2009 Richard Hughes  <rhughes@redhat.com> - 009-0.4.20090616git
- Do autoreconf as well due to different values of automake on koji.

* Tue Jun 16 2009 Richard Hughes  <rhughes@redhat.com> - 009-0.3.20090616git
- Do autoconf and automake as the polkit patch is pretty invasive
- Fix up file lists with the new polkit action paths

* Tue Jun 16 2009 Richard Hughes  <rhughes@redhat.com> - 009-0.2.20090616git
- Apply a patch to convert to the PolKit1 API.

* Tue Jun 16 2009 Richard Hughes  <rhughes@redhat.com> - 009-0.1.20090616git
- Update to todays git snapshot to fix reporting issues with empty batteries.

* Mon Jun 01 2009 Richard Hughes <richard@hughsie.com> 008-1
- Update to 008
- Fixes #497563 and #495493

* Wed May 13 2009 Richard Hughes  <rhughes@redhat.com> - 008-0.3.20090513git
- Update to todays git snapshot which should fix some polling issues.
- Fixes #495493

* Thu May 07 2009 Richard Hughes  <rhughes@redhat.com> - 008-0.2.20090507git
- Update to todays git snapshot which has the lid close property.

* Tue Apr 01 2009 Richard Hughes  <rhughes@redhat.com> - 008-0.1.20090401git
- Update to todays git snapshot which works with the new permissive DBus.

* Mon Mar 30 2009 Richard Hughes <richard@hughsie.com> 007-2
- Try to fix a compile error with koji and the new gcc.

* Mon Mar 30 2009 Richard Hughes <richard@hughsie.com> 007-1
- Update to 007

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 006-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 006-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 10 2009 Richard Hughes <richard@hughsie.com> 006-1
- Update to 006

* Mon Feb 02 2009 Richard Hughes <richard@hughsie.com> 005-1
- Update to 005

* Fri Jan 23 2009 Richard Hughes <richard@hughsie.com> 004-1
- Update to 004

* Tue Dec 09 2008 Richard Hughes <richard@hughsie.com> 003-1
- Update to 003

* Thu Nov 13 2008 Matthias Clasen <mclasen@redhat.com> 002-1
- Update to 002

* Sat Sep 06 2008 Richard Hughes <richard@hughsie.com> 001-2
- Fix the licence, and some directory ownership issues for the review request

* Tue Sep 02 2008 Richard Hughes <richard@hughsie.com> 001-1
- Initial spec file

