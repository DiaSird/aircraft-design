"""
--- Aircraft Design ---
sizing plot for civil-jet (Far 25)
*FAR = Federal Aviation Regulation
Ref. Kenichi Rinoie, "Aircraft
    Design method - conceptual design
    from single pulloperant to SST - "
"""
import math
import time

import matplotlib.pyplot as plt

class LapseRate:
    def __init__(self):
        # Lapse rate
        self.lp = 0.0
        # Coefficient
        self.k = [0.0, 0.0, 0.0, 0.0]
        # Bypass ratio
        self.bpr = 12.0
        # Maximum time steps (for mach axis)
        self.max_t = 5
        # Density ratio of air
        self.sigma = 1.0

        # Draw the graph
        self.x = []
        self.y = []

    def calc_lp(self):
        """
        Calculate the Lapse rate
        """
        # Set the coefficients
        # 1. bpr <= 1.0
        def set_coeffs_1(mach):
            if mach <= 0.4:
                self.k[0] = 1.0
                self.k[1] = 0.0
                self.k[2] = -0.2
                self.k[3] = 0.07
            elif mach >= 0.4 and mach <= 0.9:
                self.k[0] = -0.856
                self.k[1] = 0.062
                self.k[2] = 0.16
                self.k[3] = -0.23
            elif mach >= 0.9 and mach <= 2.2:
                self.k[0] = 1.0
                self.k[1] = -0.145
                self.k[2] = -0.5
                self.k[3] = -0.05
            else:
                print("Error: Mach number is out of range")
                exit()

        # 2. bpr >= 3.0 and bpr <= 6.0
        def set_coeffs_2(mach):
            if mach <= 0.4:
                self.k[0] = 1.0
                self.k[1] = 0.0
                self.k[2] = -0.6
                self.k[3] = -0.04
            elif mach >= 0.4 and mach <= 0.9:
                self.k[0] = 0.88
                self.k[1] = -0.016
                self.k[2] = -0.3
                self.k[3] = 0.0

        # 3. bpr >= 8.0
        def set_coeffs_3(mach):
            if mach <= 0.4:
                self.k[0] = 1.0
                self.k[1] = 0.0
                self.k[2] = -0.595
                self.k[3] = -0.03

            elif mach >= 0.4 and mach <= 0.9:
                self.k[0] = -0.89
                self.k[1] = -0.014
                self.k[2] = -0.3
                self.k[3] = 0.005

        s = 0.7
        mach = 1.0
        for i in range(self.max_t):
            if i >= 1:
                mach =  0.1 * i
            else:
                mach = 0.0

            if mach > 0.9:
                mach -= 0.9

            if self.bpr <= 1.0:
                set_coeffs_1(mach)
                s = 0.8
            elif self.bpr >= 3.0 and self.bpr <= 6.0:
                set_coeffs_2(mach)
            elif self.bpr >= 8:
                set_coeffs_3(mach)
            else:
                print("Error: Bypass ratio is out of range")
                exit()

            self.lp = (self.k[0] + self.k[1] * self.bpr + (self.k[2] +
                    self.k[3] * self.bpr) * mach) * (self.sigma ** s)

            print(mach)

            self.x.append(mach)
            self.y.append(self.lp)


    # Output the graph
    def output(self):
        # set labels
        plt.xlabel("Mach number")
        plt.ylabel("Lapse rate")
        plt.title("Performance curve of Engine", c="darkred", size="large", style="italic")

        # plot 1. take-off
        plt.plot(self.x, self.y, label="Sea level")
        plt.legend(loc="upper left", frameon=True)
        plt.show()


if __name__ == "__main__":
    lp = LapseRate()
    lp.calc_lp()
    lp.output()
