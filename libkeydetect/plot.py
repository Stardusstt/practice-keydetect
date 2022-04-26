
import matplotlib
import matplotlib.pyplot as pyplot
import numpy




#

class Plot:
    
    def __init__( self ):
        pass

    def __chromagram_method( self , result_dict , type_name , chromagram_method ):
        
        # Create a figure containing a single axes
        fig, ax = pyplot.subplots( )


        # create list which need to output
        write_list_chromagram = [ 'stft','cqt','cens' ]
        write_list_method = [ 'binary','k_s','harmonic' ]
        write_list_score = [ 'raw','weighted' ]


        if chromagram_method == "midi" :

            temp_name_list = list()
            temp_value_list = list()
            
            for method in write_list_method:

                for score in write_list_score :

                    temp_name_list.append( method + "\n" + score )
                    temp_value_list.append( result_dict[method][score] )
                    
            # plot    
            ax.plot( temp_name_list , temp_value_list , label=chromagram_method )
            ax.set_ylabel( 'accuracy' )  
            ax.set_title( type_name ) 
            ax.legend()

        else:
            
            for chromagram in write_list_chromagram :
                
                temp_name_list = list()
                temp_value_list = list()
                
                for method in write_list_method:

                    for score in write_list_score :

                        temp_name_list.append( method + "\n" + score )
                        temp_value_list.append( result_dict[chromagram][method][score] )
                        
                # plot
                if chromagram == chromagram_method :
                    
                    ax.plot( temp_name_list , temp_value_list , label=chromagram )
                    ax.set_ylabel( 'accuracy' )  
                    ax.set_title( type_name ) 
                    ax.legend()




        

    
        #
        pyplot.savefig( type_name + "_" + chromagram_method + ".png" , format='png' )
        #pyplot.show()

    def type( self , result_dict , type_name , midi=False ):


        if midi == False :

            # create list which need to output
            write_list_chromagram = [ 'stft','cqt','cens' ]

            for chromagram in write_list_chromagram :
                
                self.__chromagram_method( result_dict , type_name , chromagram_method=chromagram  )

        else:

            self.__chromagram_method( result_dict , type_name , chromagram_method='midi'  )
        
        

        