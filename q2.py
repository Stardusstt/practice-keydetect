import pathlib

from libkeydetect import report
from libkeydetect import plot


def swd_dataset( path , child_name , type_name ):
    
    #
    # path / child_name

    # concatenate path with child folder
    path = pathlib.Path( path )


    if type_name == 'score_midi' :
        child_path = path / child_name
    else:
        child_path = path / child_name / 'audio_wav' 

     
    #
    return child_path


if __name__ == '__main__':

    root_path = R"D:\Temporary\ttttttt\HW1\HW1 Datasets\SWD\SWD"

    score_midi_csv = R"D:\Temporary\ttttttt\HW1\HW1 Datasets\SWD\SWD\02_Annotations\ann_globalkey\score_midi.csv"
    FI66_csv = R"D:\Temporary\ttttttt\HW1\HW1 Datasets\SWD\SWD\02_Annotations\ann_globalkey\FI66.csv"
    FI80_csv = R"D:\Temporary\ttttttt\HW1\HW1 Datasets\SWD\SWD\02_Annotations\ann_globalkey\FI80.csv"
    HU33_csv = R"D:\Temporary\ttttttt\HW1\HW1 Datasets\SWD\SWD\02_Annotations\ann_globalkey\HU33.csv"
    SC06_csv = R"D:\Temporary\ttttttt\HW1\HW1 Datasets\SWD\SWD\02_Annotations\ann_globalkey\SC06.csv"


    report_cls = report.Report()
    plot_cls = plot.Plot()


    # ['FI66', 'FI80', 'HU33', 'SC06', 'score_midi']

    # score_midi
    print( "score_midi" )
    result_score_midi = report_cls.type( root_path , 'score_midi' , child_rule=swd_dataset , csv_file=score_midi_csv , midi=True )
    print( result_score_midi )

    plot_cls.type( result_score_midi , 'score_midi' , midi=True )

    # HU33
    print( "HU33" )
    result_score_HU33 =  report_cls.type( root_path , 'HU33' , child_rule=swd_dataset , csv_file=HU33_csv , midi=False ) 
    print( result_score_HU33 )

    plot_cls.type( result_score_HU33 , 'HU33' )

    # SC06
    print( "SC06" )
    result_score_SC06 = report_cls.type( root_path , 'SC06' , child_rule=swd_dataset , csv_file=SC06_csv , midi=False ) 
    print( result_score_SC06 )

    plot_cls.type( result_score_SC06 , 'SC06' )

    # FI66
    print( "FI66" )
    result_score_FI66 =  report_cls.type( root_path , 'FI66' , child_rule=swd_dataset , csv_file=FI66_csv , midi=False ) 
    print( result_score_FI66 )

    plot_cls.type( result_score_FI66 , 'FI66' )

    # FI80
    print( "FI80" )
    result_score_FI80 = report_cls.type( root_path , 'FI80' , child_rule=swd_dataset , csv_file=FI80_csv , midi=False ) 
    print( result_score_FI80 )

    plot_cls.type( result_score_FI80 , 'FI80' )





