from kaiming_ascii import kaiming_ascii


def kaiming(name: str = "") -> None:
    """
    Kaiming Bless you!

    :param name: your name
    :return:
    """

    print(kaiming_ascii)

    EMNLP_ascii = r"""
          -33333333333;    333333333333
          -3333333333        6333333333
          -3333333333           333333
          -33333333.              63~
          -3333336
          -33333        -3636
          -333~        33333336
          -33        633333333        6
          -         63333333         33
                  333333336        3333
                    33333        v33333
          -6          3         6333333
          -333                333333333
          -333336           *3333333333
          -zzzzzzzz        zzzzzzzzzzzz
        """

    if name == "":
        print("        kaiming bless you!")
    else:
        print(f"        kaiming bless you, {name}!")

    print(EMNLP_ascii)


if __name__ == "__main__":
    kaiming()
