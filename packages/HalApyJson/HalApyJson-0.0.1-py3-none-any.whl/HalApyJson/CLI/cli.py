def cli_hal():

    # Standard library import
    from argparse import ArgumentParser, Namespace
    from datetime import datetime
    from pathlib  import Path  
    
    # Third party imports
    import pandas as pd
    
    # Internal import
    from   HalApyJson.main import build_hal_df_from_api
    
    parser = ArgumentParser()
    parser.usage = '''usage cli_doi doi -k <api-key-pass>
    from a doi get the json article from scopus api
    and buils acsv file in your homedir.
    your api keys must be store in a json file locate at -k <api-key-path
    otherwise the default value is your homedir '''
    #parser.add_argument('doi',help='doi to parse', type=str)
    parser.add_argument('-y',
                        '--year',
                        help='year of the publication',
                        type=str)
    parser.add_argument('-i', '--institute',
                        nargs='?', 
                        help='institute of interest')
    parser.add_argument('-o', '--output',
                        nargs='?', 
                        help='output path for the results')
    args : Namespace = parser.parse_args()

    if args.output is None:
        output_path = Path.home()
        print(f'Default api_key_path is set to : {output_path}')
    else:
        output_path = args.keyfile
        print(f'Option and command-line argument given: "-o {output_path}"')
    
    if args.year is None:
        year = str(datetime.now().year)
        print(f'Default year : {year}')
    else:
        year = args.year
        print(f'Option and command-line year: "-y {year}"')
    
    if args.institute is None:
        institute = "cea"
        print(f'Default institute: {institute}')
    else:
        institute = args.institute
        print(f'Option and command-line institute: "-i {institute}"')
            
        
    hal_df = build_hal_df_from_api(year,institute)
    hal_df.to_excel(Path(output_path)/Path(f'HAL_{institute}_{year}_results.xlsx'), index = False)
    

    
