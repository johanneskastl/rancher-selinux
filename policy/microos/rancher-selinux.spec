# vim: sw=4:ts=4:et

%define selinux_policyver 20210716-3.1
%define container_policyver 2.164.2-1.1

%define relabel_files() \
mkdir -p /var/lib/rancher/rke /etc/kubernetes /opt/rke; \
restorecon -R /var/lib/rancher /etc/kubernetes /opt/rke;

Name:       rancher-selinux
Version:	v0.2.testing.1
Release:	0
Summary:	SELinux policy module for Rancher

Group:	System Environment/Base
License:	Apache-2.0
URL:		https://github.com/rancher/rancher-selinux
Source:     %{name}-%{version}.tar.gz

BuildArch: noarch
BuildRequires: container-selinux >= %{container_policyver}
BuildRequires:  git
BuildRequires:  selinux-policy >= %{selinux_policyver}
BuildRequires:  selinux-policy-devel >= %{selinux_policyver}

Requires: policycoreutils, selinux-tools
Requires(post): selinux-policy-base >= %{selinux_policyver}
Requires(post): policycoreutils
Requires(post): container-selinux >= %{container_policyver}
Requires(postun): policycoreutils

Provides: %{name} = %{version}-%{release}

%description
This package installs and sets up the SELinux policy security module for Rancher.

%prep
%setup -q

%build
cd policy/microos
make -f /usr/share/selinux/devel/Makefile rancher.pp

%install
install -d %{buildroot}%{_datadir}/selinux/packages
install -m 644 policy/microos/rancher.pp %{buildroot}%{_datadir}/selinux/packages

%post
semodule -n -i %{_datadir}/selinux/packages/rancher.pp
if /usr/sbin/selinuxenabled ; then
    /usr/sbin/load_policy
    %relabel_files
fi;
exit 0

%postun
if [ $1 -eq 0 ]; then
    semodule -n -r rancher
    if /usr/sbin/selinuxenabled ; then
       /usr/sbin/load_policy
    fi;
fi;
exit 0

%files
%attr(0600,root,root) %{_datadir}/selinux/packages/rancher.pp

%changelog
