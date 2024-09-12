import csv
import os
import unittest
from collections import defaultdict

# Function to convert protocol numbers to protocol names
def protocol_name(protocol_num):
    if protocol_num == "6":
        return "tcp"
    elif protocol_num == "17":
        return "udp"
    elif protocol_num == "1":
        return "icmp"
    else:
        return "unknown"

# Function to load lookup table from a CSV file
def load_lookup_table(lookup_table_file):
    lookup_table = {}
    with open(lookup_table_file, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header
        for row in reader:
            if len(row) == 3:
                try:
                    dstport = int(row[0])
                    protocol = row[1].strip().lower()
                    tag = row[2].strip()
                    lookup_table[(dstport, protocol)] = tag
                except ValueError:
                    print(f"Skipping invalid row in lookup table: {row}")
    return lookup_table


# Function to preprocess flow logs and map to tags
def process_flow_logs(flow_log_file, lookup_table):
    tag_counts = defaultdict(int)
    port_protocol_counts = defaultdict(int)
    untagged_count = 0
    
    with open(flow_log_file, 'r') as f:
        for line in f:
            row = line.split()
            try:
                # Adjust field indices based on actual log structure
                destination_port = int(row[5])
                protocol_num = row[7]
                protocol = protocol_name(protocol_num).lower()  # Convert to protocol name and ensure lowercase
                
                # Determine the tag based on destination port and protocol
                key = (destination_port, protocol)
                tag = lookup_table.get(key, 'unknown')
                
                # Update counts
                if tag == 'unknown':
                    untagged_count += 1
                else:
                    tag_counts[tag] += 1
                
                port_protocol_counts[(destination_port, protocol)] += 1
                
            except (IndexError, ValueError) as e:
                print(f"Skipping invalid line: {line.strip()} due to {e}")

    return tag_counts, port_protocol_counts, untagged_count


# Function to write results to a file
def write_results(output_file, tag_counts, port_protocol_counts, untagged_count):
    with open(output_file, 'w') as f:
        f.write("Tag Counts:\n")
        f.write("Tag,Count\n")
        for tag, count in tag_counts.items():
            f.write(f"{tag},{count}\n")
        f.write(f"Untagged,{untagged_count}\n")
        
        f.write("\nPort/Protocol Combination Counts:\n")
        f.write("Port,Protocol,Count\n")
        for (port, protocol), count in port_protocol_counts.items():
            f.write(f"{port},{protocol},{count}\n")

# Main function
def main():
    lookup_table = load_lookup_table('lookup.csv')
    tag_counts, port_protocol_counts, untagged_count = process_flow_logs('flow_logs.txt', lookup_table)
    write_results('output.csv', tag_counts, port_protocol_counts, untagged_count)
    print("Processing complete! Results written to output.csv.")

if __name__ == '__main__':
    main()
