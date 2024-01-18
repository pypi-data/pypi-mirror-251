from kaiming_ascii import kaiming_ascii


def kaiming(name: str = "") -> None:
    """
    Kaiming Bless you!

    :param name: your name
    :return:
    """

    print(kaiming_ascii)

    ECCV_ascii = r"""
                                                                                              azzzz
                                                                                             +zzzz~
                                                                                             zzzzz
                                                                                            zzzzz
                                                                                           azzzz
                                                                                           zzzza
                  @@@@@@@@@@@@@@@@*        1@@@@@@@@@         @@@@@@@@@^  @@@@@           zzzzz
                  @@@@@@@@@@@@@@@@*     3@@@@@@@@@@@@      @@@@@@@@@@@@^   @@@@@         zzzzz
                                       @@@@@@@-          @@@@@@@$          ;@@@@i       ozzzz-
                                      @@@@@             @@@@@@              @@@@@       zzzza
                                     @@@@@             z@@@@                 @@@@@     zzzzz
         zzzzzzzzzzzzzzzzzzzzzzzzz-  @@@@+             @@@@@                  @@@@@    azzz
         zzzzzzzzzzzzzzzzzzzzzzzzz-  @@@@@             @@@@@                  &@@@@     zzn
                                     @@@@@+             @@@@@                  @@@@@     z
                                      @@@@@@             @@@@@@                 @@@@@
                  @@@@@@@@@@@@@@@@*    +@@@@@@@@@@@@@     @@@@@@@@@@@@@^        .@@@@%
                  @@@@@@@@@@@@@@@@*       @@@@@@@@@@@       @@@@@@@@@@@^         @@@@@
                  ++++++++++++++++              .....             .....           +++++
         """

    if name == "":
        print("        kaiming bless you!")
    else:
        print(f"        kaiming bless you, {name}!")

    print(ECCV_ascii)


if __name__ == "__main__":
    kaiming()
