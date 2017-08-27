Name:		nano
Version:	2.8.7
Release:	1
Summary:	Tiny console text editor that aims to emulate Pico
License:	GPLv3
Group:		Editors
URL:		http://www.nano-editor.org/
Source0:	http://www.nano-editor.org/dist/v2.8/%{name}-%{version}.tar.gz
BuildRequires:	ncurses-devel
BuildRequires:	ncursesw-devel
BuildRequires:	texinfo
BuildRequires:	groff

%description
nano (Nano's ANOther editor) is the editor formerly known as
TIP (TIP Isn't Pico). It aims to emulate Pico as closely as
possible while also offering a few enhancements.

%prep
%setup -q
%apply_patches

%build
# do not run autotools, we have already reflected the configure.ac
# changes in configure and config.h.in
touch -c aclocal.m4 config.h.in configure Makefile.in

%configure
%make

%install
%makeinstall_std

#config file
install -Dpm644 doc/sample.nanorc %{buildroot}%{_sysconfdir}/nanorc

#disable line wrapping by default
sed -i -e 's/# set nowrap/set nowrap/' %{buildroot}%{_sysconfdir}/nanorc

#enable some syntax highlighting by default
for i in nanorc c makefile patch perl python ruby sh; do
	sed -i -e "/\/$i\.nanorc/ s/^#\s//" %{buildroot}%{_sysconfdir}/nanorc
done

#add and enable .spec syntax highlighting
cat >> %{buildroot}%{_sysconfdir}/nanorc << EOF

## RPM .spec files
include "%{_datadir}/nano/spec.nanorc"
EOF

%find_lang %{name} --with-man --all-name

%files -f %{name}.lang
%doc AUTHORS  ChangeLog NEWS README THANKS TODO
%doc doc/faq.html doc/sample.nanorc
%{_bindir}/nano
%{_bindir}/rnano
%{_datadir}/nano
%{_infodir}/nano.info*
%{_mandir}/man1/nano.1*
%{_mandir}/man1/rnano.1*
%{_mandir}/man5/nanorc.5*
%config(noreplace) %{_sysconfdir}/nanorc
