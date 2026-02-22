#!/usr/bin/env bash

set -e

echo "Creating hotel..."
make run ARGS="hotels create --id h1 --name 'Hotel A' --location City --total-rooms 3 --available-rooms 3"

echo "Creating customer..."
make run ARGS="customers create --id c1 --name Alice --email alice@example.com"

echo "Creating reservation..."
make run ARGS="reservations create --customer-id c1 --hotel-id h1 --rooms 2"