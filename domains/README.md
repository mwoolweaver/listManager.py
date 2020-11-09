# domains/

We store all info in `.tsv` format and parse it with [pandas](https://github.com/pandas-dev/pandas).
___

- [domains/](#domains)
  * [Why `.tsv`](#why-tsv)
    + [groups.tsv](#groupstsv)
    + [all other .tsv files found in this directory](#all-other-tsv-files-found-in-this-directory)

## Why `.tsv`

[2]: https://www.iana.org/assignments/media-types/text/tab-separated-values

> TSV is an alternative to the common [comma-separated values](https://en.wikipedia.org/wiki/Comma-separated_values) (CSV) format, which
> often causes difficulties because of the need to [escape](https://en.wikipedia.org/wiki/Escape_character) commas – [literal](https://en.wikipedia.org/wiki/Character_literal) commas
> are very common in text data, but literal tab stops are infrequent in running text.
> The IANA standard for TSV[[2]] achieves simplicity by simply disallowing tabs within fields.
>
> Wikipedia - [Tab-separated values](https://en.wikipedia.org/wiki/Tab-separated_values)

more info ---> <http://jkorpela.fi/TSV.html#format>
___

### groups.tsv

enabled | name | description | comment
------------ | -------------| ------------ | -------------  
0 for diabled,<br>1 for enable | Name of Group<br>This is usually the file name<br>or the url it's sourced from | A description | The string we<br>use to track entries<br>for this group

[//]: # (@Pi-hole documentation pages for Gravity SQLite Database)
more info -> <https://docs.pi-hole.net/database/gravity/groups/#group-management>

___

### all other .tsv files found in this directory

tpye | domain | enable | comment
------------ | -------------| ------------ | -------------  
0 = exact whitelist,<br>1 = exact blacklist,<br>2 = regex whitelist,<br>3 = regex blacklist | url for domain<br>w/o http or https | 0 for diabled,<br>1 for enable | A description

[//]: # (@Pi-hole documentation pages for Gravity SQLite Database)
more info -> <https://docs.pi-hole.net/database/gravity/#domain-tables-domainlist>
