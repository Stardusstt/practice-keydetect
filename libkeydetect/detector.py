import librosa
import pretty_midi
import numpy
import mir_eval



class Chromagram:

    def __init__( self , file_path , midi=False ):

        self.midi_arg = midi
        
        if midi == False :
            
            self.audio_time_series , self.sampling_rate = librosa.load( file_path )

        if midi == True :
            
            # pretty_midi doesn't support pathlib.Path
            self.midi_data = pretty_midi.PrettyMIDI( str( file_path ) )
            

    def stft( self ):
        '''Compute stft chromagram'''

        if self.midi_arg == True :
            raise TypeError("You can only use Chromagram.midi for midi file.")
        
        #  The default value, n_fft=2048
        chromagram_stft = librosa.feature.chroma_stft( y=self.audio_time_series , sr=self.sampling_rate )

        return chromagram_stft

    def cqt( self ):
        '''Compute cqt chromagram'''

        if self.midi_arg == True :
            raise TypeError("You can only use Chromagram.midi for midi file.")
        
        chromagram_cqt = librosa.feature.chroma_cqt( y=self.audio_time_series , sr=self.sampling_rate )

        return chromagram_cqt

    def cens( self ):
        '''Compute cens chromagram'''

        if self.midi_arg == True :
            raise TypeError("You can only use Chromagram.midi for midi file.")
        
        chromagram_cens = librosa.feature.chroma_cens( y=self.audio_time_series , sr=self.sampling_rate )

        return chromagram_cens

    def midi( self ):
        '''Compute chromagram for midi file'''

        if self.midi_arg == False :
            raise TypeError("Only midi file can use Chromagram.midi.")
        
        # get single instrument chroma
        for instrument in self.midi_data.instruments :

            if instrument.name == 'Piano' :
                
                chromagram_midi = instrument.get_chroma()


        #
        return chromagram_midi


