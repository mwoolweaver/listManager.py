## Why .tsv??

> TSV is an alternative to the common comma-separated values (CSV) format, which often causes difficulties because of the need to escape commas – literal commas are very common in text data, but literal tab stops are infrequent in running text.[[1](https://en.wikipedia.org/wiki/Tab-separated_values)]
___
## groups.tsv

enabled | name | description | comment
------------ | -------------| ------------ | -------------  
0 for diabled,<br>1 for enable | Name of Group | A description | The string we<br>use to track entries<br>for this group

for more info see ---> https://docs.pi-hole.net/database/gravity/groups/#group-management
___
## all other .tsv files found in this directory

tpye | domain | enable | comment
------------ | -------------| ------------ | -------------  
0 = exact whitelist,<br>1 = exact blacklist,<br>2 = regex whitelist,<br>3 = regex blacklist | url for domain<br>w/o http or https | 0 for diabled,<br>1 for enable | A description

for more info see ---> https://docs.pi-hole.net/database/gravity/#domain-tables-domainlist
