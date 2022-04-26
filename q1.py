from libkeydetect import report



if __name__ == '__main__':

    root_path = R"D:\Temporary\ttttttt\HW1\HW1 Datasets\GTZAN\GTZAN"

    report_cls = report.Report()

    result = report_cls.all( root_path )
    print( result )