# Analyzing the `arin-issued` mailing list

The American Registry of Internet Numbers maintains a mailing list on which daily posts are made to tell subscribers what resources (ASNs and IP ranges) ARIN has taken back into their pool and which resources have been issued. 

The code in this repository is designed to perform some analysis on the archives of this data.# Analyzing the `arin-issued` mailing list

The American Registry of Internet Numbers maintains a mailing list on which daily posts are made to tell subscribers what resources (ASNs and IP ranges) ARIN has taken back into their pool and which resources have been issued. 

The code in this repository is designed to perform some analysis on the archives of this data.# Analyzing the `arin-issued` mailing list

The American Registry of Internet Numbers maintains a mailing list on which daily posts are made to tell subscribers what resources (ASNs and IP ranges) ARIN has taken back into their pool and which resources have been issued. 

The code in this repository is designed to perform some analysis on the archives of this data.

## How do it werk

The `builddb.py` script builds the CSV database. It looks for `.txt.gz` files in the `archives` directory, unzips them, and parses the archive text from the email. This gets placed into a Pandas Dataframe and then serialized to CSV.


