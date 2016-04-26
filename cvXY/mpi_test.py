from mpi4py import MPI


def main():
    comm = MPI.COMM_WORLD

    rank = comm.rank
    size = comm.size
    data = 'no data'

    if rank == 0:
        comm.bcast("Ping")
        print("Server sent.")
    else:
        data = comm.gather(data, root=0)
        print(data)


if __name__ == '__main__':
    main()
