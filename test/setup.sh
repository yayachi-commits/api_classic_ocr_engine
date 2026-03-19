#!/bin/bash
# Setup script for testing the API

set -e

echo "Setting up test environment..."

# Create test directory structure
mkdir -p test/files
mkdir -p test/output

# Create sample test files
echo "Creating sample test files..."

# Sample TXT file
cat > test/files/sample.txt << 'EOF'
This is a sample text file.
It contains multiple lines.
Each line should be extracted as a separate paragraph.

This is a second paragraph with some content.
EOF

# Sample HTML file
cat > test/files/sample.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>Sample HTML</title>
</head>
<body>
    <h1>Sample Document</h1>
    <p>This is a paragraph with content.</p>
    <p>This is another paragraph.</p>
    <script>console.log('This should be removed')</script>
</body>
</html>
EOF

echo "Sample files created in test/files/"
echo "Setup complete!"
