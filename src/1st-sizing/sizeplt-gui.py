'''
--- Aircraft Design ---
sizing plot for civil-jet (Far 25)
*FAR = Federal Aviation Regulation
Ref. Kenichi Rinoie, "Aircraft
    Design method - conceptual design
    from single pulloperant to SST - "
'''
import time
import math
import PySimpleGUI as sg
import matplotlib.pyplot as plt


class SizingPlot():
    def __init__(self):
        # -- Set the graph parameters --
        # common
        self.m = 200    # range of axis-x
        self.fit = 25   # fitting parameter
        self.x = []     # x: (W/S)_TO

        # 1. take-off   * y: (T/W)_TO
        self.y1 = []
        self.y2 = []
        self.y3 = []

        # 2. land       * x = const.
        self.x1 = []
        self.x2 = []
        self.x3 = []
        self.x4 = []

        # 3. climb      * y = const.
        self.y4 = []

        # 4. cruise
        # x_cr is defined because of
        # defensing division by zero
        # (x[0] = 0.0)
        self.x_cr = []
        self.y5 = []

        # range of the x-direction
        for i in range(self.m):
            i = float(i)
            self.x.append(i)

        for j in range(self.fit, self.m, 1):
            j = float(j)
            self.x_cr.append(j)

        # # -- Design Requirements --
        # Initialize
        # s_tofl: take-off field length
        self.s_tofl = 0.0  # [ft]

        # s_fl: FAR landing field length
        self.s_fl = 0.0   # [ft]

        # m_cruise: Mach number on cruise
        #           definition  M := V/a
        self.m_cruise = 0.80

    def set_param(self):
        # a_ratio:
        # sound speed ratio between
        # the height and sea level
        # Height 35000 [ft];
        # approximately a_ratio = 0.87
        self.a_ratio = 0.87

        # v_cruise:
        # velocity on cruise, where
        # sound speed on sea level is
        # 340.3 [m/s]
        a = self. a_ratio * 340.3
        self.v_cruise = self.m_cruise * a
        # transform: 1 [m/s] = 3.281 [ft/s]
        self.v_cruise = 3.281 * self.v_cruise

        # -- 1. Take-off parameters --
        # sigma1:
        # density ratio between
        # height and surface of the sea
        self.sigma1 = 1.0

        # c1 = C_maxTO:
        # maximum coefficient of
        # lift in taking-off
        # approximately 1.6-2.2
        self.c1 = [1.6, 2.0, 2.2]

        # -- 2. Land parameters --
        # sigma2:
        # density ratio between
        # height and surface of
        # the sea
        self.sigma2 = self.sigma1
        # c2 = C_maxL:
        # maximum coefficient of
        # lift in landing
        # approximately 1.8-3.0
        self.c2 = [1.8, 2.2, 2.6, 3.0]

        # output variable c
        self.c = []
        for i in range(3):
            self.c.append(self.c1[i])

        for j in range(4):
            self.c.append(self.c2[j])

        # V_SL: stall speed
        self.V_SL = ((self.s_fl / 0.29) **
                     0.5 / 1.3)  # [knot]

        # -- 3. climb parameters --
        # gamma:
        # minimum of the climb gradient
        # for the twin engines; Far25.121
        self.gamma = 0.024

        # C3 = C_LmaxTO:
        # maximum coefficient of lift
        # in taking-off
        # approximately 1.6-2.2
        self.C3 = 2.0

        # calculation parameter
        # lift_drag (= lift-drag ratio)
        # ====================================
        # C_L:
        # lift coefficient in clean status
        # The rule of C_LmaxTO
        # = 1.2^2 * C_L, thus
        self.C_L = self.C3 / (1.2 ** 2)

        # C_FE:
        # equivalent skin friction coefficient
        # approximately 0.003
        self.C_FE = 0.003

        # SR: area ratio between
        # wetted area and reference area
        # SR = S_wet/S_ref
        # * decide from the existing airplane
        self.SR = 5.8

        # c_d0:
        # parasite drag;
        # c_d0 = C_FE * S_wet/S_ref
        # where take-off flap (+0.015)
        # in legs putted away
        self.c_d0 = (self.C_FE * self. SR +
                     0.015)

        #  e_f:
        # Oswalift_drag's efficiency
        # factor (max: e = 1)
        # where take-off flap
        # in legs putted away
        self.e_f = 0.8

        # ar:
        # aspect ratio
        # * decide from the existing airplane
        self.ar = 8.0

        # C_D:
        # drag coefficient in the clean form
        # "clean form" is the status that
        # flap and legs are putted away.
        # C_D = C_D0 + C_L^2/eπAR
        self.C_D = (self.c_d0 +
                    (self.C_L ** 2) /
                    (self.e_f * math.pi *
                     self.ar))
        # ====================================
        # Therefore, lift_drag
        # is calculated as follow:
        # lift_drag: Lift-Drag ratio
        # (L/D = C_L/C_D = L by D)
        self.lift_drag = self.C_L / self.C_D

        # L_p:
        # lapse rate
        # lapse rate is the trust ratio
        # between height and surface of
        # the sea
        self.lp = 1.0

        # -- 4. cruise parameters --
        # lp_cr:
        # lapse rate on cruise
        # Height 35000 [ft], M = 0.8;
        # approximately lp = 0.25
        self.lp_cr = 0.25

        # e:
        # Oswald's efficiency factor
        # (max: e = 1) in clean form;
        # approximately e = 0.8-0.85
        self.e_clean = 0.8

        # w_r:
        # weight ratio between
        # cruise and take-off
        # w_r = (W_cr / W_TO) = 0.965
        self.w_r = 0.956

    # 1. Take-off
    def take_off(self, x, y1, y2, y3,
                 m, sigma1,
                 c1, s_tofl):
        for i in range(self.m):
            k = []
            for j in range(3):
                temp1 = (self.sigma1 *
                         self.c1[j] *
                         self.s_tofl)

                temp2 = (40.3 *
                         self.x[i] /
                         temp1)

                k.append(temp2)

            self.y1.append(k[0])
            self.y2.append(k[1])
            self.y3.append(k[2])

    # 2. Land
    def land(self, x, x1, x2, x3, x4,
             m, sigma2, c2, s_fl):
        # m times repeat
        count = 0
        while count < self.m:
            count += 1

            k = []
            for j in range(4):
                '''
                Unit transformation:
                1 [kg] = 2.2046 [lb]
                1 [m] = 3.281 [ft]
                1 [knot] = 1.688 [ft/s]

                density on the sea level
                is 0.125 [kg*s^2/m^4]

                * "density" is a local
                  variable, so this name
                  is used phase 4.
                  In cruise, it's diffrent
                  on the (cruise) height.
                '''
                # density [lb*s^2/ft^4]
                density = (self.sigma2 *
                           0.125 * 2.2046 /
                           (3.281 ** 4))

                # temp1 = (W/S)_lift
                temp1 = (density *
                         ((self.V_SL *
                           1.688) ** 2) *
                         self.c2[j] / 2)
                # where
                #       W_lift
                #       = 0.85 W_take-off,
                # so
                #       (W/S)_TO
                #       = (W/S)_lift / 0.85
                temp2 = temp1 / 0.85
                k.append(temp2)

            self.x1.append(k[0])
            self.x2.append(k[1])
            self.x3.append(k[2])
            self.x4.append(k[3])

        # output stall speed V_SL
        print("Land: V_SL =",
              self.V_SL, "[knot]")

    # 3. Climb
    def climb(self, y4, m, lp, lift_drag):
        '''
        Far25.121:
        gamma = lp (T/W)_TO / 2
                - 1/(L/D)
              >= 0.024
        '''
        count = 0
        while count >= self.m:
            count += 1

            k = (2 * self.lp *
                 (1 / self.lift_drag +
                  self.gamma))
            # consider of the 27.8
            # celsius temperature,
            # 20% decrease
            k = k / 0.8
            self.y4.append(k)

    # 4. Cruise
    def cruise(self, x_cr, y5, m,
               lp_cr, e_clean,
               v_cruise, c_d0,
               w_r, ar):
        '''
        y = f(x):
             y = 1/lp_cr *
                 (W_cr/W_TO) * (T/W)_cruise
            (T/W)_cruise = (C_D0 + ΔC_D0) *
                           q / (W_cr/W_TO) +
                           (W_cr/W_TO) *
                           x / qeπAR
        In this program,
                        k = y
            temp1 + temp3  = (T/W)_cruise
        '''
        for i in range(self.m - self.fit):
            # density
            # 0.002378 [lb*s^2/ft^4]
            density = (0.31 * 0.125 *
                       2.2046 / (3.281 ** 4))

            # q:
            # kinematic pressure
            # deinition q := ρV^2 / 2
            q = (0.5 * density *
                 (self.v_cruise ** 2))

            temp1 = ((self.c_d0 - 0.015 +
                      0.003) * q /
                     (self.w_r *
                      self.x_cr[i]))

            # temp2: q * eπAR
            temp2 = (q * self.e_clean *
                     math.pi * self.ar)

            temp3 = (self.w_r *
                     self.x_cr[i] /
                     temp2)

            # y_cruise = (T/W)_cruise
            y_cruise = temp1 + temp3

            # k = (T/W)_TO
            k = (self.w_r * y_cruise /
                 self.lp_cr)

            self.y5.append(k)

    # Output
    def output(self, x, y1, y2, y3,
               m, c, x1, x2, x3,
               x4, y4, x_cr, y5):
        # set labels
        plt.xlabel("(W/S) take-off")
        plt.ylabel("(T/W) take-off")
        plt.title("Sizing-Plot",
                  c="darkred",
                  size="large",
                  style="italic")

        # plot 1. take-off
        plt.plot(x, self.y1, label=f"C_LmaxTO = {self.c[0]}")
        plt.plot(x, self.y2, label=f"C_LmaxTO = {self.c[1]}")
        plt.plot(x, self.y3, label=f"C_LmaxTO = {self.c[2]}")

        # define the plot area
        # from 0 to 0.8 for plot 2.
        y = []
        for i in range(self.m):
            i = float(i) * 4 / 1000
            y.append(i)

        # plot 2. land
        plt.plot(self.x1, y, label=f"C_LmaxL = {self.c[3]}")
        plt.plot(self.x2, y, label=f"C_LmaxL = {self.c[4]}")
        plt.plot(self.x3, y, label=f"C_LmaxL = {self.c[5]}")
        plt.plot(self.x4, y, label=f"C_LmaxL = {self.c[6]}")

        # plot 3. climb
        plt.plot(x, self.y4, label="FAR 25.121")

        # plot 4. cruise
        plt.plot(self.x_cr, self.y5, label="Cruise")

        plt.legend(loc="upper left",
                   frameon=True)
        plt.show()

    # GUI Design:

    def gui(self, m_cruise, s_tofl, s_fl):
        """
        -- Design Requirements --
        *Default

        m_cruise: Mach number on cruise
                  definition  M := V/a
        self.m_cruise = 0.80

        s_tofl: take-off field length
        self.s_tofl = 6000.0  # [ft]

        s_fl: Far landing field length
        self.s_fl = 5000.0   # [ft]
        """
        sg.theme("BlueMono")
        OK = 'ok'
        layout = [[sg.Text("1st Sizing - Design Requirement -")],
                  [sg.Text("Select parameters")],
                  # Cruise
                  [sg.Text("Mach number", size=(15, 1)),
                   sg.Combo(("0.7", "0.75", "0.8"), size=(10, 1), key="mach",
                            text_color=None, default_value="0.8")],
                  #  Take off
                  [sg.Text("Takeoff field length[ft]", size=(15, 1)),
                   sg.Combo(("5000", "6000"), size=(10, 1), key="tofl",
                            text_color=None, default_value="5000")],
                  # Land
                  [sg.Text("FAR field length[ft]", size=(15, 1)),
                   sg.Combo(("6000", "6500"), size=(10, 1), key="fl",
                            text_color=None, default_value="6000")],
                  # OK or cancel
                  [sg.Button("OK", key=OK), sg.Cancel()]
                  ]

        window = sg.Window("Sizing plot", layout=layout)

        event, values = window.read()

        if event == OK:
            # cruise
            if values["mach"] == "0.7":
                self.m_cruise = 0.70
            elif values["mach"] == "0.75":
                self.m_cruise = 0.75
            else:
                self.m_cruise = 0.80

            # take-off
            if values["tofl"] == "5000":
                self.s_tofl = 5000.0
            elif values["tofl"] == "6000":
                self.s_tofl = 6000.0

            # land
            if values["fl"] == "6000":
                self.s_fl = 6000.0
            elif values["fl"] == "6500":
                self.s_fl = 6500.0

        window.close()
        # End of GUI Design


