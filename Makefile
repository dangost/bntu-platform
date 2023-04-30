all: docker

docker: build_for_alpine alpine docker-image

docker-image:
	docker build -t bntu-platform .

build_for_alpine:
	docker build -t alpine-builder -f Dockerfile-builder .

alpine: build_for_alpine
	docker run --name alpine_builder_container -v $(PWD)/alpine:/app/dist alpine-builder
	docker stop alpine_builder_container
	docker rm alpine_builder_container
	docker rmi alpine-builder


build_platform: pipeline build_service copy_views

pipeline:
	poe precommit;

build_service:
	pyinstaller --onefile runner.py;
	mv dist/runner dist/platform;
	chmod +x dist/platform;

copy_views:
	cp -r views dist/views

clean:
	docker rmi bntu-platform

