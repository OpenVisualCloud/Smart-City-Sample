
FROM smtc_common
RUN DEBIAN_FRONTEND=noninteractive apt-get update -qq && apt-get install -qq openssl && rm -rf /var/lib/apt/lists/*

####
ARG  UID
USER ${UID}
####