if __name__ == "__main__":
    # time
    start = time.time()

    # class
    sp = SizingPlot()

    # GUI
    sp.gui(sp.m_cruise, sp.s_tofl,
           sp.s_fl)
    print("m_cruise = ",
          sp.m_cruise)
    print(sp.s_tofl, sp.s_fl)

    # set parameters
    sp.set_param()

    # 1. Take-off
    sp.take_off(sp.x, sp.y1, sp.y2,
                sp.y3, sp.m, sp.sigma1,
                sp.c1, sp.s_tofl)
    # 2. Land
    sp.land(sp.x, sp.x1, sp.x2,
            sp.x3, sp.x4, sp.m,
            sp.sigma2, sp.c2, sp.s_fl)
    # 3. Climb
    sp.climb(sp.y4, sp.m, sp.lp,
             sp.lift_drag)

    # 4. Cruise
    sp.cruise(sp.x_cr, sp.y5, sp.m,
              sp.lp_cr, sp.e_clean,
              sp.v_cruise, sp.c_d0,
              sp.w_r, sp.ar)

    # Output
    sp.output(sp.x,
              sp.y1, sp.y2, sp.y3,
              sp.m, sp.c,
              sp.x1, sp.x2, sp.x3,
              sp.x4, sp.y4,
              sp.x_cr, sp.y5)

    end = time.time()
    time = end - start
    print("time =", time, "[sec]")

# End of sizing-plot.py
