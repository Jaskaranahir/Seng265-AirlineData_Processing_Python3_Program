#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 8 14:44:33 2023
Based on: https://www.kaggle.com/datasets/arbazmohammad/world-airports-and-airlines-datasets
Sample input: --AIRLINES="airlines.yaml" --AIRPORTS="airports.yaml" --ROUTES="routes.yaml" --QUESTION="q1" --GRAPH_TYPE="bar"
@author: rivera
@author: STUDENT_ID
"""

import yaml
import sys
import pandas as pd
import matplotlib.pyplot as plt


def command_processor() -> list:           #this function is used to process the command line argument and stored the argument as a list.
    '''Processes the comand line and store the arguments into variables and 
        those variables are being stored as a List.
        
            Parameters
            ----------
                input : None, required
                    

            Returns
            -------
                Returns a list of string that will contain your all the arguments.
                    '''
    argument_list: list = sys.argv[1:]    #list of all the arguments
    usable_list: list = []

    airline_data: str = ''
    airport_data: str = ''
    routes_data: str = ''                      #all the variables that will store the specific argument 
    question: str = ''
    graph: str = ''
    count: int = 1

    for arg in argument_list:
        key, val = arg.split("=")                      #separating the argument using '=' sign as a separator.
        if count == 1:
            airline_data = val
            usable_list.append(airline_data)          #appending the val from a key-val pair into a usable list that we need to work with.
        elif count == 2:
            airport_data = val
            usable_list.append(airport_data)
        elif count == 3:
            routes_data = val
            usable_list.append(routes_data)
        elif count == 4:
            question = val
            usable_list.append(question)
        else:
            graph = val
            usable_list.append(graph)
        count += 1

    return usable_list                               #list containing all the user inputs is returned successfully.


def loading_routes(routes_file: str)-> pd.DataFrame:       #Opening the 'routes.yaml' file and turning it into a dataframe
    '''Processes the routes.yaml file and convert it into dataframe.
            Parameters
            ----------
                input : str, required
                    The name of the routes file.

            Returns
            -------
                pd.DataFrame 
                returning a dataframe.
                    '''
    with open(routes_file, 'r') as f:
        data = yaml.safe_load(f)

        df = pd.DataFrame(data['routes'])
        return df

def loading_airlines(airline_file: str)-> pd.DataFrame:       #Similar, as above opening the 'airline.yaml' file and getting a dataframe
    '''Processes the airlines.yaml file and convert it into dataframe 
            Parameters
            ----------
                input : str, required
                    The airline file name

            Returns
            -------
                Df 
                The dataframe is returned
                    '''
    with open(airline_file, 'r') as f:
        data = yaml.safe_load(f)

        df = pd.DataFrame(data['airlines'])
        return df
    
def loading_airports(airport_file: str)-> pd.DataFrame:         #opening the 'airport.yaml' file and set it as a dataframe
    '''Processes the airport.yaml file and convert it into dataframe.
            Parameters
            ----------
                input : str, required
                    The name of the airport file.

            Returns
            -------
                Dattaframe
                Return an airport datframe.
                    '''
    with open(airport_file, 'r') as f:
        data = yaml.safe_load(f)

        df: pd.DataFrame = pd.DataFrame(data['airports'])
        return df
    
def pie_chart(data: pd.DataFrame, graph_title: str, pdf: str)->None:
   '''Processes the datframe and convert it into pie chart to 
        answer the question provided.
            Parameters
            ----------
                input : pd.DataFrame,str,str, required
                    The datframe to be converted to pie chart, title to be given to graph, and name of pdf.

            Returns
            -------
                None
                    '''
   fig, ax = plt.subplots(figsize=(6.7, 6.7))
   ax.pie(data['statistic'], labels=data['subject'], autopct='%1.1f%%', counterclock=True, textprops={'fontsize': 5}, labeldistance=1, rotatelabels=True)
   ax.axis('equal')
   ax.set_title(graph_title, fontsize=12, y=1.09, x=0.35)

   fig.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
   plt.tight_layout()

   plt.savefig(pdf)
   
   
    

def bar_chart(data: pd.DataFrame, graph_title: str, pdf: str, x_title: str, y_title: str)->None:
     '''Processes the dataframe and convert it into bar graph to 
        answer the question provided.
            Parameters
            ----------
                input : pd.dataframe, str, str, str, str, required
                    The datframe to be used, title of graph, pdf name, title of x and y axis respectively.

            Returns
            -------
                None
                    '''
     
     plt.bar(data['subject'], data['statistic'])
     plt.xlabel(x_title)
     plt.ylabel(y_title)

     plt.xticks(rotation=60, ha='right', va='top')
     plt.gcf().subplots_adjust(bottom=0.4)
             
     plt.xticks(fontsize=4.3)
     plt.yticks(fontsize=4.3)
     plt.title(graph_title)
     plt.savefig(pdf, ) 


def q1_handler(input_list: list) -> None:                          # This function will handle the 'q1' accepting a input list as argument.
    '''Processes the Arguements and using dataframes convert it into dataframe to 
        answer the question provided.
            Parameters
            ----------
                input : List[str], required
                    The input list containing the arguments user provided.

            Returns
            -------
                None
                    '''

    airlines_df: pd.DataFrame = loading_airlines(input_list[0])         #getting the specific dataframes to be work with calling the functions above
    airports_df: pd.DataFrame = loading_airports(input_list[1])
    routes_df: pd.DataFrame = loading_routes(input_list[2])
    
    df1: pd.DataFrame = airports_df.loc[:,["airport_id","airport_country"]]              # df1 will create the dataframe for required aspects from airports dataframe

    df1 = df1.loc[df1["airport_country"]=="Canada"]                         
    df2: pd.DataFrame = routes_df.loc[:,["route_airline_id","route_to_airport_id"]]                     # df2 is storing the required columns from routes df
    df3: pd.DataFrame = airlines_df.loc[:,["airline_id","airline_name","airline_icao_unique_code"]]     # df3 is smaller df of airline df
    merged_df1_df2: pd.DataFrame= pd.merge(df1, df2, left_on='airport_id', right_on='route_to_airport_id')    #merging the df1 and df2 on basis of airport id's

    df4: pd.DataFrame = merged_df1_df2.loc[:,["route_airline_id"]]                                          #df4 will create a df for just airline id column from merged df above

    final_df: pd.DataFrame = pd.merge(df4, df3, left_on='route_airline_id', right_on='airline_id')          # Final dataframe that we required to answer the q1

    csv_df: pd.DataFrame = final_df.groupby(['airline_name', 'airline_icao_unique_code'],as_index=False).size().sort_values(['size', 'airline_name'], ascending=[False,True]).head(20)
    csv_df['subject'] = csv_df['airline_name'] + ' (' + csv_df['airline_icao_unique_code'] + ')' 
    csv_df = csv_df[['subject', 'size']]                                                            # Csv_df dataframe will contain the column in subject, statistic format                   
    csv_df = csv_df.rename(columns={'size': 'statistic'})                                           

    csv_df.to_csv('q1.csv', index=False)                                                            # Writing the csv dataframe to 'q1.csv' file.

    pdf_name: str = "q1.pdf"

    if(input_list[4]=="pie"):                                                                       
        label: str = "Top 20 Airlines with greatest routes" 
        pie_chart(csv_df,label,pdf_name)                                          # Creating a pie chart for the csv dataframe
    else:
        x_label: str = "Airlines"
        y_label: str = "Number of Routes to Canada"
        graph_label: str = "Top 20 Airlines with greatest routes"
        bar_chart(csv_df, graph_label, pdf_name, x_label, y_label)                # creating a bar chart for the csv dataframe
      


def q2_handler(input_list: list) -> None:                                 # Handling the 'q2' and its accepting 
    '''Processes the Arguements from the input list containing arguments and process it into 
        a dataframe to answer the question 2.
        
            Parameters
            ----------
                input : 
                    List[str], required
                    The input list containing the arguments user provided.

            Returns
            -------
                None
                    '''

    airlines_df: pd.DataFrame = loading_airlines(input_list[0])
    airports_df: pd.DataFrame = loading_airports(input_list[1])
    routes_df: pd.DataFrame = loading_routes(input_list[2])

    df1: pd.DataFrame = routes_df.loc[:,["route_to_airport_id"]]                           #df1 is storing routes to airport id column from a routes dataframe
    
    final_df: pd.DataFrame = pd.merge(df1, airports_df, left_on='route_to_airport_id', right_on='airport_id')       #merging df1 with airports dataframe along with id column

    final_df = final_df.loc[:,["airport_country"]]
    final_df = final_df.groupby(['airport_country'],as_index=False).size()                            #airport country to be worked with from a final dataframe
    final_df['airport_country'] = final_df['airport_country'].str.strip()
    final_df = final_df.sort_values(['size', 'airport_country'], ascending=[True,True]).head(30)         
    final_df = final_df.rename(columns={'size': 'statistic','airport_country': 'subject'})

    final_df.to_csv('q2.csv', index=False)                                                          #converting the dataframe to a csv file 'q2.csv

    pdf_name: str = "q2.pdf"

    if(input_list[4]=="pie"):
        label: str = "Top 30 Countries with least appearance as dest.country" 
        pie_chart(final_df,label,pdf_name)                                                             #Calling pie_chart to create a pie chart
    else:
        x_label: str = "Countries"
        y_label: str = "Number of appearances"
        graph_label: str = "Top 30 Countries with least appearance as dest.country"
        bar_chart(final_df, graph_label, pdf_name, x_label, y_label)                                 #calling a bar_chart to create a graph 
      

    

def q3_handler(input_list: list) -> None:
    '''Processes the Arguements and using dataframes convert it into dataframe to 
        answer the question 3 provided.
            Parameters
            ----------
                input : List[str],required
                    The input list containing the arguments user provided.

            Returns
            -------
                None
                    '''
    airlines_df: pd.DataFrame = loading_airlines(input_list[0])
    airports_df: pd.DataFrame = loading_airports(input_list[1])
    routes_df: pd.DataFrame = loading_routes(input_list[2])

    final_df: pd.DataFrame = routes_df.loc[:,["route_to_airport_id"]]                                                  #Final dataframe to work with
    final_df = pd.merge(final_df, airports_df, left_on='route_to_airport_id', right_on='airport_id')
    final_df = final_df.groupby(['airport_name', 'airport_icao_unique_code', 'airport_city', 'airport_country'],as_index=False).size().sort_values(['size', 'airport_name'], ascending=[False,True]).head(10)
    
    final_df['subject'] = '' + final_df['airport_name'] + ' (' + final_df['airport_icao_unique_code'] + '), ' + final_df['airport_city'] + ', ' + final_df['airport_country'] + ''
    final_df = final_df[['subject', 'size']]
    final_df = final_df.rename(columns={'size': 'statistic'}) 
    
    final_df.to_csv('q3.csv', index=False)                                                        #Final dataframe to be stored in a 'q3.csv' file

    pdf_name: str = "q3.pdf"


    if(input_list[4]=="pie"):
        label: str = "Top 10 dest. airports" 
        pie_chart(final_df,label,pdf_name)
    else:
        x_label: str = "Airports"
        y_label: str = "Number of appearance"
        graph_label: str = "Top 10 dest. airports"
        bar_chart(final_df, graph_label, pdf_name, x_label, y_label)

def q4_handler(input_list: list) -> None:                                                     #Calling the q4_handler to handle the q4
    '''Processes the Arguements and using dataframes convert it into dataframe to 
        answer the question 4 provided.
            Parameters
            ----------
                input : List[str]
                    The input list containing the arguments user provided.

            Returns
            -------
                None
                    '''

    airlines_df: pd.DataFrame = loading_airlines(input_list[0])
    airports_df: pd.DataFrame = loading_airports(input_list[1])
    routes_df: pd.DataFrame = loading_routes(input_list[2])

    final_df: pd.DataFrame = routes_df.loc[:,["route_to_airport_id"]]                                         #Creating a final datframe that will extract the usable data from the large datframes provided to us
    final_df = pd.merge(final_df, airports_df, left_on='route_to_airport_id', right_on='airport_id')
    final_df = final_df.groupby(['airport_city', 'airport_country'],as_index=False).size().sort_values(['size','airport_city'], ascending=[False, True]).head(15)
    final_df['subject'] = '' + final_df['airport_city'] + ', ' + final_df['airport_country'] + ''
    final_df = final_df[['subject', 'size']]
    final_df = final_df.rename(columns={'size': 'statistic'})

    final_df.to_csv('q4.csv', index=False)                                                             #Storing the final dataframe to a csv file

    pdf_name: str = "q4.pdf"

    if(input_list[4]=="pie"):
        label: str = "Top 15 dest. Cities" 
        pie_chart(final_df,label,pdf_name)
    else:
        x_label: str = "Cities"
        y_label: str = "Number of appearance"
        graph_label: str = "Top 15 dest. Cities"
        bar_chart(final_df, graph_label, pdf_name, x_label, y_label)

def q5_handler(input_list: list) -> None:
    '''Processes the Arguements and using dataframes convert it into dataframe to 
        answer the question 5 provided.
            Parameters
            ----------
                input : List[str]
                    The input list containing the arguments user provided.

            Returns
            -------
                None
                    '''

    airlines_df: pd.DataFrame = loading_airlines(input_list[0])
    airports_df: pd.DataFrame = loading_airports(input_list[1])
    routes_df: pd.DataFrame = loading_routes(input_list[2])

    df1: pd.DataFrame = routes_df.loc[:,["route_from_aiport_id","route_to_airport_id"]]
    df2: pd.DataFrame = airports_df.loc[:,["airport_id","airport_country","airport_icao_unique_code","airport_altitude"]]
    df2 = df2.loc[df2["airport_country"]=="Canada"]
    
    origin_df: pd.DataFrame = pd.merge(df1, df2, left_on='route_from_aiport_id', right_on='airport_id')
    origin_df = origin_df.loc[:,['route_from_aiport_id','route_to_airport_id','airport_icao_unique_code','airport_altitude']]
    
    final_df: pd.DataFrame = pd.merge(origin_df, airports_df, left_on='route_to_airport_id',right_on='airport_id')
    final_df = final_df.loc[final_df["airport_country"]=="Canada"]
    final_df = final_df.loc[:,["airport_icao_unique_code_x","airport_icao_unique_code_y","airport_altitude_x", "airport_altitude_y"]]
    
    final_df['diff'] = ((final_df['airport_altitude_y'].astype(float)) - (final_df['airport_altitude_x'].astype(float))).abs()
    final_df = final_df.sort_values(['diff'], ascending=[False]).head(10)

    final_df = final_df.loc[:,["airport_icao_unique_code_x","airport_icao_unique_code_y","diff"]]

    final_df['subject'] = final_df['airport_icao_unique_code_x'] + '-' + final_df['airport_icao_unique_code_y']
    final_df = final_df[['subject', 'diff']]
    final_df = final_df.rename(columns={'diff': 'statistic'})

    final_df.to_csv('q5.csv', index=False)

    pdf_name: str = "q5.pdf"

    if(input_list[4]=="pie"):
        label: str = "Top 10 uniques Canadian Routes with most difference b/w altitude" 
        pie_chart(final_df,label,pdf_name)
    else:
        x_label: str = "Routes"
        y_label: str = "Number of appearances"
        graph_label: str = "Top 10 unique Canadian Routes with most difference b/w altitude"
        bar_chart(final_df, graph_label, pdf_name, x_label, y_label)


def main():
    """Main entry point of the program."""
    arg_list: list = command_processor()             #Calling the command processor to process the command line 
    
    if arg_list[3] == "q1":
        q1_handler(arg_list)
    elif arg_list[3] == "q2":
        q2_handler(arg_list)                              #Check which question is the user asking.
    elif arg_list[3] == "q3":
        q3_handler(arg_list)
    elif arg_list[3] == "q4":
        q4_handler(arg_list)
    else:
        q5_handler(arg_list)

if __name__ == '__main__':
    main()
