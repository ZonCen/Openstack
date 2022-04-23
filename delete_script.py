import openstack
import time

# Initialise connection
conn = openstack.connect(cloud="kna1")

# Delete code for everything
def all_delete(c):
    print("Deleting images: ")
    for image in c.image.images():
        if image.visibility == "private":
            print(image.name + " " + image.visibility)
            c.image.delete_image(image)
            print("Deleted")

    print("Deleting servers: ")
    for server in c.compute.servers():
        c.compute.delete_server(server.id)
        print(server.name + " deleted")

    print("Deleting volume snapshots: ")
    for snapshot in c.block_storage.snapshots():
        print(snapshot.name + " is being deleted")
        c.block_storage.delete_snapshot(snapshot.id)

    time.sleep(10)
    print("Deleting ports")
    for port in c.network.ports():
        if port.device_owner != "None":
            c.network.update_port(port, device_owner="None")
        c.network.delete_port(port)
    print("Deleting subnets")
    for subnet in c.network.subnets():
        c.network.delete_subnet(subnet)
    print("Deleting networks")
    for network in c.network.networks():
        if network.name != "ext-net":
            print("Deleting network: " + network.name)
            c.network.delete_network(network)
    print("Deleting router")
    for router in c.network.routers():
        print("Deleting router: " + router.name)
        c.network.delete_router(router)

    print("Deleting volumes: ")
    for volume in c.block_storage.volumes():
        print(volume.name + " is being deleted")
        print(volume.status)
        c.block_storage.delete_volume(volume)

    print("All done")


all_delete(conn)
