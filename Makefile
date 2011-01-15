CURDIR=$(PWD)

git:
	git submodule foreach git pull origin master

doc:
	cd pyramid_formalchemy/docs; $(MAKE) html
	cd formalchemy/docs; $(MAKE) html
	cd fa.jquery/docs; $(MAKE) html
	cd docs; $(MAKE) html

clean:
	rm -Rf pyramid_formalchemy/docs/_build
	rm -Rf formalchemy/docs/_build
	rm -Rf fa.jquery/docs/_build
	rm -Rf docs/_build
