__all__ = ['parse_json',]

def parse_json(response):

    '''The `parse_json` function parses the response to the query using the HAL API.
    The parsing is based on the fields set in the global 'GLOBAL' (see 'GLOBALS' module).
            
    Args:
        response (requests.models.Response): The response to be parsed.
    
    Returns
        (pandas.core.frame.DataFrame): The dataframe resulting from the parsed response.
        
    '''
    
    # 3rd party import
    import pandas as pd
    
    # Internal import
    from HalApyJson.GLOBALS import GLOBAL
    
    response_dict = response.json() 
    parsed_response = response_dict['response']
    items_nbr = parsed_response['numFound']
    print('Number of items: ',items_nbr)
    
    fields_keys_select = GLOBAL['HAL_FIELDS'] #FIELDS_KEYS_SELECT
    results_df = pd.DataFrame(columns = fields_keys_select.keys())
    for txt in parsed_response['docs']:
        num_df = pd.DataFrame(columns = fields_keys_select.keys())
        num_results_dict = {}
        for k,v in fields_keys_select.items(): 
            field_value = txt.get(v,'NA')
            if isinstance(field_value,list) : field_value= ','.join(field_value)
            num_results_dict[k] = [field_value] 
        num_df = pd.DataFrame.from_dict(num_results_dict, orient = 'columns')
        results_df = pd.concat([results_df, num_df], ignore_index = True)
    results_df.rename(columns = GLOBAL['HAL_FINAL_COLS'], inplace = True)
    return results_df