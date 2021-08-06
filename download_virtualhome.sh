#!/usr/bin/env bash

RUN aws s3 cp --recursive s3://geniehai/jackiey/virtualhome/ .
RUN unzip virtualhome_linux_Data.zip
RUN unzip programs_processed_precond_nograb_morepreconds.zip