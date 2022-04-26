import numpy
import concurrent.futures
import tqdm
import csv

from . import path
from . import detector



class Report:

    def __init__( self ):
        pass

    def __negative_list( self , file_list ):

        negative_list = list()
        
        for index , file_path in enumerate( file_list ) :
            
            with open( file_path , 'r' ) as file:

                value = file.read()

                # str to int
                value_int = int(value)

                # check if value_int is negative
                if value_int < 0 :

                    negative_list.append( index )
                    
        
        #
        return negative_list

    def __del_negative_file( self , file_list , del_list ):

        # remove index in del_list
        file_list = numpy.delete( file_list, del_list ).tolist()

        #
        return file_list

    def __stft_method( self , chromagram ):
        
        # create template
        stft_method_result = { 'binary': None, 'k_s': None, 'harmonic': None }

        # calculate
        detector_cls = detector.Detector( chromagram.stft() )

        stft_method_result['binary'] = detector_cls.binary()
        stft_method_result['k_s'] = detector_cls.k_s()
        stft_method_result['harmonic'] = detector_cls.harmonic()

        #
        return stft_method_result
        
    def __cqt_method( self , chromagram ):

        # create template
        cqt_method_result = { 'binary': None, 'k_s': None, 'harmonic': None }

        # calculate
        detector_cls = detector.Detector( chromagram.cqt() )

        cqt_method_result['binary'] = detector_cls.binary()
        cqt_method_result['k_s'] = detector_cls.k_s()
        cqt_method_result['harmonic'] = detector_cls.harmonic()

        #
        return cqt_method_result

    def __cens_method( self , chromagram ):
        
        # create template
        cens_method_result = { 'binary': None, 'k_s': None, 'harmonic': None }

        # calculate
        detector_cls = detector.Detector( chromagram.cens() )

        cens_method_result['binary'] = detector_cls.binary()
        cens_method_result['k_s'] = detector_cls.k_s()
        cens_method_result['harmonic'] = detector_cls.harmonic()

        #
        return cens_method_result

    def __midi_method( self , chromagram ):
        
        # create template
        midi_method_result = { 'binary': None, 'k_s': None, 'harmonic': None }

        # calculate
        detector_cls = detector.Detector( chromagram.midi() )

        midi_method_result['binary'] = detector_cls.binary()
        midi_method_result['k_s'] = detector_cls.k_s()
        midi_method_result['harmonic'] = detector_cls.harmonic()

        #
        return midi_method_result

    def __score_dict( self , estimated_key , reference_key ):
        
        # create template
        score_dict = { 'raw': None, 'weighted': None }

        # calculate score
        score = detector.Score(  estimated_key , reference_key )

        score_dict['raw'] = score.raw() 
        score_dict['weighted'] = score.weighted() 

        #
        return score_dict
        
    def __score_all_dict( self , result_dict , reference_key ):
        
        # create template
        score_all_dict = { 'binary': None, 'k_s': None, 'harmonic': None }
        
        # calculate all score
        for method , estimated_key in result_dict.items() :
            
            temp_dict = self.__score_dict( estimated_key , reference_key )
            
            score_all_dict[ method ] = temp_dict
            

        #
        return score_all_dict

    def __dict_to_list( self , dict_ , midi=False ):
        
        temp_list = list()

        # create list which need to output
        write_list_chromagram = [ 'stft','cqt','cens' ]
        write_list_method = [ 'binary','k_s','harmonic' ]
        write_list_score = [ 'raw','weighted' ]

        # convert
        if midi == False :

            for chromagram in write_list_chromagram :

                for method in write_list_method:

                    for score in write_list_score :

                        temp_list.append( dict_[chromagram][method][score] )
                    
        if midi == True :

            for method in write_list_method:

                for score in write_list_score :

                    temp_list.append( dict_[method][score] )

        #
        return temp_list

    def __array_to_dict( self , numpy_array , midi=False ):
        
        temp_dict = dict()

        # create list which need to output
        write_list_chromagram = [ 'stft','cqt','cens' ]
        write_list_method = [ 'binary','k_s','harmonic' ]
        write_list_score = [ 'raw','weighted' ]


        # convert

        # read index from 0 
        index_array = 0

        if midi == False :

            for chromagram in write_list_chromagram :

                # create dict template
                temp_dict[chromagram] = {}
                
                for method in write_list_method:

                    temp_dict[chromagram][method] = {}
                    
                    for score in write_list_score :

                        temp_dict[chromagram][method][score] = numpy_array[ index_array ]

                        # next index
                        index_array += 1
                    
        if midi == True :

            for method in write_list_method:

                    temp_dict[method] = {}
                    
                    for score in write_list_score :

                        temp_dict[method][score] = numpy_array[ index_array ]

                        # next index
                        index_array += 1
                    

        #
        return temp_dict

    def accuracy( self , numpy_array , number ):
        
        return numpy_array / number

    def file( self , estimated_file_path , reference_file_path , ref_is_key=False , midi=False ):
    
        chromagram = detector.Chromagram( estimated_file_path , midi=midi )

        #
        if ref_is_key == False :
            
            # reference_file to key
            utils = Utils()

            reference_key = utils.txt_to_key( reference_file_path )

        if ref_is_key == True :
            
            reference_key = reference_file_path


        #
        if midi == False : 
            
            # multithreading 
            with concurrent.futures.ThreadPoolExecutor() as executor:
                
                # execute task
                future_stft = executor.submit( self.__stft_method , chromagram )
                future_cqt = executor.submit( self.__cqt_method , chromagram )
                future_cens = executor.submit( self.__cens_method , chromagram )

                # get result
                stft_result = future_stft.result()
                cqt_result = future_cqt.result()
                cens_result = future_cens.result()


            # create template
            result_dict = { 'stft': None, 'cqt': None, 'cens': None }
            
            # calculate score
            result_dict['stft'] = self.__score_all_dict( stft_result , reference_key )
            result_dict['cqt'] = self.__score_all_dict( cqt_result , reference_key )
            result_dict['cens'] = self.__score_all_dict( cens_result , reference_key )

        if midi == True :
            
            # get result
            midi_result = self.__midi_method( chromagram )

            # calculate score
            result_dict = self.__score_all_dict( midi_result , reference_key )


        # return score
        return result_dict
    
    def type( self , root_path , type_name , child_rule = path.child_rule_default , csv_file=False , midi=False ):
    
        path_cls = path.Path( root_path )
        
        #
        if csv_file == False :

            ref_is_key = False

            # get file list
            temp_ref = path_cls.get_readfile_list( 'key' , type_name )
            temp_est = path_cls.get_readfile_list( 'wav' , type_name )

            negative_list = self.__negative_list( temp_ref )

            reference_file_list = self.__del_negative_file( temp_ref , negative_list )
            estimated_file_list = self.__del_negative_file( temp_est , negative_list )

        else:
            
            ref_is_key = True

            utils = Utils()

            reference_file_list = utils.csv_to_key( csv_file )
            estimated_file_list = path_cls.get_readfile_list( '01_RawData' , type_name , child_rule=child_rule )


        #
        if midi == False :

            temp_array = numpy.zeros(18)

        if midi == True :

            temp_array = numpy.zeros(6)


        # multiprocessing  
        with concurrent.futures.ProcessPoolExecutor( max_workers=4 ) as executor:
            
            future_list = []

            # execute task
            for estimated_file , reference_file in zip( estimated_file_list , reference_file_list ) :
                
                # file( estimated_file , reference_file )
                future = executor.submit( self.file , estimated_file , reference_file , ref_is_key=ref_is_key , midi=midi )
                
                future_list.append( future )


            # Progress bar 
            with tqdm.tqdm( total=len( estimated_file_list ) ) as pbar:
                
                # get result
                for future in concurrent.futures.as_completed( future_list ) :

                    temp_list = self.__dict_to_list( future.result() , midi=midi )

                    temp_array += temp_list 


                    # update progress bar
                    pbar.update( 1 )


        # get accuracy
        result_array = self.accuracy( temp_array , len( estimated_file_list ) )

        result_dict = self.__array_to_dict( result_array , midi=midi )
        
    
        #
        return result_dict

    def all( self , root_path ):
        
        path_cls = path.Path( root_path )

        all_result = dict()

        # get all type
        type_list = path_cls.get_type( 'wav' )


        # calculate all type
        for type_name in type_list :
            
            print()
            print( type_name )

            type_result = self.type( root_path , type_name )
            
            all_result[ type_name ] = type_result


        #
        return all_result


