%global security_hardening none
Summary:        Kernel
Name:           linux
Version:        4.19.52
Release:        2%{?kat_build:.%kat_build}%{?dist}
License:    	GPLv2
URL:        	http://www.kernel.org/
Group:        	System Environment/Kernel
Vendor:         VMware, Inc.
Distribution: 	Photon
Source0:        http://www.kernel.org/pub/linux/kernel/v4.x/linux-%{version}.tar.xz
%define sha1 linux=0fc8eeba8a8a710c95d71f140dfdc4bdff735248
Source1:	config
Source2:	initramfs.trigger
%define ena_version 1.6.0
Source3:	https://github.com/amzn/amzn-drivers/archive/ena_linux_%{ena_version}.tar.gz
%define sha1 ena_linux=c8ec9094f9db8d324d68a13b0b3dcd2c5271cbc0
Source4:	config_aarch64
Source5:	xr_usb_serial_common_lnx-3.6-and-newer-pak.tar.xz
%define sha1 xr=74df7143a86dd1519fa0ccf5276ed2225665a9db
Source6:        update_photon_cfg.postun
# common
Patch0:         linux-4.14-Log-kmsg-dump-on-panic.patch
Patch1:         double-tcp_mem-limits.patch
# TODO: disable this patch, check for regressions
#Patch2:         linux-4.9-watchdog-Disable-watchdog-on-virtual-machines.patch
Patch3:         SUNRPC-Do-not-reuse-srcport-for-TIME_WAIT-socket.patch
Patch4:         SUNRPC-xs_bind-uses-ip_local_reserved_ports.patch
Patch5:         vsock-transport-for-9p.patch
Patch6:         4.18-x86-vmware-STA-support.patch
# ttyXRUSB support
Patch11:	usb-acm-exclude-exar-usb-serial-ports.patch
#HyperV patches
Patch13:        0004-vmbus-Don-t-spam-the-logs-with-unknown-GUIDs.patch
# TODO: Is CONFIG_HYPERV_VSOCKETS the same?
#Patch23:        0014-hv_sock-introduce-Hyper-V-Sockets.patch
#FIPS patches - allow some algorithms
Patch24:        4.18-Allow-some-algo-tests-for-FIPS.patch
Patch26:        4.18-add-sysctl-to-disallow-unprivileged-CLONE_NEWUSER-by-default.patch
# Fix CVE-2017-1000252
Patch28:        kvm-dont-accept-wrong-gsi-values.patch
# Out-of-tree patches from AppArmor:
Patch29:        4.17-0001-apparmor-patch-to-provide-compatibility-with-v2.x-ne.patch
Patch30:        4.17-0002-apparmor-af_unix-mediation.patch
Patch31:        4.17-0003-apparmor-fix-use-after-free-in-sk_peer_label.patch
# RDRAND-based RNG driver to enhance the kernel's entropy pool:
Patch32:        4.18-0001-hwrng-rdrand-Add-RNG-driver-based-on-x86-rdrand-inst.patch
# Fix for CVE-2019-12456
Patch33:        0001-scsi-mpt3sas_ctl-fix-double-fetch-bug-in-_ctl_ioctl_.patch
# Fix for CVE-2019-12379
Patch34:        0001-consolemap-Fix-a-memory-leaking-bug-in-drivers-tty-v.patch
# Fix for CVE-2019-12380
Patch35:        0001-efi-x86-Add-missing-error-handling-to-old_memmap-1-1.patch
# Fix for CVE-2019-12381
Patch36:        0001-ip_sockglue-Fix-missing-check-bug-in-ip_ra_control.patch
# Fix for CVE-2019-12382
Patch37:        0001-drm-edid-Fix-a-missing-check-bug-in-drm_load_edid_fi.patch
# Fix for CVE-2019-12378
Patch38:        0001-ipv6_sockglue-Fix-a-missing-check-bug-in-ip6_ra_cont.patch
# Fix for CVE-2019-12455
Patch39:        0001-clk-sunxi-fix-a-missing-check-bug-in-sunxi_divs_clk_.patch

