"""
----------------------------------
The SciBib Package
----------------------------------
This package enables scientific bibliographical data retrieval from
an author's Orcid id. The main goal is to collect bibtex entries for
the authors works and to collect abstracts for theses works.


Bibtex collection works fine provided the author has an orcid record and
the sought article is referenced there, see data_query.OrcidWork.bibtex.

Abstract retrieval can be performed using ArXiv's API if the article is 
on the Arxiv and the author associated her/his orcid id with her/his arxiv
account, see data_query.AuthorData.work_summary_from_arxiv.

Another option is to get a (sometimes more up-to-date) abstract scraping
the journal's website. In this case, some legal or technical obstructions
might appear. However, a tool to try this technique is provided, namely 
the scrape_abstract method of our OrcidWork class.

Another useful feature is to use the doi of a work to build an url that
leads to the article in the publisher's website. This can be obtained
with OrcidWork.doi.

Other data sources and other outputs could be added in the future,
depending of the users' suggestions/pull requests.
"""
