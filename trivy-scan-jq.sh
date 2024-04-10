#!/bin/bash

# Path to the file containing the list of images
image_file="docker-image-list-3.txt" # Update this path as per your file system

# Output file for extracted data
extracted_output_file="extracted_vulnerability_info_3.txt"

# Putting an opening square bracket
#echo '[' > "$extracted_output_file"

# Check if the image file exists
if [ ! -f "$image_file" ]; then
    echo "Image file does not exist: $image_file"
    exit 1
fi

# Loop through each image from the file and run the scan
while IFS= read -r image; do
    echo "Scanning $image..."
    # Run Trivy and save the JSON output to a temporary file
    trivy image --format json "$image" > temp.json
    
    # Extract ArtifactName, VulnerabilityID, PkgName, and Severity, append to the final output file
    jq -c '.ArtifactName as $artifact | .Results[] | .Vulnerabilities[] | {ArtifactName: $artifact, VulnerabilityID, PkgName, Severity} + {","}' temp.json >> "$extracted_output_file"

    echo "," >> "$extracted_output_file" # Add a comma after each object
done < "$image_file"

# Remove the trailing comma from the last object
truncate -s -1 "$extracted_output_file"

# Add the closing square bracket
#echo ']' >> "$extracted_output_file"

rm temp.json  # Clean up temporary file
echo "Scanning completed. Extracted results are in $extracted_output_file"
