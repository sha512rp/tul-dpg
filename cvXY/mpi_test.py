from mpi4py import MPI


def main():
    comm = MPI.COMM_WORLD

    rank = comm.rank
    size = comm.size
    data = 'no data'

    if rank == 0:
        for i in range(1, size):
            data = "Ping"
            comm.send(data, dest=i)
            print("Ping rank <{rank}>".format(rank=i))
            data = comm.recv(source=i)
            print(data)
    else:
        data = comm.recv(source=0)
        if data == "Ping":
            comm.send("Pong", dest=0)


if __name__ == '__main__':
    main()
