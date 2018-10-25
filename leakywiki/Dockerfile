FROM gcc as builder
RUN apt-get update && \
    apt-get install -y \
        cmake \
        libuv1-dev \
        binutils
WORKDIR /usr/src/app
COPY . .
RUN mkdir build && \
    cd build && \
    cmake .. && \
    make pwn && \
    strip -s -o server pwn

FROM debian
RUN apt-get update && \
    apt-get install -y \
        libuv1 \
        openssl
WORKDIR /app
COPY static static
COPY --from=builder /usr/src/app/build/server .
CMD ./server
