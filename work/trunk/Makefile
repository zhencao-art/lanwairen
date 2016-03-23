project_dir = $(shell pwd)

.PHONY:all
all:
	make -C src/server

.PHONY:rpm
rpm:
	mkdir -p rpmtop/BUILD
	mkdir -p rpmtop/BUILDROOT
	mkdir -p rpmtop/RPMS
	mkdir -p rpmtop/SOURCES
	mkdir -p rpmtop/SPECS
	mkdir -p rpmtop/SRPMS
	tar -zcf puma.tar.gz conf/ ocf/ src/ systemd/ server pumacli puma-watchdog puma-init.sh Makefile
	mv puma.tar.gz rpmtop/SOURCES/
	rpmbuild -bb --define="_topdir $(project_dir)/rpmtop" puma.spec

clean:
	make clean -C src/server
	rm -f puma.tar.gz
	rm -rf rpmtop
