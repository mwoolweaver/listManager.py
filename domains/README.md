- [1. domains/](#1-domains-)
  * [1.1. Why `.tsv`](#11-why--tsv-)
    + [1.1.1. groups.tsv](#111-groupstsv)
    + [1.1.2. all other .tsv files found in this directory](#112-all-other-tsv-files-found-in-this-directory)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>

# 1. domains/

Where we store our domains in `.tsv` format.
___

## 1.1. Why `.tsv`

> TSV is an alternative to the common comma-separated values (CSV) format, which
> often causes difficulties because of the need to escape commas – literal commas
> are very common in text data, but literal tab stops are infrequent in running text.[[1]]

[//]: # (Link to info about .tsv format)
[1]: http://jkorpela.fi/TSV.html#format

___

### 1.1.1. groups.tsv

enabled | name | description | comment
------------ | -------------| ------------ | -------------  
0 for diabled,<br>1 for enable | Name of Group | A description | The string we<br>use to track entries<br>for this group

[//]: # (@Pi-hole documentation pages for Gravity SQLite Database)
more info -> <https://docs.pi-hole.net/database/gravity/groups/#group-management>

___

### 1.1.2. all other .tsv files found in this directory

tpye | domain | enable | comment
------------ | -------------| ------------ | -------------  
0 = exact whitelist,<br>1 = exact blacklist,<br>2 = regex whitelist,<br>3 = regex blacklist | url for domain<br>w/o http or https | 0 for diabled,<br>1 for enable | A description

[//]: # (@Pi-hole documentation pages for Gravity SQLite Database)
more info -> <https://docs.pi-hole.net/database/gravity/#domain-tables-domainlist>
