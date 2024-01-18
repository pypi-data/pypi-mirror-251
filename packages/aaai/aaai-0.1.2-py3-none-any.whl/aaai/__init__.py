from kaiming_ascii import kaiming_ascii


def kaiming(name: str = "") -> None:
    """
    Kaiming Bless you!

    :param name: your name
    :return:
    """

    print(kaiming_ascii)

    AAAI_ascii = r"""

                       ..
                       %%
                      %%%3
                    n%%%%.8%
                   &%%%6 $%%$
                  $%%%3 %%%%% .
                 8%%%% &%%%& %%.
                %6%%$ 8%%%! %%%8
               %%%83 %%%8* %    $
              %%%%; %%%%  %      8
            .%%%%..%%%8 .%%8    %%%
            %%%8  8%%%. %%%%%%%%%%%%.
          .%%%%  %%%% ^%%%%      %%%8
         .%%%%-*%%%% u8%%%%      %%%%%-
        """

    if name == "":
        print("        kaiming bless you!")
    else:
        print(f"        kaiming bless you, {name}!")

    print(AAAI_ascii)


if __name__ == "__main__":
    kaiming()
