FROM registry.access.redhat.com/ubi9/ubi

# rpms required for building and running test suites
RUN dnf -y install \
    jq \
    git \
    make \
    gettext \
    which \
    skopeo \
    findutils \
    gcc \
    python3 \
    ansible \
    diffutils \
    && dnf clean all

ENTRYPOINT [ "/bin/bash" ]
