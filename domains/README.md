## groups.tsv

enabled | name | description | comment
------------ | -------------| ------------ | -------------  
1 for enable, 0 for diabled | Name of Group | A description | The string we use to track entries for this group

for more info see ---> https://docs.pi-hole.net/database/gravity/groups/#group-management

## all other .tsv files found in this directory

tpye | domain | enable | comment
------------ | -------------| ------------ | -------------  
0 = exact whitelist,<br>1 = exact blacklist,<br>2 = regex whitelist,<br>3 = regex blacklist | url for domain w/o http or https | 1 for enable, 0 for diabled | A description

for more info see ---> https://docs.pi-hole.net/database/gravity/#domain-tables-domainlist
