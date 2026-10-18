FROM mcr.microsoft.com/devcontainers/java:21

# Bake Pakku into the image
RUN curl -fsSL -o /usr/local/bin/pakku.jar https://github.com/juraj-hrivnak/Pakku/releases/download/v1.5.0/pakku.jar \
    && printf '#!/bin/sh\nexec java -jar /usr/local/bin/pakku.jar "$@"\n' > /usr/local/bin/pakku \
    && chmod +x /usr/local/bin/pakku /usr/local/bin/pakku.jar
