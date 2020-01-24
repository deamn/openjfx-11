%global openjfxdir %{_jvmdir}/%{name}

Name:           openjfx-11
Version:        11.0.3.1
Release:        0%{?dist}
Summary:        Rich client application platform for Java

#fxpackager is BSD -> TODO fxpackager is always included?
License:        GPL v2 with exceptions and BSD
URL:            http://openjdk.java.net/projects/openjfx/

Source0:        hg.openjdk.java.net/openjfx/11/rt/archive/rt-11.0.3+1.tar.bz2

#Patch0:         0000-Change-SWT-and-Lucene.patch
#Patch0:         0000-Fix-wait-call-in-PosixPlatform.patch
#Patch1:         0001-Change-SWT-and-Lucene.patch
#Patch2:         0002-Allow-build-to-work-on-newer-gradles.patch
#Patch3:         0003-fix-cast-between-incompatible-function-types.patch
#Patch4:         0004-Fix-Compilation-Flags.patch
#Patch5:         0005-fxpackager-extract-jre-accept-symlink.patch
#Patch6:         0006-Drop-SWT-32bits-and-Lucene.patch

ExclusiveArch:  x86_64

Requires:       java-11-openjdk

BuildRequires:  java-11-openjdk-devel
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libstdc++-static
BuildRequires:  mvn(antlr:antlr)
BuildRequires:  mvn(org.antlr:antlr:3.1.3)
BuildRequires:  mvn(org.antlr:stringtemplate)
BuildRequires:  mvn(org.apache.ant:ant)
BuildRequires:  mvn(org.eclipse.swt:swt)

BuildRequires:  pkgconfig(gtk+-2.0)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(gthread-2.0)
BuildRequires:  pkgconfig(xtst)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(xxf86vm)
BuildRequires:  pkgconfig(gl)

BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  gperf

%description
JavaFX/OpenJFX is a set of graphics and media APIs that enables Java
developers to design, create, test, debug, and deploy rich client
applications that operate consistently across diverse platforms.

The media and web module have been removed due to missing dependencies.

%package devel
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: java-devel
Summary: OpenJFX development tools and libraries

%description devel
%{summary}.

%package src
Requires: %{name}%{?_isa} = %{version}-%{release}
Summary: OpenJFX Source Bundle

%description src
%{summary}.

%package javadoc
Summary: Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n rt-11.0.3+1
#%patch0 -p1
#%ifarch s390 %{arm} %{ix86}
#%patch -P 6 -p1
#%else
#%patch1 -p1
#%endif
#%patch2 -p1
#%patch3 -p1
#%patch4 -p1
#%patch5 -p1

#Drop *src/test folders
rm -rf modules/javafx.{base,controls,fxml,graphics,media,swing,swt,web}/src/test/
rm -rf modules/jdk.packager/src/test/

#prep for javafx.graphics
cp -a modules/javafx.graphics/src/jslc/antlr modules/javafx.graphics/src/main/antlr3
cp -a modules/javafx.graphics/src/main/resources/com/sun/javafx/tk/quantum/*.properties modules/javafx.graphics/src/main/java/com/sun/javafx/tk/quantum

find -name '*.class' -delete
find -name '*.jar' -delete

#Bundled libraries
#rm -rf modules/javafx-media/src/main/native/gstreamer/3rd_party/glib
#rm -rf modules/javafx-media/src/main/native/gstreamer/gstreamer-lite

#set VersionInfo
cp -a ../build.xml .
ant -f build.xml

#TODO mettre à jour version dans les pom.xml

#copy maven files
cp -a ../pom-openjfx.xml ./pom.xml
for MODULE in base controls fxml graphics media swing swt web
do
	cp -a ../pom-$MODULE.xml  ./modules/javafx.$MODULE/pom.xml
done

mkdir ./modules/javafx.graphics/mvn-{antlr,decora,fulljava,graphics,libdecora,libglass,libglassgtk2,libglassgtk3,libjavafx_font,libjavafx_font_freetype,libjavafx_font_pango,libjavafx_iio,libprism_common,libprism_es2,libprism_sw,prism}
for GRAPHMOD in antlr decora fulljava graphics libdecora libglass libglassgtk2 libglassgtk3 libjavafx_font libjavafx_font_freetype libjavafx_font_pango libjavafx_iio libprism_common libprism_es2 libprism_sw prism
do
	cp -a ../pom-graphics_$GRAPHMOD.xml  ./modules/javafx.graphics/mvn-$GRAPHMOD/pom.xml
done

mkdir ./modules/javafx.graphics/mvn-fulljava/mvn-{decora,java,prism}
for SUBMOD in decora java prism
do
	cp -a ../pom-graphics_fulljava-$SUBMOD.xml  ./modules/javafx.graphics/mvn-fulljava/mvn-$SUBMOD/pom.xml
done

%build
#set openjdk11 for build
export JAVA_HOME=%{_jvmdir}/java-11-openjdk

mvn clean package

%install
install -d -m 755 %{buildroot}%{openjfxdir}
cp -a build/sdk/{bin,lib,rt} %{buildroot}%{openjfxdir}

install -d -m 755 %{buildroot}%{_mandir}/man1
install -m 644 build/sdk/man/man1/* %{buildroot}%{_mandir}/man1

install -d -m 755 %{buildroot}%{_mandir}/ja_JP/man1
install -m 644 build/sdk/man/ja_JP.UTF-8/man1/* %{buildroot}%{_mandir}/ja_JP/man1

install -m 644 build/sdk/javafx-src.zip %{buildroot}%{openjfxdir}/javafx-src.zip

install -d 755 %{buildroot}%{_javadocdir}/%{name}
cp -a build/sdk/docs/api/. %{buildroot}%{_javadocdir}/%{name}

mkdir -p %{buildroot}%{_bindir}
ln -s %{openjfxdir}/bin/javafxpackager %{buildroot}%{_bindir}
ln -s %{openjfxdir}/bin/javapackager %{buildroot}%{_bindir}

%files
%dir %{openjfxdir}
%{openjfxdir}/rt
%license LICENSE
%doc README

%files devel
%{openjfxdir}/lib
%{openjfxdir}/bin
%{_bindir}/javafxpackager
%{_bindir}/javapackager
%{_mandir}/man1/javafxpackager.1*
%{_mandir}/man1/javapackager.1*
%{_mandir}/ja_JP/man1/javafxpackager.1*
%{_mandir}/ja_JP/man1/javapackager.1*
%license LICENSE
%doc README

%files src
%{openjfxdir}/javafx-src.zip

%files javadoc
%{_javadocdir}/%{name}
%license LICENSE

%changelog
* Wed Aug 14 2019 Nicolas De Amicis - 11.0.3.1-0
- Initial packaging
