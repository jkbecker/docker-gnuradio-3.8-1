# gnuradio-3.8

Docker build of gnuradio-3.8, from source, on Ubuntu 18.04.

Build locally using the build instructions, if you want.

Or, this image is also pushed to [Theseus Cores Docker Hub](https://hub.docker.com/r/theseuscores/gnuradio),
so you can jump straight to the "running" section without doing a local build.


## Build instructions

`docker build --tag theseuscores/gnuradio .`

There's also a number of override-able parameters in the Dockerfile that
can be used to specify Gnuradio and UHD configuration.

## Running

Run the docker image, with volume mounts for running gnuradio-companion
and a data directory:

```
docker run -it -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v </local/path/to/data>:/home/developer/data --name <container-name> theseuscores/gnuradio:v3.8.0.0-rc1
```

To start and reattach to a stopped container:
```bash
docker start <container-name>
docker attach <container-name>
```
