from kaiming_ascii import kaiming_ascii


def kaiming(name: str = "") -> None:
    """
    Kaiming Bless you!

    :param name: your name
    :return:
    """

    print(kaiming_ascii)

    IJCAI_ascii = r"""
                                    zz*
                                  zzo aan
                           ;vzzzzvz*   aazuuuu1
                          ovvzzzaa+     aauuuu11
                         *vvvzzza        auuuu111
                         vvvvzzz          nuuu1111
                        ~vvvvzz            *uu1111
                        nvvvvn              +u11111
                       -nvvv;                 11111
                       +nvn-       niiu        za1i
                     ;vzza.     .u11ii!!3z      vzzaz
                  onnvvzz      ~uu11ii!!336      zzaauu1
                oonnnvvv      +auu11ii!!3363      ;aauu11i~
              ~ooonnnvn       zauu11ii!!3366       -auu11iii*
            *~~ooonnn~        zauu11ii!!3366+       .uu11iii!!
           ;;~~ooonn+         zauu11ii!!3366          u11iii!!3o
          ;;;~~ooon           .auu11ii!!336a           11iii!!33a
         *;;;~~ooo             ;uu11ii!!33!             aiii!!336~
         .;;;~~oo               ~u11ii!!3!               vii!!33a
            ;;~~                 ^11ii!!v                 *i1ii
           *;;^                    uii!                    .336
           ;;-                                               36;
           +;;;;~*;;~~~oonnvvzzaauv     vvzaauu11ii!!3366!3333!
                 .;;~~~oonnvvzz^           vauu11ii!!3366
                  ;;~~~ooo*                    ^zii!!336^
        """

    if name == "":
        print("        kaiming bless you!")
    else:
        print(f"        kaiming bless you, {name}!")

    print(IJCAI_ascii)


if __name__ == "__main__":
    kaiming()
