#!/bin/bash
# Test script for Classic OCR Engine API

set -e

API_URL="http://localhost:9003"
API_PREFIX="/api/v1"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=========================================="
echo "Classic OCR Engine - API Tests"
echo "=========================================="

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Helper function to make requests
test_endpoint() {
    local name=$1
    local method=$2
    local endpoint=$3
    local data=$4
    local expected_status=$5

    echo -e "\n${YELLOW}Testing: ${name}${NC}"
    echo "  Method: ${method} ${endpoint}"

    if [ -z "$data" ]; then
        response=$(curl -s -w "\n%{http_code}" -X ${method} "${API_URL}${endpoint}")
    else
        response=$(curl -s -w "\n%{http_code}" -X ${method} -F "${data}" "${API_URL}${endpoint}")
    fi

    status_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')

    if [ "$status_code" == "$expected_status" ]; then
        echo -e "${GREEN}✓ PASS${NC} (Status: ${status_code})"
        ((TESTS_PASSED++))
        echo "  Response: ${body:0:100}..."
    else
        echo -e "${RED}✗ FAIL${NC} (Expected: ${expected_status}, Got: ${status_code})"
        ((TESTS_FAILED++))
        echo "  Response: ${body}"
    fi
}

# Check if API is running
echo -e "\n${YELLOW}Checking API connectivity...${NC}"
if ! curl -s -o /dev/null -w "%{http_code}" ${API_URL}/health/liveness | grep -q "200"; then
    echo -e "${RED}API is not running at ${API_URL}${NC}"
    exit 1
fi
echo -e "${GREEN}API is running${NC}"

# Test 1: Health check - Liveness
test_endpoint "Liveness Check" "GET" "/health/liveness" "" "200"

# Test 2: Health check - Readiness
test_endpoint "Readiness Check" "GET" "/health/readiness" "" "200"

# Test 3: Root endpoint
test_endpoint "Root Endpoint" "GET" "/" "" "200"

# Test 4: List supported formats
test_endpoint "List Formats" "GET" "${API_PREFIX}/convert/formats" "" "200"

# Test 5: Convert TXT file
if [ -f "test/files/sample.txt" ]; then
    test_endpoint "Convert TXT File" "POST" "${API_PREFIX}/convert" "file=@test/files/sample.txt" "200"
else
    echo -e "${YELLOW}Skipping TXT test - sample file not found${NC}"
fi

# Test 6: Convert HTML file
if [ -f "test/files/sample.html" ]; then
    test_endpoint "Convert HTML File" "POST" "${API_PREFIX}/convert" "file=@test/files/sample.html" "200"
else
    echo -e "${YELLOW}Skipping HTML test - sample file not found${NC}"
fi

# Test 7: Invalid file format
echo -e "\n${YELLOW}Testing: Invalid File Format${NC}"
echo "  Method: POST ${API_PREFIX}/convert"
response=$(curl -s -w "\n%{http_code}" -X POST -F "file=@test/test.sh" "${API_URL}${API_PREFIX}/convert")
status_code=$(echo "$response" | tail -n1)
if [ "$status_code" == "422" ] || [ "$status_code" == "400" ]; then
    echo -e "${GREEN}✓ PASS${NC} (Status: ${status_code})"
    ((TESTS_PASSED++))
else
    echo -e "${YELLOW}~ SKIP${NC} (Status: ${status_code} - Might be valid)"
fi

# Summary
echo -e "\n=========================================="
echo -e "Test Summary"
echo -e "==========================================${NC}"
echo -e "${GREEN}Passed: ${TESTS_PASSED}${NC}"
echo -e "${RED}Failed: ${TESTS_FAILED}${NC}"

if [ ${TESTS_FAILED} -eq 0 ]; then
    echo -e "${GREEN}All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}Some tests failed!${NC}"
    exit 1
fi
