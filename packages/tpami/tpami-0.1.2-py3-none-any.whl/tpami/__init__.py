from kaiming_ascii import kaiming_ascii


def kaiming(name: str = "") -> None:
    """
    Kaiming Bless you!

    :param name: your name
    :return:
    """

    print(kaiming_ascii)

    TPAMI_ascii = r"""
        TTTTTTTTTTTTTTTTTTTTTTTPPPPPPPPPPPPPPPPP        AAA               MMMMMMMM               MMMMMMMMIIIIIIIIII
        T:::::::::::::::::::::TP::::::::::::::::P      A:::A              M:::::::M             M:::::::MI::::::::I
        T:::::::::::::::::::::TP::::::PPPPPP:::::P    A:::::A             M::::::::M           M::::::::MI::::::::I
        T:::::TT:::::::TT:::::TPP:::::P     P:::::P  A:::::::A            M:::::::::M         M:::::::::MII::::::II
        TTTTTT  T:::::T  TTTTTT  P::::P     P:::::P A:::::::::A           M::::::::::M       M::::::::::M  I::::I
                T:::::T          P::::P     P:::::PA:::::A:::::A          M:::::::::::M     M:::::::::::M  I::::I
                T:::::T          P::::PPPPPP:::::PA:::::A A:::::A         M:::::::M::::M   M::::M:::::::M  I::::I
                T:::::T          P:::::::::::::PPA:::::A   A:::::A        M::::::M M::::M M::::M M::::::M  I::::I
                T:::::T          P::::PPPPPPPPP A:::::A     A:::::A       M::::::M  M::::M::::M  M::::::M  I::::I
                T:::::T          P::::P        A:::::AAAAAAAAA:::::A      M::::::M   M:::::::M   M::::::M  I::::I
                T:::::T          P::::P       A:::::::::::::::::::::A     M::::::M    M:::::M    M::::::M  I::::I
                T:::::T          P::::P      A:::::AAAAAAAAAAAAA:::::A    M::::::M     MMMMM     M::::::M  I::::I
              TT:::::::TT      PP::::::PP   A:::::A             A:::::A   M::::::M               M::::::MII::::::II
              T:::::::::T      P::::::::P  A:::::A               A:::::A  M::::::M               M::::::MI::::::::I
              T:::::::::T      P::::::::P A:::::A                 A:::::A M::::::M               M::::::MI::::::::I
              TTTTTTTTTTT      PPPPPPPPPPAAAAAAA                   AAAAAAAMMMMMMMM               MMMMMMMMIIIIIIIIII
        """

    if name == "":
        print("        kaiming bless you!")
    else:
        print(f"        kaiming bless you, {name}!")

    print(TPAMI_ascii)


if __name__ == "__main__":
    kaiming()
