"""Python zero division error."""


def main():
    array1 = range(5)
    array2 = [1, 2, 3, 0, 4]

    for i in range(6):
        try:
            print(array1[i]/array2[i])
        except ZeroDivisionError:
            print('Zero division!')
        except IndexError:
            print('Out of bounds!')
        finally:
            print('Processed.')

if __name__ == '__main__':
    main()
