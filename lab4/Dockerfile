FROM alpine:latest as build

ARG NGINX_VERSION=1.22.1
ARG PKG_RELEASE=1

RUN set -x && \
    NGINX_PACKAGE_NAME="nginx=${NGINX_VERSION}-r${PKG_RELEASE}" && \
    #addgroup -g 101 -S nginx && \
    #adduser -S -D -H -u 101 -h /var/cache/nginx -s /sbin/nologin -G nginx -g nginx nginx && \
    # install packages for keys check
    apk add --no-cache --virtual .checksum-deps \
        openssl && \
    # get keys
    KEY_SHA512="e09fa32f0a0eab2b879ccbbc4d0e4fb9751486eedda75e35fac65802cc9faa266425edf83e261137a2f4d16281ce2c1a5f4502930fe75154723da014214f0655" && \
    wget -O /tmp/nginx_signing.rsa.pub https://nginx.org/keys/nginx_signing.rsa.pub && \
    #check control sum
    if echo "$KEY_SHA512 */tmp/nginx_signing.rsa.pub" | sha512sum -c -; then \
        echo "key verification succeeded"; \
        mv /tmp/nginx_signing.rsa.pub /etc/apk/keys/; \
    else \
        echo "key verification failed"; \
        exit 1; \
    fi && \
    apk add -X "https://nginx.org/packages/alpine/v$(egrep -o '^[0-9]+\.[0-9]+' /etc/alpine-release)/main" --no-cache $NGINX_PACKAGE_NAME && \
    # remove all redundant deps
    apk del .checksum-deps && \
    if [ -n "/etc/apk/keys/nginx_signing.rsa.pub" ]; then \ 
        rm -f /etc/apk/keys/nginx_signing.rsa.pub; \
    fi && \
    # forward errors/logs for Docker
    ln -sf /dev/stdout /var/log/nginx/access.log && \
    ln -sf /dev/stderr /var/log/nginx/error.log 


FROM scratch

COPY --from=build /etc/passwd /etc/group /etc/

COPY --from=build ["/lib/ld-musl-x86_64.so.1", \
    "/lib/libssl.so.3", \
    "/lib/libcrypto.so.3", \
    "/lib/libz.so.1", \
    "/lib/ld-musl-x86_64.so.1", \
    "/lib/"]
COPY --from=build /usr/lib/libpcre2-8.so.0 /usr/lib/

COPY --from=build /usr/sbin/nginx /usr/sbin/nginx
COPY --from=build /var/log/nginx /var/log/nginx
COPY --from=build /etc/nginx /etc/nginx

# COPY static/ /usr/share/nginx/html/
# COPY nginx.conf /etc/nginx/

STOPSIGNAL SIGQUIT

EXPOSE 80

CMD ["/usr/sbin/nginx", "-g", "daemon off;"]