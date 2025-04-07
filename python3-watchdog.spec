#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

Summary:	Python API and shell utilities to monitor file system events
Summary(pl.UTF-8):	API pythonowe i narzędzia powłoki do monitorowania zdarzeń systemu plików
Name:		python3-watchdog
Version:	6.0.0
Release:	1
License:	Apache v2.0
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/watchdog/
Source0:	https://files.pythonhosted.org/packages/source/w/watchdog/watchdog-%{version}.tar.gz
# Source0-md5:	d3adf236e17e5747e397f7d0b93e05b4
URL:		https://pypi.org/project/watchdog/
BuildRequires:	python3-modules >= 1:3.6
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-PyYAML >= 3.10
BuildRequires:	python3-eventlet
BuildRequires:	python3-pytest
BuildRequires:	python3-pytest-cov
BuildRequires:	python3-pytest-timeout
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.6
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python API and shell utilities to monitor file system events.

%description -l pl.UTF-8
API pythonowe i narzędzia powłoki do monitorowania zdarzeń systemu
plików.

%package apidocs
Summary:	API documentation for Python watchdog module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona watchdog
Group:		Documentation

%description apidocs
API documentation for Python watchdog module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona watchdog.

%prep
%setup -q -n watchdog-%{version}

%build
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pytest_cov.plugin,pytest_timeout \
PYTHONPATH=$(pwd)/src \
%{__python3} -m pytest tests -k 'not test_unmount_watched_directory_filesystem and not test_auto_restart_on_file_change_debounce and not test_select_fd'
# disabled test uses sudo for mount/umount
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/watchmedo{,-3}
ln -sf watchmedo-3 $RPM_BUILD_ROOT%{_bindir}/watchmedo

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING README.rst
%attr(755,root,root) %{_bindir}/watchmedo
%attr(755,root,root) %{_bindir}/watchmedo-3
%{py3_sitescriptdir}/watchdog
%{py3_sitescriptdir}/watchdog-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/{_modules,_static,*.html,*.js}
%endif
