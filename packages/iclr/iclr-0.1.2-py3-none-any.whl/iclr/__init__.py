from kaiming_ascii import kaiming_ascii


def kaiming(name: str = "") -> None:
    """
    Kaiming Bless you!

    :param name: your name
    :return:
    """

    print(kaiming_ascii)

    ICLR_ascii = r"""
        IIIIIIIIII      CCCCCCCCCCCCCLLLLLLLLLLL             RRRRRRRRRRRRRRRRR
        I::::::::I   CCC::::::::::::CL:::::::::L             R::::::::::::::::R
        I::::::::I CC:::::::::::::::CL:::::::::L             R::::::RRRRRR:::::R
        II::::::IIC:::::CCCCCCCC::::CLL:::::::LL             RR:::::R     R:::::R
          I::::I C:::::C       CCCCCC  L:::::L                 R::::R     R:::::R
          I::::IC:::::C                L:::::L                 R::::R     R:::::R
          I::::IC:::::C                L:::::L                 R::::RRRRRR:::::R
          I::::IC:::::C                L:::::L                 R:::::::::::::RR
          I::::IC:::::C                L:::::L                 R::::RRRRRR:::::R
          I::::IC:::::C                L:::::L                 R::::R     R:::::R
          I::::IC:::::C                L:::::L                 R::::R     R:::::R
          I::::I C:::::C       CCCCCC  L:::::L         LLLLLL  R::::R     R:::::R
        II::::::IIC:::::CCCCCCCC::::CLL:::::::LLLLLLLLL:::::LRR:::::R     R:::::R
        I::::::::I CC:::::::::::::::CL::::::::::::::::::::::LR::::::R     R:::::R
        I::::::::I   CCC::::::::::::CL::::::::::::::::::::::LR::::::R     R:::::R
        IIIIIIIIII      CCCCCCCCCCCCCLLLLLLLLLLLLLLLLLLLLLLLLRRRRRRRR     RRRRRRR
        """

    if name == "":
        print("        kaiming bless you!")
    else:
        print(f"        kaiming bless you, {name}!")

    print(ICLR_ascii)


if __name__ == "__main__":
    kaiming()
