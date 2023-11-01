# -*- coding: utf-8 -*-
%global __python /usr/bin/python3
%{?scl:%{?scl_package:%scl_package ltrace}}

Summary: A GNU tool which simplifies the build process for users
Name: %{?scl_prefix}make
Epoch: 1
Version: 4.2.1
Release: 1%{?dist}
License: GPLv3+
URL: http://www.gnu.org/software/make/
Source: ftp://ftp.gnu.org/gnu/make/make-%{version}.tar.bz2

Patch0: make-4.2-getcwd.patch
Patch1: make-4.0-newlines.patch

# Assume we don't have clock_gettime in configure, so that
# make is not linked against -lpthread (and thus does not
# limit stack to 2MB).
Patch2: make-4.0-noclock_gettime.patch

# BZs #142691, #17374
Patch3: make-4.2-j8k.patch

# Upstream: https://savannah.gnu.org/bugs/?30748
# The default value of .SHELL_FLAGS is -c.
Patch4: make-4.0-weird-shell.patch

# Upstream patch: https://git.savannah.gnu.org/cgit/make.git/patch/?id=193f1e81edd6b1b56b0eb0ff8aa4b41c7b4257b4
# Fixes wrong assumptions of glibc's glob internals.
Patch5: make-4.2.1-glob-fix-2.patch
# Upstream patch: https://git.savannah.gnu.org/cgit/make.git/patch/?id=48c8a116a914a325a0497721f5d8b58d5bba34d4
# Fixes incorrect use of glibc 2.27 glob internals.
Patch6: make-4.2.1-glob-fix.patch
Patch7: make-4.2.1-glob-fix-3.patch

# Perl 5.26 removed the implicit CWD in @INC.
Patch8: make-4.2.1-test-driver.patch

# Upstream patch: https://git.savannah.gnu.org/cgit/make.git/commit/?id=fbf71ec25a5986d9003ac16ee9e23675feac9053
# Adds support of guile 2.2
Patch9: 0001-configure.ac-SV-50648-Detect-Guile-2.2-packages.patch

# Upstream patch: https://git.savannah.gnu.org/cgit/make.git/commit/?id=b552b05251980f693c729e251f93f5225b400714
# Avoids hangs in parallel builds
Patch10: make-4.2.1-nonblocking-reads.patch

# autoreconf
BuildRequires: autoconf, automake, gettext-devel
BuildRequires: procps
BuildRequires: perl-interpreter
BuildRequires: gcc

%description
A GNU tool for controlling the generation of executables and other
non-source files of a program from the program's source files. Make
allows users to build and install packages without any significant
knowledge about the details of the build process. The details about
how the program should be built are provided for make in the program's
makefile.

%package devel
Summary: Header file for externally visible definitions

%description devel
The make-devel package contains gnumake.h.

%prep
%autosetup -p1 -n make-%{version}

rm -f tests/scripts/features/parallelism.orig

%build
autoreconf -vfi

%configure
%make_build

%install
%make_install
ln -sf make ${RPM_BUILD_ROOT}/%{_bindir}/gmake
ln -sf make.1 ${RPM_BUILD_ROOT}/%{_mandir}/man1/gmake.1
rm -f ${RPM_BUILD_ROOT}/%{_infodir}/dir

%find_lang make

%check
echo ============TESTING===============
/usr/bin/env LANG=C make -k check && true
echo ============END TESTING===========

%files  -f make.lang
%license COPYING
%doc NEWS README AUTHORS
%{_bindir}/*
%{_mandir}/man*/*
%{_infodir}/*.info*
%{_includedir}/gnumake.h

%files devel
%{_includedir}/gnumake.h

%changelog
* Wed May 27 2020 DJ Delorie <dj@redhat.com> - 1:4.2.1-1
- Initial sources (#1818987)

