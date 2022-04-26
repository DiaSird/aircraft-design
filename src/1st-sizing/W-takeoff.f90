!------------------------------------------------------------------------------
!
! MODULE: parameters
!
! DESCRIPTION:
!>  パラメータ定義
!
! REVISION HISTORY:
! 06 11 2021 - Initial Version
! 26 04 2022 - Updated
!------------------------------------------------------------------------------
module parameters
    implicit none
    integer, parameter :: t_max = 1000

!---Specification 設計要求
    ! prameter: air(craft)
    ! 1 = ジェット旅客機
    ! 2 = リージョナルジェット機
    ! 3 = 単発軽飛行機
    integer, parameter :: air = 1

    ! sound of air
    double precision, parameter :: air_sound = 296.6
    double precision, parameter :: Mach = 0.82
    ! cruise velocity V [knot]
    double precision, parameter :: V_cruise = air_sound / Mach
    ! Range R [nm, nautical mile]
    double precision, parameter :: R = 5000
    ! Payload WPL [lb]
    double precision, parameter :: WPL = 64698

!---初期推定重量
    double precision :: WTO_init = 400000.d0 ! WTO_guess [lb]
    ! double precision :: WTO_init = 520000.d0 ! WTO_guess [lb]
    ! Maximum take-off weight WTO [lb]
    double precision :: WTO
    ! 重量の増分
    double precision, parameter :: dW = 10000.d0

!---Parameters
    double precision :: W
    double precision :: Mff
    double precision :: C, efficient_p
    double precision :: cj,  cp, LD
    double precision :: E_ltr, cj_ltr, LD_ltr

end module

!------------------------------------------------------------------------------
!
! MAIN PROGRAM: first_sizing
!
! REVISION HISTORY:
! 06 11 2021 - Initial Version
!------------------------------------------------------------------------------
!
program first_sizing
    use parameters
    implicit none
    double precision :: A, B

    call initialize
    call Breguet(air)
    call mission_fuel_fraction(air)
    call aircraft_parameter(A, B, air)
    call Output(A, B)
    stop

end program

!------------------------------------------------------------------------------
!
! SUBROUTINE:initialize
!
!
! REVISION HISTORY:
! 06 11 2021 - Initial Version
!------------------------------------------------------------------------------
!
subroutine initialize
    use parameters
    implicit none

!---初期推定重量
    WTO = WTO_init

!---ジェット旅客機 green, pp.73 ~ 74
    ! 例題4.2
    cj = 0.5d0 ! Turbofan engine cj = 0.5 ~ 0.8 [(lb/hr)/lb]
    LD = 15.d0 ! L/D = 13 ~ 15 or 15 ~

    ! ltr = loiter, holding (green, p.74)
    E_ltr = 45.d0 / 60.d0 ! E_ltr [min/1hr = hr]
    cj_ltr = 0.4d0 ! cj_ltr = 0.4 ~ 0.6 [(lb/hr)/lb]
    LD_ltr = 18.d0 ! (L/D)ltr = 14 ~ 18

!---プロペラ機
    C = 326.d0 ! 単位換算係数
    efficient_p = 0.8 ! プロペラ効率
    cj = 0.4d0 ! Turbofan engine cj = 0.5 ~ 0.8 [(lb/hr)/lb]
    LD = 18.d0 ! L/D = 13 ~ 15 or 15 ~

!---Output
    write (*, *) ""
    write (*, *) "-- Initialize --"
    write (*, *) "You guessed take-off weight WTO [lb] = "
    write (*, "(f15.4)") WTO

end subroutine

!------------------------------------------------------------------------------
!
! SUBROUTINE: Breguet
!
!
! DESCRIPTION:
!>  Calculate weight ratio with Breguet range formula
!
! REVISION HISTORY:
! 06 11 2021 - Initial Version
!------------------------------------------------------------------------------
!
subroutine Breguet(n)
    use parameters
    implicit none
    integer n
    double precision :: W5W4, W6W5


    if ( n == 1) then
        W5W4 = exp(- R / (V_cruise / cj) / LD)
        W6W5 = exp(- E_ltr / (V_cruise / cj_ltr) / LD_ltr)
        W = W5W4 * W6W5 ! W5/W4 * W6/W5

        write(*, *) ""
        write (*, *) "-- Breguet Range formula Phase 5 and 6 --"
        write (*, "(A, f10.4)") "cruise weight ratio = ", W5W4
        write (*, "(A, f10.4)") "loiter weight ratio = ", W6W5

    else if ( n == 2) then
        W5W4 = exp(- R / (C * efficient_p / cp) / LD)
        W = W5W4

        write(*, *) ""
        write (*, *) "-- Breguet Range formula Phase 5 and 6 --"
        write (*, "(A, f10.4)") "cruise weight ratio = ", W5W4

    end if

    return
end subroutine

