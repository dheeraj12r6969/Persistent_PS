import os

class RouterConnectionFinder:
    def __init__(self, router_files):
        self.router_files = router_files
        self.router_connections = set()
        self.parsed_data_dict = {}

    def process_router_file(self, router_file):
        with open(router_file, 'r') as file:
            lines = file.readlines()
        router_ip = router_file.split('\\')[-1].split('_')[0]
        for line in lines:
            if 'Dynamic' in line:
                parts = line.split()
                ip_address = parts[0]
                hardware_addr = parts[2]
                self.router_connections.add(( ip_address, hardware_addr))
        # print(self.router_connections)   # We extracted the data as combination of  router_ip, ip_address, hardware_addr
        self.parsed_data_dict[router_ip]=self.router_connections
        # print(self.parsed_data_dict)

    def find_logical_connections(self):
        # dict of data having key as ip address and values as parsed data in form of tuple
        for router_file in self.router_files:
            self.process_router_file(router_file)  # Call process_router_file for each router file
            
        other_router_files = [f for f in self.router_files if f != router_file][0].split('\\')[-1].split('_')[0]
        router_ip = router_file.split('\\')[-1].split('_')[0]
        set1=self.parsed_data_dict[router_ip]
        set2=self.parsed_data_dict[other_router_files]

        common_tuples = set1.intersection(set2)
        # print("=================",common_tuples)

        if common_tuples is None:
            print("No logical connections found.")
        else:
            print("{}<->{}".format(router_ip, other_router_files))

if __name__ == "__main__":
    cwd = os.getcwd()
    router_directory = "example_for_ARP_match"
    router_files = [os.path.join(cwd, router_directory, file) for file in os.listdir(os.path.join(cwd, router_directory)) if file.endswith("_22")]

    # Create an instance of RouterConnectionFinder
    router_connection_finder = RouterConnectionFinder([os.path.join(router_directory, f) for f in router_files])

    # Find and print logical connections between routers
    router_connection_finder.find_logical_connections()
