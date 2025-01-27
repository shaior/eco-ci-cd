FROM registry.access.redhat.com/ubi9/ubi

# Install required packages
RUN dnf -y install \
    python3 \
    python3-pip \
    && dnf clean all

# Upgrade pip3
RUN pip3 install --upgrade pip

# Install ansible and ansible-lint
RUN pip3 install --no-cache-dir \
    setuptools_rust \
    ansible \
    ansible-lint

# Copy application files to eco-ci-cd folder
COPY . ./eco-ci-cd

WORKDIR /eco-ci-cd

# Install requirements
RUN ansible-galaxy collection install -r requirements.yml

# Set entrypoint to bash
ENTRYPOINT ["/bin/bash"]
