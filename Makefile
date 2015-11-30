# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved.  This file is offered as-is,
# without any warranty.

PREFIX = /usr
BIN = /bin
DATA = /share
BINDIR = $(PREFIX)$(BIN)
DATADIR = $(PREFIX)$(DATA)
DOCDIR = $(DATADIR)/doc
INFODIR = $(DATADIR)/info
MANDIR = $(DATADIR)/man
MAN1DIR = $(MANDIR)/man1
LICENSEDIR = $(DATADIR)/licenses


PKGNAME = wikiquote-fortune
COMMAND = wikiquote-fortune



.PHONY: default
default: base man

.PHONY: all
all: base doc

.PHONY: base
base:

.PHONY: doc
doc: man info pdf dvi ps

.PHONY: man
man:

.PHONY: info
info: bin/wikiquote-fortune.info
bin/%.info: doc/info/%.texinfo doc/info/fdl.texinfo
	@mkdir -p bin
	makeinfo $<
	mv $*.info $@

.PHONY: pdf
pdf: bin/wikiquote-fortune.pdf
bin/%.pdf: doc/info/%.texinfo doc/info/fdl.texinfo
	@mkdir -p obj/pdf bin
	cd obj/pdf ; yes X | texi2pdf ../../$<
	mv obj/pdf/$*.pdf $@

.PHONY: dvi
dvi: bin/wikiquote-fortune.dvi
bin/%.dvi: doc/info/%.texinfo doc/info/fdl.texinfo
	@mkdir -p obj/dvi bin
	cd obj/dvi ; yes X | $(TEXI2DVI) ../../$<
	mv obj/dvi/$*.dvi $@

.PHONY: ps
ps: bin/wikiquote-fortune.ps
bin/%.ps: doc/info/%.texinfo doc/info/fdl.texinfo
	@mkdir -p obj/ps bin
	cd obj/ps ; yes X | texi2pdf --ps ../../$<
	mv obj/ps/$*.ps $@



.PHONY: install
install: install-base install-man install-info

.PHONY: install-all
install-all: install-base install-doc

.PHONY: install-base
install-base: install-command install-copyright

.PHONY: install-command
install-command:
	install -dm755 -- "$(DESTDIR)$(BINDIR)"
	install -m755 src/wikiquote-fortune -- "$(DESTDIR)$(BINDIR)/$(COMMAND)"

.PHONY: install-copyright
install-copyright: install-copying install-license

.PHONY: install-copying
install-copying:
	install -dm755 -- "$(DESTDIR)$(LICENSEDIR)/$(PKGNAME)"
	install -m644 COPYING -- "$(DESTDIR)$(LICENSEDIR)/$(PKGNAME)/COPYING"

.PHONY: install-license
install-license:
	install -dm755 -- "$(DESTDIR)$(LICENSEDIR)/$(PKGNAME)"
	install -m644 LICENSE -- "$(DESTDIR)$(LICENSEDIR)/$(PKGNAME)/LICENSE"

.PHONY: install-doc
install-doc: install-man install-info install-pdf install-ps install-dvi

.PHONY: install-man
install-man:
	install -dm755 -- "$(DESTDIR)$(MAN1DIR)"
	install -m644 doc/man/wikiquote-fortune.1 -- "$(DESTDIR)$(MAN1DIR)/$(COMMAND).1"

.PHONY: install-info
install-info: bin/wikiquote-fortune.info
	install -dm755 -- "$(DESTDIR)$(INFODIR)"
	install -m644 $< -- "$(DESTDIR)$(INFODIR)/$(PKGNAME).info"

.PHONY: install-pdf
install-pdf: bin/wikiquote-fortune.pdf
	install -dm755 -- "$(DESTDIR)$(DOCDIR)"
	install -m644 $< -- "$(DESTDIR)$(DOCDIR)/$(PKGNAME).pdf"

.PHONY: install-ps
install-ps: bin/wikiquote-fortune.ps
	install -dm755 -- "$(DESTDIR)$(DOCDIR)"
	install -m644 $< -- "$(DESTDIR)$(DOCDIR)/$(PKGNAME).ps"

.PHONY: install-dvi
install-dvi: bin/wikiquote-fortune.dvi
	install -dm755 -- "$(DESTDIR)$(DOCDIR)"
	install -m644 $< -- "$(DESTDIR)$(DOCDIR)/$(PKGNAME).dvi"



.PHONY: uninstall
uninstall:
	-rm -- "$(DESTDIR)$(BINDIR)/$(COMMAND)"
	-rm -- "$(DESTDIR)$(LICENSEDIR)/$(PKGNAME)/COPYING"
	-rm -- "$(DESTDIR)$(LICENSEDIR)/$(PKGNAME)/LICENSE"
	-rmdir -- "$(DESTDIR)$(LICENSEDIR)/$(PKGNAME)"
	-rm -- "$(DESTDIR)$(MAN1DIR)/$(COMMAND).1"
	-rm -- "$(DESTDIR)$(INFODIR)/$(PKGNAME).info"
	-rm -- "$(DESTDIR)$(DOCDIR)/$(PKGNAME).pdf"
	-rm -- "$(DESTDIR)$(DOCDIR)/$(PKGNAME).ps"
	-rm -- "$(DESTDIR)$(DOCDIR)/$(PKGNAME).dvi"



.PHONY: clean
clean:
	-rm -rf obj bin

