import pathlib



def child_rule_default( path , child_name , type_name=None ):
    
    #
    # path / child_name

    # concatenate path with child folder
    child_path = path / child_name

    #
    return child_path


class Path:

    def __init__( self , root_path ):

        # init path
        self.root_path = pathlib.Path( root_path )
        

    def get_type( self , child_name , child_rule=child_rule_default ):
        
        # get child path
        child_path = child_rule( self.root_path , child_name )

        # whether the path is existing 
        if child_path.exists() == False :
             
            print( child_path )
            raise OSError("Directory does not exist.")

        # get type
        type_list = list()

        for temp_path in child_path.iterdir() :

            for temp in temp_path.iterdir() :
                
                if temp.is_dir() == True :

                    type_list.append( temp.stem )

                else:

                    type_list.append( temp_path.stem )

                    break

        
        #
        return type_list

    def get_readfile_list( self , child_name , type_name , child_rule=child_rule_default ):

        # get child path
        child_path = child_rule( self.root_path , child_name , type_name )
        
        # whether the path is existing 
        if child_path.exists() == False :
             
            print( child_path )
            raise OSError("Directory does not exist.")

        #
        # get file list
        readfile_list = list()

        # get typepath
        for temp_typepath in child_path.iterdir() :

            # get file list
            if temp_typepath.stem == type_name :
                
                for temp_filepath in temp_typepath.iterdir() :

                    readfile_list.append( temp_filepath )

        #
        return readfile_list       

    

            
    
        