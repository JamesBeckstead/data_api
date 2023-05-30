
## Step 1: Design a schema for the resulting database for the clean data in SQL (your final clean tables from step 1 should match these).Create table statements and a schema diagram are required.

With the need for normalization the **Snow Flake Schema** stood out as a clear chose. 

The **Snow Flake Schema** is setup as follows:
- Fact table
    - *Policies*
- Demension Tables
    - *Data_Providers*
    - *Carriers*
    - *Benefits*
    - *Dates*
- Demension Table with one reference to another Demension table
    - *Insured*

This method of design allowed me to keep the data linked while having to enter the repeated data only once.
\* The exception being that for some of the tables I did allow for multiple entries of the "same" data.
    
        Insured persons could have the same name, but different birth dates. 
        I took these persons as different persons, therefore allowing the same name listed twice.

        For example:
            name: Gloria Murray dob: null
            name: Gloria Murray dob: "1931-09-27"

        The carrier table has a similar logic, but the difference is the name.

        For example:
            carrier_name: "AG"
            carrier_name: "American General"

        The above examples could, of course, be modified after direction from someone who is familiar with the industry
        or at the behest of management.


#### Create table statements [found here](app\models\models.py).
#### Schema diagram [found here](app\scripts\schema_diagram.pgerd).

## Step 2: Build an ETL pipeline to stage, transform, and load the data into the final schema created in step 1. Please include as much information from the raw data as possible. If removing data points or columns, provide an explanation.

&nbsp;&nbsp;&nbsp;&nbsp;The data is in a csv, so the simpliest approach is to have pandas read it into a dataframe.

\* csv is located [here](app\scripts\life_policy_data.csv)

&nbsp;&nbsp;&nbsp;&nbsp;Once it is loaded the **CustomValidator** is used to ensure each column is encoded with the appropriate datatype.
- *str*
- *int*
- *np.datetime64* (I thought this date format looked more universal)

&nbsp;&nbsp;&nbsp;&nbsp;After the data is validated the process of transforming and loading takes place.

&nbsp;&nbsp;&nbsp;&nbsp;This is done in the **populate_tables** method in multiple steps.

### step 1: Determine if the value is in the database already (uses **already_in_database**)

&nbsp;&nbsp;&nbsp;&nbsp;If the data is already in the database, the id is returned.

&nbsp;&nbsp;&nbsp;&nbsp;If the data is not in the database, *None* is returned.

### step 2: Either the data is put into the database, (uses **put_in_db**), or the id is saved.

&nbsp;&nbsp;&nbsp;&nbsp;If the data is put into the database the id, created by the placement in the table, is saved.

### step 3: The policy table **policies** is updated to include the above referenced ids.

### step 4: The insured person table **insured** is update to include a reference to the **dates** table for the dob.


\* no columns were removed and no data was excluded.

## Step 3: Design a Restful API (tip: use flask) with the following endpoints that would:

- policy-info

This endpoint queries the **policies** table and returns the following ids, which are queried in the assocaited tables

<div align="center">

| Data Point    | Table Queried |
|:--------------|:--------------|
|policy_id      | **policies**  |
|effective_date | **dates**     |
|issue_date     | **dates**     |
|maturity_date  | **dates**     |
|death_benefit  | **benefits**  |
|carrier_name   | **carriers**  |

</div>

- carrier-policy-count

This endpoint queries the **carrier** table first, the **policies** table second, and returns the following a count

<div align="center">

| Data Point    | Table Queried |
|:--------------|:------------- |
|carrier_id     | **carriers**  |
|policy_id      | **policies**  |

</div>

- person-policies

This endpoint queries the **insured** table first, the **policies** table second, and returns the following a list of all policies associated with that person.

<div align="center">

| Data Point    | Table Queried |
|:--------------|:------------- |
|insured _id    | **insureced** |
|policy_id      | **policies**  |

</div>

- data-provider-policies

This endpoint takes in a **data_provider code** queries the **data_providers** table first, the **policies** table second, and returns a count of all the policies on record.

<div align="center">

| Data Point  | Table Queried      |
|:------------|:-------------------|
| provider_id | **data_providers** |
| policy_id   | **policies**       |

</div>

\* **Flask** was used to create this API; however, consideration should be made for the use of the **FastAPI** library.


# Things to Note
 
Each file can be run individually. This was done so that the dev could run the **database.py** file and remove all
of the tables that were created in the *homework* schema.

I was not able to get the code in **command_line.py** file to run on my windows machine. See extra instructions below
for what needs to be setup before running this program.


# Instructions to Run this App

To run this program:

1. setup a postgresql database

    &nbsp;&nbsp;&nbsp;&nbsp;[see this page for help](https://www.postgresql.org/docs/15/index.html)

    &nbsp;&nbsp;&nbsp;&nbsp;- the [*db_create.sql*](app\scripts\db_create.sql) file has the code


2. create a schema


    &nbsp;&nbsp;&nbsp;&nbsp;- the [*db_create.sql*](app\scripts\db_create.sql) file has the code 


3. *cd* into the directory containing the **app.py** file

4. run the following command:

    &nbsp;&nbsp;&nbsp;&nbsp;*python app.py -f C:\Users\jtbec\Downloads\life_policy_data.csv*


## Example of how to use the entire pipeline

If the above instructions have been followed, the following example will work to run the entire pipeline

1. *cd* into the directory containing the **app.py** file

2. run the following command:

    &nbsp;&nbsp;&nbsp;&nbsp;*python app.py*

If you want to run each file separately, please see the following example.

- create database tables (if `True` is passed into the class, tables will be deleted)

    *python database.py*

- ETL (csv file is hardcoded to be should be passed in with the -f keyword aurgement)

    *python read_data.py -f C:\Users\jtbec\Downloads\life_policy_data.csv*

- api (api is set to run on http://127.0.0.1:5000)

    *python app.py -f C:\Users\jtbec\Downloads\life_policy_data.csv*