#
class Utils:
    
    def __init__( self ):
        pass

    def __int_to_symbol( self , value ):
        
        conversion_list = [ 'A major','A# major','B major','C major','C# major','D major','D# major','E major','F major','F# major','G major','G# major',  'A minor','A# minor','B minor','C minor','C# minor','D minor','D# minor','E minor','F minor','F# minor','G minor','G# minor'  ]

        # str to int
        temp_int = int(value)

        # check if reference_key_int is negative
        if temp_int < 0 :
            raise RuntimeError("reference_key_int is negative.")

        # int to symbol
        symbol = conversion_list[ temp_int ] 

        return symbol

    def txt_to_key( self , filepath ):

        with open( filepath , 'r' ) as file:

            key_value = file.read()

        # to symbol
        key = self.__int_to_symbol( key_value )

        #
        return key

    def csv_to_key( self , csv_file ):

        key_list = list()

        with open( csv_file , newline='' ) as file:

            rows = csv.DictReader( file , delimiter=';' )

            for row in rows:
                
                key_list.append( row['key'] )
                

        #
        return key_list

    def reference_key_list( self , filepath_list ):
        
        # ref list

        reference_key_list = list()
        #
        for filepath in filepath_list :

            # read reference_key_file value
            with open( filepath , 'r' ) as file:

                reference_key_value = file.read()

            # to symbol
            reference_key = self.__int_to_symbol( reference_key_value )

            #
            reference_key_list.append( reference_key )

        #
        return reference_key_list






