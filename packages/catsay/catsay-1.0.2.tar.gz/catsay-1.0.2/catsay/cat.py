import sys


def catsay(input_string:str):
    """make a cat say anything you pass"""
    
    length = len(input_string)+2
    
    cat_message = f'''
           {"-"*length}       
          ( {input_string} )
           {"-"*length}   
          |/     
    /\_/\\
   ( o.o )
    > ^ <  ,"",
    ( " ) :
     (|)""
      '''

    print(cat_message)


if __name__=='__main__':
    catsay(sys.argv[1])