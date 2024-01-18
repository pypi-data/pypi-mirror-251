from kaiming_ascii import kaiming_ascii


def kaiming(name: str = "") -> None:
    """
    Kaiming Bless you!

    :param name: your name
    :return:
    """

    print(kaiming_ascii)

    IJCV_ascii = r"""
        IIIIIIIIII          JJJJJJJJJJJ      CCCCCCCCCCCCCVVVVVVVV           VVVVVVVV
        I::::::::I          J:::::::::J   CCC::::::::::::CV::::::V           V::::::V
        I::::::::I          J:::::::::J CC:::::::::::::::CV::::::V           V::::::V
        II::::::II          JJ:::::::JJC:::::CCCCCCCC::::CV::::::V           V::::::V
          I::::I              J:::::J C:::::C       CCCCCC V:::::V           V:::::V
          I::::I              J:::::JC:::::C                V:::::V         V:::::V
          I::::I              J:::::JC:::::C                 V:::::V       V:::::V
          I::::I              J:::::jC:::::C                  V:::::V     V:::::V
          I::::I              J:::::JC:::::C                   V:::::V   V:::::V
          I::::I  JJJJJJJ     J:::::JC:::::C                    V:::::V V:::::V
          I::::I  J:::::J     J:::::JC:::::C                     V:::::V:::::V
          I::::I  J::::::J   J::::::J C:::::C       CCCCCC        V:::::::::V
        II::::::IIJ:::::::JJJ:::::::J  C:::::CCCCCCCC::::C         V:::::::V
        I::::::::I JJ:::::::::::::JJ    CC:::::::::::::::C          V:::::V
        I::::::::I   JJ:::::::::JJ        CCC::::::::::::C           V:::V
        IIIIIIIIII     JJJJJJJJJ             CCCCCCCCCCCCC            VVV
        """

    if name == "":
        print("        kaiming bless you!")
    else:
        print(f"        kaiming bless you, {name}!")

    print(IJCV_ascii)


if __name__ == "__main__":
    kaiming()