%ifarch aarch64
# NXP LS1012a FRWY patches
Patch51:        0001-staging-fsl_ppfe-eth-header-files-for-pfe-driver.patch
Patch52:        0002-staging-fsl_ppfe-eth-introduce-pfe-driver.patch
Patch53:        0003-staging-fsl_ppfe-eth-fix-RGMII-tx-delay-issue.patch
Patch54:        0004-staging-fsl_ppfe-eth-remove-unused-functions.patch
Patch55:        0005-staging-fsl_ppfe-eth-fix-read-write-ack-idx-issue.patch
Patch56:        0006-staging-fsl_ppfe-eth-Make-phy_ethtool_ksettings_get-.patch
Patch57:        0007-staging-fsl_ppfe-eth-add-function-to-update-tmu-cred.patch
Patch58:        0008-staging-fsl_ppfe-eth-Avoid-packet-drop-at-TMU-queues.patch
Patch59:        0009-staging-fsl_ppfe-eth-Enable-PFE-in-clause-45-mode.patch
Patch60:        0010-staging-fsl_ppfe-eth-Disable-autonegotiation-for-2.5.patch
Patch61:        0011-staging-fsl_ppfe-eth-add-missing-included-header-fil.patch
Patch62:        0012-staging-fsl_ppfe-eth-clean-up-iounmap-pfe-ddr_basead.patch
Patch63:        0013-staging-fsl_ppfe-eth-calculate-PFE_PKT_SIZE-with-SKB.patch
Patch64:        0014-staging-fsl_ppfe-eth-support-for-userspace-networkin.patch
Patch65:        0015-staging-fsl_ppfe-eth-unregister-netdev-after-pfe_phy.patch
Patch66:        0016-staging-fsl_ppfe-eth-HW-parse-results-for-DPDK.patch
Patch67:        0017-staging-fsl_ppfe-eth-reorganize-pfe_netdev_ops.patch
Patch68:        0018-staging-fsl_ppfe-eth-use-mask-for-rx-max-frame-len.patch
Patch69:        0019-staging-fsl_ppfe-eth-define-pfe-ndo_change_mtu-funct.patch
Patch70:        0020-staging-fsl_ppfe-eth-remove-jumbo-frame-enable-from-.patch
Patch71:        0021-staging-fsl_ppfe-eth-disable-CRC-removal.patch
Patch72:        0022-staging-fsl_ppfe-eth-handle-ls1012a-errata_a010897.patch
Patch73:        0023-staging-fsl_ppfe-eth-Modify-Kconfig-to-enable-pfe-dr.patch
%endif

%if 0%{?kat_build:1}
Patch1000:	%{kat_build}.patch
%endif
BuildRequires:  bc
BuildRequires:  kbd
BuildRequires:  kmod-devel
BuildRequires:  glib-devel
BuildRequires:  xerces-c-devel
BuildRequires:  xml-security-c-devel
BuildRequires:  libdnet-devel
BuildRequires:  libmspack-devel
BuildRequires:  Linux-PAM-devel
BuildRequires:  openssl-devel
BuildRequires:  procps-ng-devel
BuildRequires:	audit-devel
Requires:       filesystem kmod
Requires(post):(coreutils or toybox)
Requires(postun):(coreutils or toybox)
%define uname_r %{version}-%{release}

%description
The Linux package contains the Linux kernel.


%package devel
Summary:        Kernel Dev
Group:          System Environment/Kernel
Obsoletes:      linux-dev
Requires:       %{name} = %{version}-%{release}
Requires:       python3 gawk
%description devel
The Linux package contains the Linux kernel dev files

%package drivers-gpu
Summary:        Kernel GPU Drivers
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}
%description drivers-gpu
The Linux package contains the Linux kernel drivers for GPU

%package drivers-sound
Summary:        Kernel Sound modules
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}
%description drivers-sound
The Linux package contains the Linux kernel sound support

%package docs
Summary:        Kernel docs
Group:          System Environment/Kernel
Requires:       python3
%description docs
The Linux package contains the Linux kernel doc files

%ifarch x86_64
%package oprofile
Summary:        Kernel driver for oprofile, a statistical profiler for Linux systems
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}
%description oprofile
Kernel driver for oprofile, a statistical profiler for Linux systems
%endif

%package tools
Summary:        This package contains the 'perf' performance analysis tools for Linux kernel
Group:          System/Tools
Requires:       %{name} = %{version}-%{release}
Requires:       audit
%description tools
This package contains the 'perf' performance analysis tools for Linux kernel.

%ifarch aarch64
%package dtb-rpi3
Summary:        Kernel Device Tree Blob files for Raspberry Pi3
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}
%description dtb-rpi3
Kernel Device Tree Blob files for Raspberry Pi3

%package dtb-ls1012afrwy
Summary:        Kernel Device Tree Blob files for NXP ls1012a FRWY board
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}
%description dtb-ls1012afrwy
Kernel Device Tree Blob files for NXP ls1012a FRWY board

%endif


%prep
%setup -q -n linux-%{version}
%ifarch x86_64
%setup -D -b 3 -n linux-%{version}
%setup -D -b 5 -n linux-%{version}
%endif
%patch0 -p1
%patch1 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch11 -p1
%patch13 -p1
%patch24 -p1
%patch26 -p1
%patch28 -p1
%patch29 -p1
%patch30 -p1
%patch31 -p1
%patch32 -p1
%patch33 -p1
%patch34 -p1
%patch35 -p1
%patch36 -p1
%patch37 -p1
%patch38 -p1
%patch39 -p1

%ifarch aarch64
# NXP FSL_PPFE Driver patches
%patch51 -p1
%patch52 -p1
%patch53 -p1
%patch54 -p1
%patch55 -p1
%patch56 -p1
%patch57 -p1
%patch58 -p1
%patch59 -p1
%patch60 -p1
%patch61 -p1
%patch62 -p1
%patch63 -p1
%patch64 -p1
%patch65 -p1
%patch66 -p1
%patch67 -p1
%patch68 -p1
%patch69 -p1
%patch70 -p1
%patch71 -p1
%patch72 -p1
%patch73 -p1
%endif
%if 0%{?kat_build:1}
%patch1000 -p1
%endif

