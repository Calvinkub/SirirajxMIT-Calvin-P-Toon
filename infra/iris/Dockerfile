ARG IRIS_IMAGE=intersystems/irishealth-community:latest-cd
FROM ${IRIS_IMAGE}
USER root
RUN mkdir -p /durable && chown irisowner:irisowner /durable
USER irisowner
RUN iris start IRIS && \
    echo 'do ##class(Security.Users).UnExpireUserPasswords("*")' | iris session IRIS -U %SYS && \
    iris stop IRIS quietly
