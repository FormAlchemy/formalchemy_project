TEST=$(PWD)/bin/nosetests

all: git clean html

develop:
	python2.6 bootstrap.py --distribute
	bin/buildout

git:
	git pull origin master
	git submodule foreach git pull origin master

push:
	git submodule foreach git push origin master
	git push origin master

html:
	cd pyramid_formalchemy/docs; $(MAKE) html
	cd formalchemy/docs; $(MAKE) html
	cd fa.jquery/docs; $(MAKE) html
	cd docs; $(MAKE) html

test:
	cd pyramid_formalchemy; $(TEST)
	cd formalchemy; bin/test
	cd fa.jquery; $(TEST)

clean:
	rm -Rf pyramid_formalchemy/docs/_build
	rm -Rf formalchemy/docs/_build
	rm -Rf fa.jquery/docs/_build
	rm -Rf docs/_build

