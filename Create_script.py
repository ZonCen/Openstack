import openstack

# Initate connection
conn = openstack.connect(cloud="kna1")

#Create Volumes
def create_volumes(conn):
    print("Creating volumes")
    myVolumes = []
    for volume in conn.block_storage.volumes():
        myVolumes.append(volume.name)
    conn.block_storage.create_volume(size=50, name="Volume_From_Python_Script_" + str(len(myVolumes) + 1), description="Test Volume created from python script")

#Create everything
def all_create(conn):
    print("Creating Servers")
    amount = input("How many servers do you want to create?: ")
    i = 0
    while i < int(amount):
        serverList = []
        for server in conn.compute.servers():
            serverList.append(server.name)
        number = len(serverList) + 1
        print(i)
        print("Creating server")
        image = conn.compute.find_image("Ubuntu 20.04 Focal Fossa 20200423")
        print("Using image " + image.id)
        flavor = conn.compute.find_flavor("1C-1GB-50GB")
        print("Using flavor " + flavor.id)
        network = attach_network(conn)
        print("Using network " + network.id)
        server = conn.compute.create_server(name="Python_Server_Created_" + str(number), image_id=image.id, flavor_id=flavor.id, networks=[{"uuid": network.id}])
        conn.compute.wait_for_server(server)
        print(server.name + " is now " +server.status)
        i += 1
        create_volumes(conn)

    print("Creating server images")
    print("List of servers we will create snapshots from: ")
    for server in conn.compute.servers():
        print(server.name)
    for server in conn.compute.servers():
        conn.compute.create_server_image(server, f'test_image_{server.name}', metadata=None, wait=False, timeout=120)
        print(server.name + " has now status " +server.status)
        conn.compute.wait_for_server(server)

    print("Creating volume snapshots")
    for volume in conn.block_storage.volumes():
        print(volume.name)
        conn.block_storage.create_snapshot(name=volume.name, volume_id=volume.id)

def attach_network(conn):
    name = create_network(conn)
    return name

# Create networks
def create_network(conn):
    print("Creating network")
    myNetworks=[]
    for network in conn.network.networks():
        if network.is_router_external == False:
            myNetworks.append(network.name)
    createdNetwork=conn.network.create_network(
            name="Network_Created_From_Python_" + (str(len(myNetworks) +1)))
    createdSubnet=conn.network.create_subnet(
            name="Subnet_Created_From_Python_" + (str(len(myNetworks) +1 )),
            network_id=createdNetwork.id,
            ip_version='4',
            cidr='10.1.0.0/24',
            gateway_ip='10.1.0.1')
    createdRouter=conn.network.create_router(
            name="Router_Created_From_Python_" + (str(len(myNetworks) +1)))
            #add_interface=createdSubnet.id,
            #network_id=createdNetwork.id,
            #subnet_id=createdSubnet)
    return createdNetwork

all_create(conn)