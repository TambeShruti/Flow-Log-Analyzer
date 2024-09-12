import unittest
import csv
import os
from collections import defaultdict

# Ensure to import your actual functions
from main import load_lookup_table, process_flow_logs, write_results

class TestFlowLogProcessing(unittest.TestCase):

    def setUp(self):
        # Setup mock data
        self.lookup_table_file = 'test_lookup.csv'
        self.flow_log_file = 'test_flow_logs.txt'
        self.output_file = 'test_output.csv'

        # Mock lookup table data
        with open(self.lookup_table_file, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['Port', 'Protocol', 'Tag'])
            writer.writerow(['80', 'tcp', 'web'])
            writer.writerow(['53', 'udp', 'dns'])

        # Mock flow log data
        with open(self.flow_log_file, 'w') as f:
            f.write('Header1 Header2 Header3 Header4 Header5 Header6 Port Protocol\n')
            f.write('data data data data data 80 data 6\n')  # tcp
            f.write('data data data data data 53 data 17\n') # udp
            f.write('data data data data data 999 data 99\n') # unknown

    def test_load_lookup_table(self):
        lookup_table = load_lookup_table(self.lookup_table_file)
        print(f"Loaded lookup table: {lookup_table}")
        expected_lookup_table = {
            (80, 'tcp'): 'web',
            (53, 'udp'): 'dns'
        }
        self.assertEqual(lookup_table, expected_lookup_table)

    def test_process_flow_logs(self):
        lookup_table = load_lookup_table(self.lookup_table_file)
        tag_counts, port_protocol_counts, untagged_count = process_flow_logs(self.flow_log_file, lookup_table)
        print(f"Tag counts: {tag_counts}")
        print(f"Port/Protocol counts: {port_protocol_counts}")
        print(f"Untagged count: {untagged_count}")
        expected_tag_counts = {'web': 1, 'dns': 1}
        expected_port_protocol_counts = {
            (80, 'tcp'): 1,
            (53, 'udp'): 1,
            (999, 'unknown'): 1
        }
        self.assertEqual(tag_counts, expected_tag_counts)
        self.assertEqual(port_protocol_counts, expected_port_protocol_counts)
        self.assertEqual(untagged_count, 1)

    def test_write_results(self):
        lookup_table = load_lookup_table(self.lookup_table_file)
        tag_counts, port_protocol_counts, untagged_count = process_flow_logs(self.flow_log_file, lookup_table)
        write_results(self.output_file, tag_counts, port_protocol_counts, untagged_count)
        
        with open(self.output_file, 'r') as f:
            content = f.read()
        
        print(f"Output file content: {content}")
        
        expected_content = (
            "Tag Counts:\n"
            "Tag,Count\n"
            "web,1\n"
            "dns,1\n"
            "Untagged,1\n"
            "\nPort/Protocol Combination Counts:\n"
            "Port,Protocol,Count\n"
            "80,tcp,1\n"
            "53,udp,1\n"
            "999,unknown,1\n"
        )
        self.assertEqual(content, expected_content)

    def tearDown(self):
        try:
            if os.path.exists(self.lookup_table_file):
                os.remove(self.lookup_table_file)
            if os.path.exists(self.flow_log_file):
                os.remove(self.flow_log_file)
            if os.path.exists(self.output_file):
                os.remove(self.output_file)
        except Exception as e:
            print(f"Error during cleanup: {e}")

if __name__ == '__main__':
    unittest.main()