class Detector:

    def __init__( self , chromagram ):

        # all mean , axis = time
        self.chroma_array = chromagram.mean( axis=1 )


        # pitch_class
        self.pitch_class_list = [ 'C','C#','D','D#','E','F','F#','G','G#','A','A#','B' ]

        # binary C template
        self.binary_C_major_template = numpy.array( [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1] )
        self.binary_C_minor_template = numpy.array( [1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0] )


    def __corrcoef( self , template_list ):
        """
        Compute correlation coefficient.

        :rtype: list
        """
        
        corrcoef_list = []

        for template in template_list :
            
            temp_corrcoef = numpy.corrcoef( self.chroma_array , template )
            
            corrcoef_list.append( temp_corrcoef[0,1] )


        #
        return corrcoef_list
    
    def __max( self , corrcoef_major_list , corrcoef_minor_list ):
        """
        Find maximum correlation coefficient.

        :rtype: str
        """
        
        # find maximum value in list
        major_maximum = max( corrcoef_major_list )
        minor_maximum = max( corrcoef_minor_list )

        # get maximum value index
        temp_major_index = corrcoef_major_list.index( major_maximum )
        temp_minor_index = corrcoef_minor_list.index( minor_maximum )

        #
        if major_maximum > minor_maximum :

            maximum_key = self.pitch_class_list[temp_major_index] + " major"

        elif major_maximum < minor_maximum :

            maximum_key = self.pitch_class_list[temp_minor_index] + " minor"

        else:
            
            # use tonic to find 
            
            # find maximum value in major , minor 
            temp_major_value = self.chroma_array[temp_major_index]
            temp_minor_value = self.chroma_array[temp_minor_index]
            
            #
            if temp_major_value > temp_minor_value :
                
                temp_index = list(self.chroma_array).index( temp_major_value )

                maximum_key = self.pitch_class_list[temp_index] + " major"

            elif temp_major_value < temp_minor_value :
                
                temp_index = list(self.chroma_array).index( temp_minor_value )

                maximum_key = self.pitch_class_list[temp_index] + " minor"

            else:
                maximum_key = "key can't find"


        #
        return maximum_key

    def __get_harmonic_c_note( self , alpha: int ):
        """
        Get harmonic c note list.

        :rtype: list
        """

        # C_note array with 12 elements
        C_note_list = [None] * 12

        # 0
        C_note_list[0] = 1 + alpha + pow( alpha , 3 ) + pow( alpha , 7 )
        
        # 1
        C_note_list[1] = 0
        
        # 2
        C_note_list[2] = 0
        
        # 3
        C_note_list[3] = 0
        
        # 4
        C_note_list[4] = pow( alpha , 4 )
        
        # 5
        C_note_list[5] = 0
        
        # 6
        C_note_list[6] = 0
        
        # 7
        C_note_list[7] = pow( alpha , 2 ) + pow( alpha , 5 )
        
        # 8
        C_note_list[8] = 0

        # 9
        C_note_list[9] = 0

        # 10
        C_note_list[10] = pow( alpha , 6 )
        
        # 11
        C_note_list[11] = 0
        
        
        #
        return C_note_list

    def __get_k_s_template_list( self , K_S_template ):
        """
        Get k_s template list.

        :rtype: list
        """
        
        k_s_template_list = []

        # rotated with pitch_class
        for index , pitch in enumerate( self.pitch_class_list ) :
            
            template_rotated = numpy.roll( K_S_template , index )
            
            k_s_template_list.append( template_rotated )


        #
        return k_s_template_list

    def __get_harmonic_template_list( self , c_note_list , binary_C_template ):
        """
        Get harmonic template list.

        :rtype: list
        """
        
        harmonic_template_list = []

        # rotated with pitch_class
        for index , pitch in enumerate( self.pitch_class_list ):

            # get rotated
            binary_template_rotated = numpy.roll( binary_C_template , index )

            # Calculate key array
            key_array = numpy.zeros( 12 )

            for index , value in enumerate( binary_template_rotated ) :

                if value == 1 :

                    # Calculate note array
                    harmonic_note_rotated = numpy.roll( c_note_list , index )
                    
                    # add to key array
                    key_array += harmonic_note_rotated

            #
            harmonic_template_list.append( key_array )
            

        #
        return harmonic_template_list
    
    def binary( self ):
        """
        Compute estimated_key with binary method.

        :rtype: str
        """

        #     
        # estimate tonic
        
        # maximum value index
        chroma_array_maximum_index = self.chroma_array.argmax()

        tonic_estimate = self.pitch_class_list[chroma_array_maximum_index]

        #
        # get rotated template
        binary_template_major_rotated = numpy.roll( self.binary_C_major_template , chroma_array_maximum_index )
        binary_template_minor_rotated = numpy.roll( self.binary_C_minor_template , chroma_array_maximum_index )


        #
        # correlation coefficient  
        corrcoef_major = numpy.corrcoef( self.chroma_array , binary_template_major_rotated )
        corrcoef_minor = numpy.corrcoef( self.chroma_array , binary_template_minor_rotated )


        #
        # estimate key
        if corrcoef_major[0,1] > corrcoef_minor[0,1] :
            
            estimated_key = tonic_estimate + " major"
        
        elif corrcoef_major[0,1] < corrcoef_minor[0,1] :

            estimated_key = tonic_estimate + " minor"

        else:
            
            estimated_key = "equal"


        #
        return estimated_key

    def k_s( self ):
        """
        Compute estimated_key with k_s method.

        :rtype: str
        """
        
        # K_S C template
        K_S_C_major_template = numpy.array( [6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88] )
        K_S_C_minor_template = numpy.array( [6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17] )


        # get k_s template list
        k_s_major_template_list = self.__get_k_s_template_list( K_S_C_major_template )
        k_s_minor_template_list = self.__get_k_s_template_list( K_S_C_minor_template )

        # correlation coefficient
        corrcoef_major_list = self.__corrcoef( k_s_major_template_list )
        corrcoef_minor_list = self.__corrcoef( k_s_minor_template_list )

        # estimate key
        estimated_key = self.__max( corrcoef_major_list , corrcoef_minor_list )

        #
        return estimated_key

    def harmonic( self ):
        """
        Compute estimated_key with harmonic method.

        :rtype: str
        """
        
        # get c_note_list with alpha = 0.9
        c_note_list = self.__get_harmonic_c_note( 0.9 )
        

        # get harmonic template list
        harmonic_major_template_list = self.__get_harmonic_template_list( c_note_list , self.binary_C_major_template )
        harmonic_minor_template_list = self.__get_harmonic_template_list( c_note_list , self.binary_C_minor_template )
        
        # correlation coefficient
        corrcoef_major_list = self.__corrcoef( harmonic_major_template_list )
        corrcoef_minor_list = self.__corrcoef( harmonic_minor_template_list )

        # estimate key
        estimated_key = self.__max( corrcoef_major_list , corrcoef_minor_list )

        #
        return estimated_key


class Score:
    
    def __init__( self , estimated_key , reference_key ):
         
        if estimated_key == "equal" :

            raise RuntimeError("estimated_key is equal")

        # init
        self.estimated_key = estimated_key
        self.reference_key = reference_key

    def raw( self ) -> int:
        """
        Compute raw score.

        :rtype: int
        """
        
        if self.estimated_key == self.reference_key :

            score = 1

        else:

            score = 0

        return score

    def weighted( self ) -> float:
        """
        Compute weighted score.

        :rtype: float
        """
        
        score = mir_eval.key.weighted_score( self.reference_key , self.estimated_key )

        return score





















