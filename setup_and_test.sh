#!/bin/bash

# Comprehensive script to set up, test, and verify the News Summary API project.
# It ensures the environment is correct, sets up the application, and runs an
# end-to-end test to validate all features are working.

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Helper Functions ---
print_step() {
    echo ""
    echo "------------------------------------------"
    echo "STEP: $1"
    echo "------------------------------------------"
}

print_success() {
    echo "✅ SUCCESS: $1"
}

print_error() {
    echo "❌ ERROR: $1" >&2
    exit 1
}

# --- 1. Prerequisites Check ---
print_step "Checking Prerequisites"

# Check for Python 3.11
if ! command -v python3.11 &> /dev/null; then
    print_error "Python 3.11 is not found. Please install it or ensure it's in your PATH."
else
    print_success "Python 3.11 found."
fi

# Check for PostgreSQL client
if ! command -v psql &> /dev/null; then
    print_error "PostgreSQL client (psql) not found. Please install PostgreSQL."
else
    print_success "PostgreSQL client found."
fi

# Check for .env file
if [ ! -f .env ]; then
    print_error ".env file not found. Please create it by copying the template from README.md."
else
    print_success ".env file found."
fi

# --- 2. Project Setup ---
print_step "Setting up Python Virtual Environment"
python3.11 -m venv .venv
print_success "Virtual environment created."

print_step "Installing Dependencies"
.venv/bin/pip install -r requirements.txt
print_success "All dependencies installed from requirements.txt."

# --- 3. Database Setup ---
print_step "Running Database Migrations"
.venv/bin/python manage.py migrate
print_success "Database migrations applied."

# --- 4. Run Server in Background ---
print_step "Starting Django Server in Background"
.venv/bin/python manage.py runserver > server.log 2>&1 &
SERVER_PID=$!
echo "Server started with PID: $SERVER_PID. Log file is server.log."

# Wait for the server to be ready
echo "Waiting for server to respond..."
timeout 30s bash -c 'until curl -s http://127.0.0.1:8000/api/latest/ > /dev/null; do echo -n "." && sleep 1; done' || print_error "Server failed to start in 30 seconds."
print_success "Server is up and running."

# --- 5. End-to-End Test ---
print_step "Running End-to-End Test"

# Define a cleanup function to kill the server on exit
cleanup() {
    echo ""
    print_step "Cleaning Up"
    echo "Shutting down server (PID: $SERVER_PID)..."
    kill $SERVER_PID
    print_success "Server shut down."
}
trap cleanup EXIT

# Register a new user
echo "Registering user 'test_script_user'..."
curl -s -X POST -H "Content-Type: application/json" -d '{"username": "test_script_user", "email": "script@test.com", "password": "password123"}' http://127.0.0.1:8000/api/register/ > /dev/null
print_success "User registration request sent."

# Log in to get a token
echo "Logging in to get JWT token..."
TOKEN=$(curl -s -X POST -H "Content-Type: application/json" -d '{"username": "test_script_user", "password": "password123"}' http://127.0.0.1:8000/api/token/ | jq -r '.access')

if [ -z "$TOKEN" ] || [ "$TOKEN" == "null" ]; then
    print_error "Failed to get login token."
fi
print_success "Successfully logged in and obtained token."

# Search for an article
echo "Searching for articles..."
ARTICLE_JSON=$(curl -s -X GET "http://127.0.0.1:8000/api/search/?q=Django" -H "Authorization: Bearer $TOKEN" | jq '.[0]')

if [ -z "$ARTICLE_JSON" ] || [ "$ARTICLE_JSON" == "null" ]; then
    print_error "Failed to fetch articles from search."
fi
print_success "Successfully searched for articles."

# Save the article
echo "Saving an article..."
SAVE_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X POST http://127.0.0.1:8000/api/save/ -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d "$ARTICLE_JSON")
if [ "$SAVE_RESPONSE" != "201" ]; then
    print_error "Failed to save article. Server responded with HTTP $SAVE_RESPONSE."
fi
print_success "Successfully saved the article."

# Verify the saved article
echo "Verifying saved articles..."
SAVED_COUNT=$(curl -s -X GET http://127.0.0.1:8000/api/saved/ -H "Authorization: Bearer $TOKEN" | jq 'length')
if [ "$SAVED_COUNT" -lt 1 ]; then
    print_error "Verification failed. No articles found in saved list."
fi
print_success "Verification complete. Found $SAVED_COUNT article(s) in saved list."

print_step "FULL TEST SUITE PASSED"
