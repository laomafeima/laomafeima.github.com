run:
	make clean
	python3 blog.py
clean:
	rm -rf blog/*
	rm -rf annual/*
	rm -rf tag/*
	rm tags.html
	rm notes.html
	rm index.html