%build
make mrproper

%ifarch x86_64
cp %{SOURCE1} .config
arch="x86_64"
archdir="x86"
%endif

%ifarch aarch64
cp %{SOURCE4} .config
arch="arm64"
archdir="arm64"
%endif

sed -i 's/CONFIG_LOCALVERSION=""/CONFIG_LOCALVERSION="-%{release}"/' .config
make LC_ALL= oldconfig
make VERBOSE=1 KBUILD_BUILD_VERSION="1-photon" KBUILD_BUILD_HOST="photon" ARCH=${arch} %{?_smp_mflags}
make -C tools perf
%ifarch x86_64
# build ENA module
bldroot=`pwd`
pushd ../amzn-drivers-ena_linux_%{ena_version}/kernel/linux/ena
make -C $bldroot M=`pwd` VERBOSE=1 modules %{?_smp_mflags}
popd
# build XR module
bldroot=`pwd`
pushd ../xr_usb_serial_common_lnx-3.6-and-newer-pak
make KERNELDIR=$bldroot %{?_smp_mflags} all
popd
%endif

%define __modules_install_post \
for MODULE in `find %{buildroot}/lib/modules/%{uname_r} -name *.ko` ; do \
    ./scripts/sign-file sha512 certs/signing_key.pem certs/signing_key.x509 $MODULE \
    rm -f $MODULE.{sig,dig} \
    xz $MODULE \
    done \
%{nil}

# We want to compress modules after stripping. Extra step is added to
# the default __spec_install_post.
%define __spec_install_post\
    %{?__debug_package:%{__debug_install_post}}\
    %{__arch_install_post}\
    %{__os_install_post}\
    %{__modules_install_post}\
%{nil}

%install
install -vdm 755 %{buildroot}/etc
install -vdm 755 %{buildroot}/boot
install -vdm 755 %{buildroot}%{_defaultdocdir}/%{name}-%{uname_r}
install -vdm 755 %{buildroot}/usr/src/%{name}-headers-%{uname_r}
install -vdm 755 %{buildroot}/usr/lib/debug/lib/modules/%{uname_r}
make INSTALL_MOD_PATH=%{buildroot} modules_install

%ifarch x86_64
# install ENA module
bldroot=`pwd`
pushd ../amzn-drivers-ena_linux_%{ena_version}/kernel/linux/ena
make -C $bldroot M=`pwd` INSTALL_MOD_PATH=%{buildroot} modules_install
popd

# install XR module
bldroot=`pwd`
pushd ../xr_usb_serial_common_lnx-3.6-and-newer-pak
make KERNELDIR=$bldroot INSTALL_MOD_PATH=%{buildroot} modules_install
popd

# Verify for build-id match
# We observe different IDs sometimes
# TODO: debug it
ID1=`readelf -n vmlinux | grep "Build ID"`
./scripts/extract-vmlinux arch/x86/boot/bzImage > extracted-vmlinux
ID2=`readelf -n extracted-vmlinux | grep "Build ID"`
if [ "$ID1" != "$ID2" ] ; then
	echo "Build IDs do not match"
	echo $ID1
	echo $ID2
	exit 1
fi
install -vm 644 arch/x86/boot/bzImage %{buildroot}/boot/vmlinuz-%{uname_r}
%endif

%ifarch aarch64
install -vm 644 arch/arm64/boot/Image %{buildroot}/boot/vmlinuz-%{uname_r}
# Install DTB files
install -vdm 755 %{buildroot}/boot/dtb
install -vm 640 arch/arm64/boot/dts/broadcom/bcm2837-rpi-3-b.dtb %{buildroot}/boot/dtb/
install -vm 640 arch/arm64/boot/dts/freescale/fsl-ls1012a-frwy.dtb %{buildroot}/boot/dtb/
%endif

