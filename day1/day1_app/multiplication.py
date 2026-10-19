def multiplication_table():
    for dan in range(2, 5):
        for i in range(1, 5):
            print(f"{dan} X {i} = {dan * i}", end="\t")
        print("\n======================")
