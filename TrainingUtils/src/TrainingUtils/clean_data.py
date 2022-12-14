import pandas as pd
import numpy
import matplotlib.pyplot as plt
import math
import os
from argparse import ArgumentParser


class PlaneCalculations:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def Normal_Plane(self):
        return [self.p1[0] * -self.p2[0], self.p1[1] * -self.p2[1], self.p1[2] * -self.p2[2]]

    def Reverse_Normal_Plane(self):
        return [self.p2[0] * -self.p1[0], self.p2[1] * -self.p1[1], self.p2[2] * -self.p1[2]]

    def Unit_Vector(self):
        sub = numpy.subtract(self.p1, self.p2)
        return sub / numpy.linalg.norm(sub)

    def Calc_W(self):
        u = self.Normal_Plane()
        v = numpy.cross(u, self.Unit_Vector())
        return numpy.cross(u, v)

    def Calc_Theta(self):
        w = self.Calc_W()
        n2 = self.Reverse_Normal_Plane()
        u = self.Normal_Plane()
        # print("W: ", w, "n2: ", n2, "U: ", u)
        return math.atan(numpy.dot(w, n2) / numpy.dot(u, n2))


class Cleaner:
    def __init__(self, inputDir, outputDir, csvOutput):
        self.inputDir = inputDir
        self.outputDir = outputDir
        self.csvOutput = csvOutput

    def DataCleaner(self):
        for filename in os.listdir(self.inputDir):
            f = os.path.join(self.inputDir, filename)
            print(f)
            if (os.path.isfile(f) and ".csv" in f):
                mound_name = filename.replace(".csv", "")
                df = pd.read_csv(f)

                minX = min(df['x'])
                minY = min(df['y'])
                minZ = min(df['z'])
                df['x'] = df['x'] - minX
                df['y'] = df['y'] - minY
                df['Z'] = df['z'] - minZ

                centroidX = df['x'].sum() / len(df.index)
                centroidY = df['y'].sum() / len(df.index)
                centroidZ = df['z'].sum() / len(df.index)
                starting_point = (centroidX, centroidY, centroidZ)

                maxim = 0
                for index, row in df.iterrows():
                    radius = math.sqrt(((starting_point[0] - row['x']) ** 2) + ((starting_point[1] - row['y']) ** 2) + (
                            (starting_point[2] - row['z']) ** 2))
                    if (radius > maxim):
                        maxim = radius

                bins = []
                alphas = []
                phis = []
                thetas = []

                for index, row in df.iterrows():
                    plane1 = PlaneCalculations(starting_point, (row['x'], row['y'], row['z']))
                    plane2 = PlaneCalculations((row['x'], row['y'], row['z']), starting_point)

                    alphas.append(
                        numpy.dot(plane1.Normal_Plane(), plane2.Normal_Plane())
                    )
                    phis.append(
                        numpy.dot(plane1.Normal_Plane(), plane2.Unit_Vector())
                    )
                    thetas.append(
                        plane1.Calc_Theta()
                    )

                alpha_range = numpy.ptp(alphas)
                phi_range = numpy.ptp(phis)
                theta_range = numpy.ptp(thetas)

                alpha_min = min(alphas)
                phi_min = min(phis)
                theta_min = min(thetas)
                alphas_normal = []
                phis_normal = []
                thetas_normal = []

                for x in range(len(alphas)):
                    alpha_normal = (alphas[x] - alpha_min) / alpha_range
                    phi_normal = (phis[x] - phi_min) / phi_range
                    theta_normal = (thetas[x] - theta_min) / theta_range
                    bins.append([alpha_normal, phi_normal, theta_normal])
                    alphas_normal.append(alpha_normal)
                    phis_normal.append(phi_normal)
                    thetas_normal.append(theta_normal)

                n_bins = len(bins)
                print(self.outputDir + mound_name)
                plt.hist(alphas_normal, n_bins, density=True, histtype='bar')
                plt.savefig(self.outputDir + mound_name + '-alpha')
                plt.close()

                plt.hist(thetas_normal, n_bins, density=True, histtype='bar')
                plt.savefig(self.outputDir + mound_name + '-theta')
                plt.close()

                plt.hist(phis_normal, n_bins, density=True, histtype='bar')
                plt.savefig(self.outputDir + mound_name + '-phi')
                plt.close()

                new_df = pd.DataFrame()
                new_df['alphas'] = alphas_normal
                new_df['theta'] = thetas_normal
                new_df['phi'] = phis_normal
                new_df.to_csv(self.csvOutput + mound_name + '.csv')

def main():
    parser = ArgumentParser()
    parser.add_argument('-id', '--input_dir',
                        dest='input_dir',
                        help='Input directory for CSV files',
                        required=True)
    parser.add_argument('-od', '--output_dir',
                        dest='output_dir',
                        help='Output directory for pngs of histograms',
                        required=True)
    parser.add_argument('-ocsv', '--csv_output',
                        dest='csv_output',
                        help='Output directory for new csv files of histograms',
                        required=True)

    args = parser.parse_args()
    input_dir = args.input_dir
    output_dir = args.output_dir
    csv_output = args.csv_output

    cleaner = Cleaner(input_dir, output_dir, csv_output)
    cleaner.DataCleaner()

if __name__ == "__main__":
    main()