!------------------------------------------------------------------------------
!
! SUBROUTINE: mission_fuel_fraction
!
!
! DESCRIPTION:
!>  Calculate Mff = mission fuel fraction
!  フライト時の機体重量比を算出
!
! REVISION HISTORY:
! 06 11 2021 - Initial Version
!------------------------------------------------------------------------------
!
subroutine mission_fuel_fraction(n)
    use parameters
    implicit none

    integer n
    double precision :: a
    double precision :: W1WTO, W2W1
    double precision :: W3W2, W4W3
    double precision :: W5W4_W6W5
    double precision :: W7W6, W8W7

    a = 0.99d0
    if ( n == 1 ) then
        W1WTO = a
        W2W1 = a
        W3W2 = a + 0.005d0
        W4W3 = a - 0.01d0
        W5W4_W6W5 = W
        W7W6 = a
        W8W7 = a + 0.002d0

    else if ( n == 2 ) then
        W1WTO = a
        W2W1 = a
        W3W2 = a + 0.005d0
        W4W3 = a - 0.01d0
        W5W4_W6W5 = W
        W7W6 = a
        W8W7 = a + 0.002d0

    else if ( n == 3 ) then
        W1WTO = a + 0.005d0
        W2W1 = a + 0.007d0
        W3W2 = a + 0.008d0
        W4W3 = a - 0.02d0
        W5W4_W6W5 = W
        W7W6 = a + 0.003d0
        W8W7 = a + 0.003d0
    end if

    Mff = W1WTO * W2W1 * W3W2 * W4W3 * W5W4_W6W5 * W7W6 * W8W7
    write (*, *) ""
    write (*, *) "-- Mission fuel fraction --"
    write (*, "(A, f16.4)") "W5/W4 * W6/W5 =", W
    write (*, "(A, f16.4)") "Mff =", Mff
    write (*, *) "Therefore,"
    write (*, "(A, f16.4)") "1 - Mff =", 1 - Mff

    return
end subroutine

!------------------------------------------------------------------------------
!
! SUBROUTINE: aircraft_parameter
!
! DESCRIPTION:
!>  統計関係式で使用するパラメータA,Bの入力
!
! REVISION HISTORY:
! 06 11 2021 - Initial Version
!------------------------------------------------------------------------------
!
subroutine aircraft_parameter(A, B, n)
    implicit none
    integer n
    double precision :: A, B

    ! prameter: n
    ! 1 = ジェット旅客機
    ! 2 = リージョナルジェット機
    ! 3 = 単発軽飛行機
    if ( n == 1 ) then
        A = - 0.163d0
        B = 1.084d0

    else if ( n == 2 ) then
        A = 0.186d0
        B = 1.012d0

    else if ( n == 3 ) then
        A = - 0.144d0
        B = 1.116d0

    end if

    return
end subroutine

!------------------------------------------------------------------------------
!
! SUBROUTINE:Output
!
!
! DESCRIPTION:
!>  機体重量の計算と出力
!
! REVISION HISTORY:
! 06 11 2021 - Initial Version
!------------------------------------------------------------------------------
!
subroutine Output(A, B)
    use parameters
    implicit none

    integer i
    double precision :: k
    double precision :: WOE, WF
    double precision :: A, B, temp
    double precision :: Error, WOE_tent

    ! Loop
    do i = 1, t_max
        k = 0.d0
        WF = ((1 - Mff) + k) * WTO
        ! WF = 0.365 * WTO ! 例題4.2: 1 - Mff = 0.365
        WOE_tent = WTO - WF - WPL ! WOE = WTO - (1 - Mff) WTO - WFres - WPL

!-------Statistic data elimination for WOE
        ! log10(WTO) = A + B log10(WE)
        ! log10(WTO) = A' + B' log10(WOE)
        temp = WTO * 10 ** (- A)
        WOE = temp ** (1 / B)

!-------Output
        Error = 1 - WOE / WOE_tent
        if ( abs(Error) <= 0.05 ) then
            write (*, *) ""
            write (*, *) "-- Successfully. --"
            write (*, "(A, f15.4)") "WOE_tent = ", WOE_tent
            write (*, "(A, f15.4)") "WOE = ", WOE
            write (*, "(A, f15.4)") "|WOE - WOE_tent| = ", abs(Error)
            write (*, *) ""
            write (*, *) "--    Resuls    --"
            write (*, "(A, f15.4)") "WTO = ", WTO
            write (*, "(A, f15.4)") "WOE = ", WOE
            write (*, "(A, f15.4)") "WF  = ", WF
            write (*, *) ""
            stop
        else
            write (*, *) ""
            write (*, *) "--     Weight error.     --"
            ! write (*, "(A, f15.4)") "WTO = ", WTO
            write (*, "(A, f15.4)") "WOE_tent = ", WOE_tent
            write (*, "(A, f15.4)") "WOE = ", WOE
            write (*, "(A, f15.4)") "|WOE - WOE_tent| = ", abs(Error)
            write (*, *) ""
            write (*, *) "Change guessed take off Weight. You need to repeat."
            write (*, *) ""
        end if
        WTO = WTO + dW
    end do

    return
end subroutine
