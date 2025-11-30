"""
Clean up text file by removing extra line feeds
Makes everything single-spaced while keeping all content
"""

input_file = 'neverloseajob-originalchat.txt'
output_file = 'neverloseajob-originalchat.txt'

# Read the file
with open(input_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Remove empty lines and extra whitespace
cleaned_lines = []
for line in lines:
    stripped = line.rstrip('\r\n')
    if stripped:  # Only keep non-empty lines
        cleaned_lines.append(stripped)

# Write back with single spacing
with open(output_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(cleaned_lines))

print(f"Cleaned {len(lines)} lines down to {len(cleaned_lines)} lines")
print("Removed all extra line feeds - file is now single-spaced")
