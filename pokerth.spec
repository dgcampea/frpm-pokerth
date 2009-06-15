Name:		pokerth
Version:	0.7
Release:	3%{?dist}
Summary:	A Texas-Holdem poker game
Group:		Amusements/Games
License:	GPLv2+
URL:		http://www.pokerth.net
Source0:	http://downloads.sourceforge.net/%{name}/PokerTH-%{version}-src.tar.bz2
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	desktop-file-utils
BuildRequires:	qt4-devel
BuildRequires:	zlib-devel
BuildRequires:	libcurl-devel
BuildRequires:	gnutls-devel
BuildRequires:	boost-devel >= 1.37
BuildRequires:	SDL_mixer-devel

# Removed bundled fonts
Requires:	bitstream-vera-sans-fonts
Requires:	urw-fonts

%description
PokerTH is a poker game written in C++/QT4. You can play the popular
"Texas Hold'em" poker variant against up to six computer-opponents or
play network games with people all over the world. This poker engine
is available for Linux, Windows, and MacOSX.

%prep
%setup -q -n PokerTH-%{version}-src
# Fix permissions
chmod 644 ChangeLog
find . -name *.h -exec chmod 644 {} \;
find . -name *.cpp -exec chmod 644 {} \;

# Remove option that breaks build from qmake files
for file in *.pro; do
 sed -i "s|-no_dead_strip_inits_and_terms||g" $file
done

%build
%{_qt4_qmake} pokerth.pro
make %{?_smp_mflags}


%install
rm -rf %{buildroot} 
make install INSTALL_ROOT=%{buildroot} COPY="cp -p -f"
# Ugh, binary isn't automatically installed
install -D -p -m 755 %{name} %{buildroot}%{_bindir}/%{name}
install -D -p -m 755 bin/%{name}_server %{buildroot}%{_bindir}/%{name}_server

# Remove bundled fonts
rm %{buildroot}%{_datadir}/%{name}/data/fonts/{VeraBd.ttf,c059013l.pfb,n019003l.pfb}
# and replace them with symlinks
ln -s %{_datadir}/fonts/default/Type1/c059013l.pfb %{buildroot}%{_datadir}/%{name}/data/fonts/
ln -s %{_datadir}/fonts/default/Type1/n019003l.pfb %{buildroot}%{_datadir}/%{name}/data/fonts/
ln -s %{_datadir}/fonts/bitstream-vera/VeraBd.ttf %{buildroot}%{_datadir}/%{name}/data/fonts/

# Install desktop file
desktop-file-install --remove-category="Qt" --dir=%{buildroot}%{_datadir}/applications %{name}.desktop 

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING ChangeLog TODO
%{_bindir}/%{name}
%{_bindir}/%{name}_server
%{_datadir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png


%changelog
* Sun Jun 14 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0.7-3
- Removed BR: asio-devel.
- Changed BR on boost to >= 1.37.

* Sat Jun 13 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0.7-2
- Fix spelling error in font symlink, conserve time stamps.

* Wed May 27 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0.7-1
- First release.