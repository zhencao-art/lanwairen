project_dir = $(shell pwd)
.PHONY:
rpm:
	mkdir -p rpmtop/BUILD
	mkdir -p rpmtop/BUILDROOT
	mkdir -p rpmtop/RPMS
	mkdir -p rpmtop/SOURCES
	mkdir -p rpmtop/SPECS
	mkdir -p rpmtop/SRPMS
	tar -zcvf freebird.tar.gz freebird.py freebird.conf freebird.service freebird.timer
	mv freebird.tar.gz rpmtop/SOURCES
	rpmbuild -bb --define='_topdir $(project_dir)/rpmtop' freebird.spec


install:
	cp freebird.py /usr/bin
	cp freebird.service freebird.timer /lib/systemd/system
	cp freebird.conf /etc

uninstall:
	rm -f /usr/bin/freebird
	rm -f /lib/systemd/system/freebird.service
	rm -f /lib/systemd/system/freebird.timer
	rm -f /etc/freebird.conf

clean:
	rm -f freebird.tar.gz
	rm -rf rpmtop
