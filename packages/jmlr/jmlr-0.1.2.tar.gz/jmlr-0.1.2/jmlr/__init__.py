from kaiming_ascii import kaiming_ascii


def kaiming(name: str = "") -> None:
    """
    Kaiming Bless you!

    :param name: your name
    :return:
    """

    print(kaiming_ascii)

    JMLR_ascii = r"""
                  JJJJJJJJJJJMMMMMMMM               MMMMMMMMLLLLLLLLLLL             RRRRRRRRRRRRRRRRR
                  J:::::::::JM:::::::M             M:::::::ML:::::::::L             R::::::::::::::::R
                  J:::::::::JM::::::::M           M::::::::ML:::::::::L             R::::::RRRRRR:::::R
                  JJ:::::::JJM:::::::::M         M:::::::::MLL:::::::LL             RR:::::R     R:::::R
                    J:::::J  M::::::::::M       M::::::::::M  L:::::L                 R::::R     R:::::R
                    J:::::J  M:::::::::::M     M:::::::::::M  L:::::L                 R::::R     R:::::R
                    J:::::J  M:::::::M::::M   M::::M:::::::M  L:::::L                 R::::RRRRRR:::::R
                    J:::::j  M::::::M M::::M M::::M M::::::M  L:::::L                 R:::::::::::::RR
                    J:::::J  M::::::M  M::::M::::M  M::::::M  L:::::L                 R::::RRRRRR:::::R
        JJJJJJJ     J:::::J  M::::::M   M:::::::M   M::::::M  L:::::L                 R::::R     R:::::R
        J:::::J     J:::::J  M::::::M    M:::::M    M::::::M  L:::::L                 R::::R     R:::::R
        J::::::J   J::::::J  M::::::M     MMMMM     M::::::M  L:::::L         LLLLLL  R::::R     R:::::R
        J:::::::JJJ:::::::J  M::::::M               M::::::MLL:::::::LLLLLLLLL:::::LRR:::::R     R:::::R
         JJ:::::::::::::JJ   M::::::M               M::::::ML::::::::::::::::::::::LR::::::R     R:::::R
           JJ:::::::::JJ     M::::::M               M::::::ML::::::::::::::::::::::LR::::::R     R:::::R
             JJJJJJJJJ       MMMMMMMM               MMMMMMMMLLLLLLLLLLLLLLLLLLLLLLLLRRRRRRRR     RRRRRRR
        """

    if name == "":
        print("        kaiming bless you!")
    else:
        print(f"        kaiming bless you, {name}!")

    print(JMLR_ascii)


if __name__ == "__main__":
    kaiming()
