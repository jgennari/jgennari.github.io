---
title: "Creating a Docker Hub Repository"
date: 2024-02-28T11:12:38-05:00
draft: false
---

Recently I was looking to implement some analytics from this site and came across the following blog post by Haseed Majid: [How to Add Page Views to your Hugo Blog Posts Using Goatcounter](https://haseebmajid.dev/posts/2022-11-25-how-to-add-page-views-to-your-hugo-blog-posts-using-goatcounter/). I really like the concept of [Goatcounter](https://github.com/arp242/goatcounter) and wanted to try it in my self-hosted environment, but it appears the creator has strong opinions about Docker, so there's no provided `Dockerfile`. There are a few implementations referenced in the readme, however they were all based on older versions and not kept up. 

Plus, I run Unraid at home, and I'd love to see it in the Community Applications store, so I decided to try and build it myself.

## Fork the Repository

The first thing I needed to do was fork the repository, which is as easy as clicking the "Fork" button in the top right of the repository page. Once I had my own [fork](https://github.com/jgennari/goatcounter), I created a new branch called `docker` and started working on the `Dockerfile`.

Now admittedly, this was was my first `Dockerfile` from scratch, so I'm building off of some of the examples the original repo suggested. But the gist is this container is based on Debian Bookwork Slim, creates a user within the container, copies the built binary from the build container, and sets the entrypoint to the binary. It also exposes port 80 and creates a volume for the database.

```dockerfile
FROM golang:1.21 AS build

WORKDIR /go/src/goatcounter

# we squat the "dynamically created user accounts" space, see:
# https://www.debian.org/doc/debian-policy/ch-opersys.html#uid-and-gid-classes
# this assumes 32bit support (!)
RUN groupadd -K GID_MIN=65536 -K GID_MAX=4294967293 builder && \
        useradd --no-log-init --create-home -K UID_MIN=65536 -K UID_MAX=4294967293 --gid builder builder && \
        chown builder:builder /go/src/goatcounter

COPY --chown=builder:builder . .

USER builder

# if build fails, try this for more verbosity:
#RUN go build -x -v -work ./cmd/goatcounter
RUN go build -ldflags="-X zgo.at/goatcounter/v2.Version=$(git log -n1 --format='%h_%cI')" ./cmd/goatcounter

FROM debian:bookworm-slim AS runtime

RUN groupadd -K GID_MIN=65536 -K GID_MAX=4294967293 user && \
        useradd --no-log-init --create-home -K UID_MIN=65536 -K UID_MAX=4294967293 --gid user user && \
        rm -fr -- /var/lib/apt/lists/* /var/cache/*

COPY --from=build /go/src/goatcounter/goatcounter /usr/local/bin

USER user
WORKDIR /home/user

RUN mkdir /home/user/db

VOLUME ["/home/user/db/"]
EXPOSE 801

ENTRYPOINT ["/usr/local/bin/goatcounter", "serve", "-tls", "http", "-listen", ":80"]
CMD ["help"]
```

From here, a simple `docker build .` command will build the container so I can test it locally.

![Building](../../images/creating-a-docker-hub-repository_1709137836654.gif)

## Push to Docker Hub

Now that we have a local container tested, I want to publish it to Docker Hub so others can use it. First, I need to create a repository on Docker Hub. Once that's done, I can tag the local container and push it to the repository.

```bash
docker tag <image_id> jgennari/goatcounter:latest
docker push jgennari/goatcounter:latest
```

And just like that, our image is pushed to my repository!

![Image 2](../../images/creating-a-docker-hub-repository_1709138142804.png)  

## Slight Problem & CI

So when I tried to run this container on my Unraid server, I ran into an issue. The container wouldn't start due to it being an ARM64 image. That's because the image was build on my M1 ARM-based Mac. Now there are lots of ways to build multi-platform images on the command line, but I also knew long term I didn't want to have to manually build and push the image every time there was an update to the upstream repository.

So Github Actions to the rescue! I created a new workflow in the `.github/workflows` directory called `docker.yml`. This workflow listens for pushes to the `docker` branch, builds the container, and pushes it to Docker Hub.

```yaml
name: Build Docker Container

on:
  workflow_dispatch:
  push:
    branches:
      - 'docker'

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      -
        name: Set up QEMU
        uses: docker/setup-qemu-action@v3
      -
        name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      -
        name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
      -
        name: Build and push
        uses: docker/build-push-action@v5
        with:
          push: true
          platforms: linux/amd64,linux/arm64
          tags: joeygennari/goatcounter:latest
```

The magic sauce is the `platforms` bit on line 30. This tells the build to build for both `linux/amd64` and `linux/arm64`. The `docker/setup-qemu-action` and `docker/setup-buildx-action` are required to build for ARM64 on an x86 machine.

And just like that, one every push to the `docker` branch, the container is built and pushed to Docker Hub!

In the future I'll show you how I automate the management of the upstream repository and keep my fork up to date, as well as submitting the container to the Community Applications store. Stay tuned!