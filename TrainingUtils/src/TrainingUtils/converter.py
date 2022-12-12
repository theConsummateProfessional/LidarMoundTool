import pylas
import os
import pandas as pd
from argparse import ArgumentParser


class Converter:
    def __init__(self, inputDir, outputDir):
        self.inputDir = inputDir
        self.outputDir = outputDir

    def read_lazs_to_file_verbose(self):
        for filename in os.listdir(self.inputDir):
            if filename.endswith('.laz'):
                print(self.inputDir + filename)
                with pylas.open(self.inputDir + filename) as fh:
                    print(fh)
                    las = fh.read()
                    print(las)
                    print('Points from Header:', fh.header.point_count)
                    print(las.x)
                    print(las.y)
                    print(las.z)
                    new_df = pd.DataFrame()
                    new_df['x'] = las.x
                    new_df['y'] = las.y
                    new_df['z'] = las.z

                    if os.path.exists(self.outputDir):
                        new_df.to_csv(self.outputDir + filename.replace('.laz', '.csv'))
                    else:
                        os.mkdir(self.outputDir)
                        new_df.to_csv(self.outputDir)

    def read_lazs_to_file(self):
        for filename in os.listdir(self.inputDir):
            if filename.endswith('.laz'):
                with pylas.open(self.inputDir + filename) as fh:
                    las = fh.read()
                    new_df = pd.DataFrame()
                    new_df['x'] = las.x
                    new_df['y'] = las.y
                    new_df['z'] = las.z

                    if os.path.exists(self.outputDir):
                        new_df.to_csv(self.outputDir + filename.replace('.laz', '.csv'))
                    else:
                        os.mkdir(self.outputDir)
                        new_df.to_csv(self.outputDir)


def main():
    parser = ArgumentParser()
    parser.add_argument('-id', '--input_dir',
                        dest='input_dir',
                        help='The directory that contains laz files',
                        required=True)
    parser.add_argument('-od', '--output_dir',
                        dest='output_dir',
                        help='The directory that will contain all output csv files',
                        required=True)
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        dest='verbose',
                        help='Verbose mode')

    args = parser.parse_args()
    input_dir = args.input_dir
    output_dir = args.output_dir
    verbose = args.verbose

    file_converter = Converter(input_dir, output_dir)
    if verbose:
        file_converter.read_lazs_to_file_verbose()
    else:
        file_converter.read_lazs_to_file()


if __name__ == "__main__":
    main()
