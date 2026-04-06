run:
	docker compose up --build 


run-bg:
	docker compose up --build -d


test:
	docker build -t myimage:test -f Dockerfile_test .
	docker run -it --rm myimage:test

bench:
	docker build -t myimage:bench -f Dockerfile_bench .
	docker run -it --rm myimage:bench