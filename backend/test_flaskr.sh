#!/bin/bash

# Test Flaskr Application
# This script sets up the test database and runs the tests

echo "Setting up test database..."

# Drop the test database if it exists
dropdb trivia_test 2>/dev/null || echo "Database trivia_test does not exist, skipping drop"

# Create a new test database
echo "Creating test database..."
createdb trivia_test

# Load the SQL data into the test database
echo "Loading SQL data into test database..."
psql trivia_test < trivia.psql

# Run the tests
echo "Running tests..."
python test_flaskr.py

echo "Test execution completed!" 