# Restrict the permission on System.map-X file
install -vm 400 System.map %{buildroot}/boot/System.map-%{uname_r}
install -vm 644 .config %{buildroot}/boot/config-%{uname_r}
cp -r Documentation/*        %{buildroot}%{_defaultdocdir}/%{name}-%{uname_r}
install -vm 644 vmlinux %{buildroot}/usr/lib/debug/lib/modules/%{uname_r}/vmlinux-%{uname_r}
# `perf test vmlinux` needs it
ln -s vmlinux-%{uname_r} %{buildroot}/usr/lib/debug/lib/modules/%{uname_r}/vmlinux

cat > %{buildroot}/boot/%{name}-%{uname_r}.cfg << "EOF"
# GRUB Environment Block
photon_cmdline=init=/lib/systemd/systemd ro loglevel=3 quiet no-vmw-sta
photon_linux=vmlinuz-%{uname_r}
photon_initrd=initrd.img-%{uname_r}
EOF

# Register myself to initramfs
mkdir -p %{buildroot}/%{_localstatedir}/lib/initramfs/kernel
cat > %{buildroot}/%{_localstatedir}/lib/initramfs/kernel/%{uname_r} << "EOF"
--add-drivers "tmem xen-scsifront xen-blkfront xen-acpi-processor xen-evtchn xen-gntalloc xen-gntdev xen-privcmd xen-pciback xenfs hv_utils hv_vmbus hv_storvsc hv_netvsc hv_sock hv_balloon cn"
EOF

#    Cleanup dangling symlinks
rm -rf %{buildroot}/lib/modules/%{uname_r}/source
rm -rf %{buildroot}/lib/modules/%{uname_r}/build

find . -name Makefile* -o -name Kconfig* -o -name *.pl | xargs  sh -c 'cp --parents "$@" %{buildroot}/usr/src/%{name}-headers-%{uname_r}' copy
find arch/${archdir}/include include scripts -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}/usr/src/%{name}-headers-%{uname_r}' copy
find $(find arch/${archdir} -name include -o -name scripts -type d) -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}/usr/src/%{name}-headers-%{uname_r}' copy
find arch/${archdir}/include Module.symvers include scripts -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}/usr/src/%{name}-headers-%{uname_r}' copy
%ifarch x86_64
# CONFIG_STACK_VALIDATION=y requires objtool to build external modules
install -vsm 755 tools/objtool/objtool %{buildroot}/usr/src/%{name}-headers-%{uname_r}/tools/objtool/
install -vsm 755 tools/objtool/fixdep %{buildroot}/usr/src/%{name}-headers-%{uname_r}/tools/objtool/
%endif

cp .config %{buildroot}/usr/src/%{name}-headers-%{uname_r} # copy .config manually to be where it's expected to be
ln -sf "/usr/src/%{name}-headers-%{uname_r}" "%{buildroot}/lib/modules/%{uname_r}/build"
find %{buildroot}/lib/modules -name '*.ko' -print0 | xargs -0 chmod u+x

%ifarch aarch64
cp arch/arm64/kernel/module.lds %{buildroot}/usr/src/%{name}-headers-%{uname_r}/arch/arm64/kernel/
%endif

# disable (JOBS=1) parallel build to fix this issue:
# fixdep: error opening depfile: ./.plugin_cfg80211.o.d: No such file or directory
# Linux version that was affected is 4.4.26
make -C tools JOBS=1 DESTDIR=%{buildroot} prefix=%{_prefix} perf_install

%include %{SOURCE2}
%include %{SOURCE6}

%post
/sbin/depmod -a %{uname_r}
ln -sf %{name}-%{uname_r}.cfg /boot/photon.cfg

%post drivers-gpu
/sbin/depmod -a %{uname_r}

%post drivers-sound
/sbin/depmod -a %{uname_r}

%ifarch x86_64
%post oprofile
/sbin/depmod -a %{uname_r}
%endif

%files
%defattr(-,root,root)
/boot/System.map-%{uname_r}
/boot/config-%{uname_r}
/boot/vmlinuz-%{uname_r}
%config(noreplace) /boot/%{name}-%{uname_r}.cfg
%config %{_localstatedir}/lib/initramfs/kernel/%{uname_r}
%defattr(0644,root,root)
/lib/modules/%{uname_r}/*
%exclude /lib/modules/%{uname_r}/build
%exclude /lib/modules/%{uname_r}/kernel/drivers/gpu
%exclude /lib/modules/%{uname_r}/kernel/sound
%ifarch x86_64
%exclude /lib/modules/%{uname_r}/kernel/arch/x86/oprofile/
%endif

%files docs
%defattr(-,root,root)
%{_defaultdocdir}/%{name}-%{uname_r}/*

%files devel
%defattr(-,root,root)
/lib/modules/%{uname_r}/build
/usr/src/%{name}-headers-%{uname_r}

%files drivers-gpu
%defattr(-,root,root)
%exclude /lib/modules/%{uname_r}/kernel/drivers/gpu/drm/cirrus/
/lib/modules/%{uname_r}/kernel/drivers/gpu

%files drivers-sound
%defattr(-,root,root)
/lib/modules/%{uname_r}/kernel/sound

%ifarch x86_64
%files oprofile
%defattr(-,root,root)
/lib/modules/%{uname_r}/kernel/arch/x86/oprofile/
%endif

%files tools
%defattr(-,root,root)
/usr/libexec
%exclude %{_libdir}/debug
%ifarch x86_64
/usr/lib64/traceevent
%endif
%ifarch aarch64
/usr/lib/traceevent
%endif
%{_bindir}
/etc/bash_completion.d/*
/usr/share/perf-core/strace/groups/file
/usr/share/doc/*
%{_libdir}/perf/examples/bpf/*
%{_libdir}/perf/include/bpf/*

%ifarch aarch64
%files dtb-rpi3
%defattr(-,root,root)
/boot/dtb/bcm2837-rpi-3-b.dtb

%files dtb-ls1012afrwy
%defattr(-,root,root)
/boot/dtb/fsl-ls1012a-frwy.dtb

%endif

%changelog
*   Thu Jun 20 2019 Tapas Kundu <tkundu@vmware.com> 4.19.52-2
-   Enabled CONFIG_I2C_CHARDEV to support lm-sensors
*   Mon Jun 17 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.52-1
-   Update to version 4.19.52
-   Fix CVE-2019-12456, CVE-2019-12379, CVE-2019-12380, CVE-2019-12381,
-   CVE-2019-12382, CVE-2019-12378, CVE-2019-12455
*   Tue May 28 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.40-3
-   Change default I/O scheduler to 'deadline' to fix performance issue.
*   Tue May 14 2019 Keerthana K <keerthanak@vmware.com> 4.19.40-2
-   Fix to parse through /boot folder and update symlink (/boot/photon.cfg) if
-   mulitple kernels are installed and current linux kernel is removed.
*   Tue May 07 2019 Ajay Kaher <akaher@vmware.com> 4.19.40-1
-   Update to version 4.19.40
*   Thu Apr 11 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.32-3
-   Update config_aarch64 to fix ARM64 build.
*   Fri Mar 29 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.32-2
-   Fix CVE-2019-10125
*   Wed Mar 27 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.32-1
-   Update to version 4.19.32
*   Thu Mar 14 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.29-1
-   Update to version 4.19.29
*   Tue Mar 05 2019 Ajay Kaher <akaher@vmware.com> 4.19.26-1
-   Update to version 4.19.26
*   Thu Feb 21 2019 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.15-3
-   Fix CVE-2019-8912
*   Thu Jan 24 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.15-2
-   Add WiFi (ath10k), sensors (i2c,spi), usb support for NXP LS1012A board.
*   Tue Jan 15 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.15-1
-   Update to version 4.19.15
*   Fri Jan 11 2019 Srinidhi Rao <srinidhir@vmware.com> 4.19.6-7
-   Add Network support for NXP LS1012A board.
*   Wed Jan 09 2019 Ankit Jain <ankitja@vmware.com> 4.19.6-6
-   Enable following for x86_64 and aarch64:
-    Enable Kernel Address Space Layout Randomization.
-    Enable CONFIG_SECURITY_NETWORK_XFRM
*   Fri Jan 04 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.6-5
-   Enable AppArmor by default.
*   Wed Jan 02 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.6-4
-   .config: added Compulab fitlet2 device drivers
-   .config_aarch64: added gpio sysfs support
-   renamed -sound to -drivers-sound
*   Tue Jan 01 2019 Ajay Kaher <akaher@vmware.com> 4.19.6-3
-   .config: Enable CONFIG_PCI_HYPERV driver
*   Wed Dec 19 2018 Srinidhi Rao <srinidhir@vmware.com> 4.19.6-2
-   Add NXP LS1012A support.
*   Mon Dec 10 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.6-1
-   Update to version 4.19.6
*   Fri Dec 07 2018 Alexey Makhalov <amakhalov@vmware.com> 4.19.1-3
-   .config: added qmi wwan module
*   Mon Nov 12 2018 Ajay Kaher <akaher@vmware.com> 4.19.1-2
-   Fix config_aarch64 for 4.19.1
*   Mon Nov 05 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.1-1
-   Update to version 4.19.1
*   Tue Oct 16 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.18.9-5
-   Change in config to enable drivers for zigbee and GPS
*   Fri Oct 12 2018 Ajay Kaher <akaher@vmware.com> 4.18.9-4
-   Enable LAN78xx for aarch64 rpi3
*   Fri Oct 5 2018 Ajay Kaher <akaher@vmware.com> 4.18.9-3
-   Fix config_aarch64 for 4.18.9
-   Add module.lds for aarch64
*   Wed Oct 03 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.18.9-2
-   Use updated steal time accounting patch.
-   .config: Enable CONFIG_CPU_ISOLATION and a few networking options
-   that got accidentally dropped in the last update.
*   Mon Oct 1 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.18.9-1
-   Update to version 4.18.9
*   Tue Sep 25 2018 Ajay Kaher <akaher@vmware.com> 4.14.67-2
-   Build hang (at make oldconfig) fix in config_aarch64
*   Wed Sep 19 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.67-1
-   Update to version 4.14.67
*   Tue Sep 18 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.54-7
-   Add rdrand-based RNG driver to enhance kernel entropy.
*   Sun Sep 02 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.54-6
-   Add full retpoline support by building with retpoline-enabled gcc.
*   Thu Aug 30 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.54-5
-   Apply out-of-tree patches needed for AppArmor.
*   Wed Aug 22 2018 Alexey Makhalov <amakhalov@vmware.com> 4.14.54-4
-   Fix overflow kernel panic in rsi driver.
-   .config: enable BT stack, enable GPIO sysfs.
-   Add Exar USB serial driver.
*   Fri Aug 17 2018 Ajay Kaher <akaher@vmware.com> 4.14.54-3
-   Enabled USB PCI in config_aarch64
-   Build hang (at make oldconfig) fix in config_aarch64
*   Thu Jul 19 2018 Alexey Makhalov <amakhalov@vmware.com> 4.14.54-2
-   .config: usb_serial_pl2303=m,wlan=y,can=m,gpio=y,pinctrl=y,iio=m
*   Mon Jul 09 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.14.54-1
-   Update to version 4.14.54
*   Fri Jan 26 2018 Alexey Makhalov <amakhalov@vmware.com> 4.14.8-2
-   Added vchiq entry to rpi3 dts
-   Added dtb-rpi3 subpackage
*   Fri Dec 22 2017 Alexey Makhalov <amakhalov@vmware.com> 4.14.8-1
-   Version update
*   Wed Dec 13 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.66-4
-   KAT build support
*   Thu Dec 07 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.66-3
-   Aarch64 support
*   Tue Dec 05 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.66-2
-   Sign and compress modules after stripping. fips=1 requires signed modules
*   Mon Dec 04 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.66-1
-   Version update
*   Tue Nov 21 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.64-1
-   Version update
*   Mon Nov 06 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.60-1
-   Version update
*   Wed Oct 11 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.53-3
-   Add patch "KVM: Don't accept obviously wrong gsi values via
    KVM_IRQFD" to fix CVE-2017-1000252.
*   Tue Oct 10 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.53-2
-   Build hang (at make oldconfig) fix.
*   Thu Oct 05 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.53-1
-   Version update
*   Mon Oct 02 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.52-3
-   Allow privileged CLONE_NEWUSER from nested user namespaces.
*   Mon Oct 02 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.52-2
-   Fix CVE-2017-11472 (ACPICA: Namespace: fix operand cache leak)
*   Mon Oct 02 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.52-1
-   Version update
*   Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.47-2
-   Requires coreutils or toybox
*   Mon Sep 04 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.47-1
-   Fix CVE-2017-11600
*   Tue Aug 22 2017 Anish Swaminathan <anishs@vmware.com> 4.9.43-2
-   Add missing xen block drivers
*   Mon Aug 14 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.43-1
-   Version update
-   [feature] new sysctl option unprivileged_userns_clone
*   Wed Aug 09 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.41-2
-   Fix CVE-2017-7542
-   [bugfix] Added ccm,gcm,ghash,lzo crypto modules to avoid
    panic on modprobe tcrypt
*   Mon Aug 07 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.41-1
-   Version update
*   Fri Aug 04 2017 Bo Gan <ganb@vmware.com> 4.9.38-6
-   Fix initramfs triggers
*   Tue Aug 01 2017 Anish Swaminathan <anishs@vmware.com> 4.9.38-5
-   Allow some algorithms in FIPS mode
-   Reverts 284a0f6e87b0721e1be8bca419893902d9cf577a and backports
-   bcf741cb779283081db47853264cc94854e7ad83 in the kernel tree
-   Enable additional NF features
*   Fri Jul 21 2017 Anish Swaminathan <anishs@vmware.com> 4.9.38-4
-   Add patches in Hyperv codebase
*   Fri Jul 21 2017 Anish Swaminathan <anishs@vmware.com> 4.9.38-3
-   Add missing hyperv drivers
*   Thu Jul 20 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.38-2
-   Disable scheduler beef up patch
*   Tue Jul 18 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.38-1
-   Fix CVE-2017-11176 and CVE-2017-10911
*   Mon Jul 03 2017 Xiaolin Li <xiaolinl@vmware.com> 4.9.34-3
-   Add libdnet-devel, kmod-devel and libmspack-devel to BuildRequires
*   Thu Jun 29 2017 Divya Thaluru <dthaluru@vmware.com> 4.9.34-2
-   Added obsolete for deprecated linux-dev package
*   Wed Jun 28 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.34-1
-   [feature] 9P FS security support
-   [feature] DM Delay target support
-   Fix CVE-2017-1000364 ("stack clash") and CVE-2017-9605
*   Thu Jun 8 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.31-1
-   Fix CVE-2017-8890, CVE-2017-9074, CVE-2017-9075, CVE-2017-9076
    CVE-2017-9077 and CVE-2017-9242
-   [feature] IPV6 netfilter NAT table support
*   Fri May 26 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.30-1
-   Added ENA driver for AMI
-   Fix CVE-2017-7487 and CVE-2017-9059
*   Wed May 17 2017 Vinay Kulkarni <kulkarniv@vmware.com> 4.9.28-2
-   Enable IPVLAN module.
*   Tue May 16 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.28-1
-   Version update
*   Wed May 10 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.27-1
-   Version update
*   Sun May 7 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.26-1
-   Version update
-   Removed version suffix from config file name
*   Thu Apr 27 2017 Bo Gan <ganb@vmware.com> 4.9.24-2
-   Support dynamic initrd generation
*   Tue Apr 25 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.24-1
-   Fix CVE-2017-6874 and CVE-2017-7618.
-   Fix audit-devel BuildRequires.
-   .config: build nvme and nvme-core in kernel.
*   Mon Mar 6 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.13-2
-   .config: NSX requirements for crypto and netfilter
*   Tue Feb 28 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.13-1
-   Update to linux-4.9.13 to fix CVE-2017-5986 and CVE-2017-6074
*   Thu Feb 09 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.9-1
-   Update to linux-4.9.9 to fix CVE-2016-10153, CVE-2017-5546,
    CVE-2017-5547, CVE-2017-5548 and CVE-2017-5576.
-   .config: added CRYPTO_FIPS support.
*   Tue Jan 10 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.2-1
-   Update to linux-4.9.2 to fix CVE-2016-10088
-   Move linux-tools.spec to linux.spec as -tools subpackage
*   Mon Dec 19 2016 Xiaolin Li <xiaolinl@vmware.com> 4.9.0-2
-   BuildRequires Linux-PAM-devel
*   Mon Dec 12 2016 Alexey Makhalov <amakhalov@vmware.com> 4.9.0-1
-   Update to linux-4.9.0
-   Add paravirt stolen time accounting feature (from linux-esx),
    but disable it by default (no-vmw-sta cmdline parameter)
*   Thu Dec  8 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.35-3
-   net-packet-fix-race-condition-in-packet_set_ring.patch
    to fix CVE-2016-8655
*   Wed Nov 30 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.35-2
-   Expand `uname -r` with release number
-   Check for build-id matching
-   Added syscalls tracing support
-   Compress modules
*   Mon Nov 28 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.35-1
-   Update to linux-4.4.35
-   vfio-pci-fix-integer-overflows-bitmask-check.patch
    to fix CVE-2016-9083
*   Tue Nov 22 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.31-4
-   net-9p-vsock.patch
*   Thu Nov 17 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.31-3
-   tty-prevent-ldisc-drivers-from-re-using-stale-tty-fields.patch
    to fix CVE-2015-8964
*   Tue Nov 15 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.31-2
-   .config: add cgrup_hugetlb support
-   .config: add netfilter_xt_{set,target_ct} support
-   .config: add netfilter_xt_match_{cgroup,ipvs} support
*   Thu Nov 10 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.31-1
-   Update to linux-4.4.31
*   Fri Oct 21 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.26-1
-   Update to linux-4.4.26
*   Wed Oct 19 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-6
-   net-add-recursion-limit-to-GRO.patch
-   scsi-arcmsr-buffer-overflow-in-arcmsr_iop_message_xfer.patch
*   Tue Oct 18 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-5
-   ipip-properly-mark-ipip-GRO-packets-as-encapsulated.patch
-   tunnels-dont-apply-GRO-to-multiple-layers-of-encapsulation.patch
*   Mon Oct  3 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-4
-   Package vmlinux with PROGBITS sections in -debuginfo subpackage
*   Tue Sep 27 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-3
-   .config: CONFIG_IP_SET_HASH_{IPMARK,MAC}=m
*   Tue Sep 20 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-2
-   Add -release number for /boot/* files
-   Use initrd.img with version and release number
-   Rename -dev subpackage to -devel
*   Wed Sep  7 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-1
-   Update to linux-4.4.20
-   apparmor-fix-oops-validate-buffer-size-in-apparmor_setprocattr.patch
-   keys-fix-asn.1-indefinite-length-object-parsing.patch
*   Thu Aug 25 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-11
-   vmxnet3 patches to bumpup a version to 1.4.8.0
*   Wed Aug 10 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-10
-   Added VSOCK-Detach-QP-check-should-filter-out-non-matching-QPs.patch
-   .config: pmem hotplug + ACPI NFIT support
-   .config: enable EXPERT mode, disable UID16 syscalls
*   Thu Jul 07 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-9
-   .config: pmem + fs_dax support
*   Fri Jun 17 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-8
-   patch: e1000e-prevent-div-by-zero-if-TIMINCA-is-zero.patch
-   .config: disable rt group scheduling - not supported by systemd
*   Wed Jun 15 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.4.8-7
-   fixed the capitalization for - System.map
*   Thu May 26 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-6
-   patch: REVERT-sched-fair-Beef-up-wake_wide.patch
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.4.8-5
-   GA - Bump release of all rpms
*   Mon May 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.4.8-4
-   Fixed generation of debug symbols for kernel modules & vmlinux.
*   Mon May 23 2016 Divya Thaluru <dthaluru@vmware.com> 4.4.8-3
-   Added patches to fix CVE-2016-3134, CVE-2016-3135
*   Wed May 18 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.4.8-2
-   Enabled CONFIG_UPROBES in config as needed by ktap
*   Wed May 04 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-1
-   Update to linux-4.4.8
-   Added net-Drivers-Vmxnet3-set-... patch
*   Tue May 03 2016 Vinay Kulkarni <kulkarniv@vmware.com> 4.2.0-27
-   Compile Intel GigE and VMXNET3 as part of kernel.
*   Thu Apr 28 2016 Nick Shi <nshi@vmware.com> 4.2.0-26
-   Compile cramfs.ko to allow mounting cramfs image
*   Tue Apr 12 2016 Vinay Kulkarni <kulkarniv@vmware.com> 4.2.0-25
-   Revert network interface renaming disable in kernel.
*   Tue Mar 29 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-24
-   Support kmsg dumping to vmware.log on panic
-   sunrpc: xs_bind uses ip_local_reserved_ports
*   Mon Mar 28 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-23
-   Enabled Regular stack protection in Linux kernel in config
*   Thu Mar 17 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-22
-   Restrict the permissions of the /boot/System.map-X file
*   Fri Mar 04 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-21
-   Patch: SUNRPC: Do not reuse srcport for TIME_WAIT socket.
*   Wed Mar 02 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-20
-   Patch: SUNRPC: Ensure that we wait for connections to complete
    before retrying
*   Fri Feb 26 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-19
-   Disable watchdog under VMware hypervisor.
*   Thu Feb 25 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-18
-   Added rpcsec_gss_krb5 and nfs_fscache
*   Mon Feb 22 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-17
-   Added sysctl param to control weighted_cpuload() behavior
*   Thu Feb 18 2016 Divya Thaluru <dthaluru@vmware.com> 4.2.0-16
-   Disabling network renaming
*   Sun Feb 14 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-15
-   veth patch: don’t modify ip_summed
*   Thu Feb 11 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-14
-   Full tickless -> idle tickless + simple CPU time accounting
-   SLUB -> SLAB
-   Disable NUMA balancing
-   Disable stack protector
-   No build_forced no-CBs CPUs
-   Disable Expert configuration mode
-   Disable most of debug features from 'Kernel hacking'
*   Mon Feb 08 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-13
-   Double tcp_mem limits, patch is added.
*   Wed Feb 03 2016 Anish Swaminathan <anishs@vmware.com>  4.2.0-12
-   Fixes for CVE-2015-7990/6937 and CVE-2015-8660.
*   Tue Jan 26 2016 Anish Swaminathan <anishs@vmware.com> 4.2.0-11
-   Revert CONFIG_HZ=250
*   Fri Jan 22 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-10
-   Fix for CVE-2016-0728
*   Wed Jan 13 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-9
-   CONFIG_HZ=250
*   Tue Jan 12 2016 Mahmoud Bassiouny <mbassiouny@vmware.com> 4.2.0-8
-   Remove rootfstype from the kernel parameter.
*   Mon Jan 04 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-7
-   Disabled all the tracing options in kernel config.
-   Disabled preempt.
-   Disabled sched autogroup.
*   Thu Dec 17 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-6
-   Enabled kprobe for systemtap & disabled dynamic function tracing in config
*   Fri Dec 11 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-5
-   Added oprofile kernel driver sub-package.
*   Fri Nov 13 2015 Mahmoud Bassiouny <mbassiouny@vmware.com> 4.2.0-4
-   Change the linux image directory.
*   Wed Nov 11 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-3
-   Added the build essential files in the dev sub-package.
*   Mon Nov 09 2015 Vinay Kulkarni <kulkarniv@vmware.com> 4.2.0-2
-   Enable Geneve module support for generic kernel.
*   Fri Oct 23 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-1
-   Upgraded the generic linux kernel to version 4.2.0 & and updated timer handling to full tickless mode.
*   Tue Sep 22 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.0.9-5
-   Added driver support for frame buffer devices and ACPI
*   Wed Sep 2 2015 Alexey Makhalov <amakhalov@vmware.com> 4.0.9-4
-   Added mouse ps/2 module.
*   Fri Aug 14 2015 Alexey Makhalov <amakhalov@vmware.com> 4.0.9-3
-   Use photon.cfg as a symlink.
*   Thu Aug 13 2015 Alexey Makhalov <amakhalov@vmware.com> 4.0.9-2
-   Added environment file(photon.cfg) for grub.
*   Wed Aug 12 2015 Sharath George <sharathg@vmware.com> 4.0.9-1
-   Upgrading kernel version.
*   Wed Aug 12 2015 Alexey Makhalov <amakhalov@vmware.com> 3.19.2-5
-   Updated OVT to version 10.0.0.
-   Rename -gpu-drivers to -drivers-gpu in accordance to directory structure.
-   Added -sound package/
*   Tue Aug 11 2015 Anish Swaminathan<anishs@vmware.com> 3.19.2-4
-   Removed Requires dependencies.
*   Fri Jul 24 2015 Harish Udaiya Kumar <hudaiyakumar@gmail.com> 3.19.2-3
-   Updated the config file to include graphics drivers.
*   Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 3.13.3-2
-   Update according to UsrMove.
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 3.13.3-1
-   Initial build. First version

